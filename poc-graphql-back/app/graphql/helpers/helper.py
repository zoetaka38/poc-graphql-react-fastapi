import re

from sqlalchemy import delete, insert, select
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import load_only, selectinload, subqueryload
from strawberry.dataloader import DataLoader

from app.graphql.db.session import get_session


def convert_camel_case(name):
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    name = pattern.sub("_", name).lower()
    return name


def get_only_selected_fields(db_baseclass_name, info):
    db_relations_fields = inspect(db_baseclass_name).relationships.keys()
    result = {"base": [], "relations": {}}

    for field in info.selected_fields[0].selections:
        field_name = convert_camel_case(field.name)
        if field.name not in db_relations_fields:
            result["base"].append(field_name)
        else:
            result["relations"][field_name] = [convert_camel_case(sub_field.name) for sub_field in field.selections]

    return result


def get_valid_data(model_data_object, model_class):
    data_dict = {}
    for column in model_class.__table__.columns:
        try:
            data_dict[column.name] = getattr(model_data_object, column.name)
        except:
            pass
    return data_dict


async def fetch_single_data(scalar_mapping, selected_fields, model, data_scalar, id):
    async with get_session() as s:
        sql = (
            select(model)
            .options(load_only(*[getattr(model, attr) for attr in selected_fields["base"]]))
            .filter_by(id=id)
        )
        for key, value in selected_fields["relations"].items():
            relation_attr = getattr(model, key)
            sql = sql.options(
                selectinload(relation_attr).load_only(*[getattr(relation_attr.mapper.class_, attr) for attr in value])
            )
        db_data = (await s.execute(sql)).scalars().first()
        if db_data is None:
            return None

        data_dict = get_valid_data(db_data, model)
        for relation, fields in selected_fields["relations"].items():
            related_objects = getattr(db_data, relation)
            data_dict[relation] = [get_valid_data(obj, obj.__class__) for obj in related_objects]

        for relation, scalar in scalar_mapping.items():
            if relation in data_dict:
                data_dict[relation] = [scalar(**note) for note in data_dict[relation]]

        return data_scalar(**data_dict)


async def batch_load_models(model_ids, model, selected_fields):
    async with get_session() as s:
        sql = (
            select(model)
            .filter(model.id.in_(model_ids))
            .options(load_only(*[getattr(model, attr) for attr in selected_fields["base"]]))
        )
        db_data = (await s.execute(sql)).scalars().all()
        # IDをキーとする辞書を作成
        model_map = {obj.id: obj for obj in db_data}
        # 入力の順序に合わせて結果を返す
        return [model_map.get(model_id) for model_id in model_ids]


def get_fk_attribute_name(related_model, parent_model):
    for column in related_model.__table__.columns:
        for fk in column.foreign_keys:
            if fk.column.table == parent_model.__table__:
                return column.name
    return None


async def batch_load_relations(parent_ids, parent_model, relation_name, selected_fields):
    relation_attr = getattr(parent_model, relation_name)
    related_model = relation_attr.property.mapper.class_

    # ヘルパー関数を使用して外部キー属性名を取得
    fk_attribute_name = get_fk_attribute_name(related_model, parent_model)
    if fk_attribute_name is None:
        raise ValueError(f"{related_model.__name__}に{parent_model.__name__}への外部キーが見つかりませんでした。")

    async with get_session() as s:
        sql = (
            select(related_model)
            .filter(getattr(related_model, fk_attribute_name).in_(parent_ids))
            .options(load_only(*[getattr(related_model, attr) for attr in selected_fields + [fk_attribute_name]]))
        )
        db_data = (await s.execute(sql)).scalars().all()

        # 親IDごとに関連オブジェクトをマッピング
        relation_map = {}
        for obj in db_data:
            parent_id = getattr(obj, fk_attribute_name)
            relation_map.setdefault(parent_id, []).append(obj)

        # 入力の順序に合わせて結果を返す
        return [relation_map.get(parent_id, []) for parent_id in parent_ids]


async def fetch_data(scalar_mapping, selected_fields, model, data_scalar, target_ids=[]):
    # Dataloaderのインスタンスを作成
    model_loader = DataLoader(load_fn=lambda ids: batch_load_models(ids, model, selected_fields))
    relation_loaders = {}
    for relation, fields in selected_fields["relations"].items():
        relation_loaders[relation] = DataLoader(
            load_fn=lambda parent_ids, r=relation, f=fields: batch_load_relations(parent_ids, model, r, f)
        )

    # 対象のIDリストを取得
    if target_ids:
        ids = target_ids
    else:
        # 全てのIDを取得
        async with get_session() as s:
            ids = (await s.execute(select(model.id).order_by(model.id))).scalars().all()

    # ベースモデルのデータをロード
    db_data = await model_loader.load_many(ids)
    data_list = []
    for obj in db_data:
        if obj is None:
            continue  # データが存在しない場合はスキップ
        data_dict = get_valid_data(obj, model)

        # リレーションのデータをロード
        for relation, loader in relation_loaders.items():
            related_objects = await loader.load(getattr(obj, "id"))
            data_dict[relation] = [get_valid_data(rel_obj, rel_obj.__class__) for rel_obj in related_objects]

            # スカラーに変換
            if relation in scalar_mapping:
                scalar = scalar_mapping[relation]
                data_dict[relation] = [scalar(**item) for item in data_dict[relation]]

        data_list.append(data_scalar(**data_dict))
    return data_list
