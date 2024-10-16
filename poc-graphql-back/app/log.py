import json
import logging
import typing
from collections.abc import Callable, Mapping, MutableMapping

# https://docs.python.org/ja/3/library/logging.html#logrecord-attributes
RESERVED_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
}


def safe_extra(extra: dict[str, typing.Any]) -> dict[str, typing.Any]:
    """extraは予約された要素とバッティングを避ける
    Analytics のエラーレスポンスの message 要素の競合を避けるのが主な目的
    """
    for attr in RESERVED_ATTRS:
        if attr in extra:
            value = extra.pop(attr)
            extra[attr + "_"] = value
    return extra


def shorten_rule(v: list[dict]) -> list:
    shorten = v[:3]
    for i in shorten:
        i["rule_json"] = i["rule_json"][:20] + "..."
    return shorten


NEED_MASK: Mapping[str, Callable] = {
    "password": lambda v: "***",
    "sip_password": lambda v: "***",
    "sip_password_ws": lambda v: "***",
    "turn_password": lambda v: "***",
    "cookie": lambda v: "***",
}

NEED_SHORTEN: Mapping[str, Callable] = {
    "rules": shorten_rule,
    "rule_json": lambda v: v[:20] + "...",
}


def mask(dic: MutableMapping[str, typing.Any]) -> Mapping[str, typing.Any]:
    for k, v in dic.items():
        if isinstance(v, dict):
            dic[k] = mask(v)
        elif k in NEED_MASK:
            dic[k] = NEED_MASK[k](v)
        elif k in NEED_SHORTEN:
            dic[k] = NEED_SHORTEN[k](v)
        elif isinstance(v, list):
            # リストの要素は極力NEED_SHORTENで対応すること
            if len(v) > 10:
                dic[k] = v[:10]
                dic[k].append("...")
            else:
                dic[k] = v
        else:
            pass
    return dic


# https://docs.python.org/ja/3/library/json.html#py-to-json-table
JsonSerializable = typing.Union[dict, list, tuple, str, int, float, bool, None]


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        message_obj = {
            "asctime": getattr(record, "asctime", None),
            "message": message,
            "name": record.name,
            "created": record.created,
            "msecs": record.msecs,
            "level": record.levelname,
            # https://docs.datadoghq.com/logs/log_configuration/attributes_naming_convention/#source-code
            "logger": {
                "name": record.name,
                "thread_name": record.threadName,
                "method_name": record.funcName,
                "lineno": record.lineno,
            },
        }
        message_obj.update(self.get_extra(record))
        return json.dumps(message_obj, default=self.default, ensure_ascii=False)

    def get_extra(self, record: logging.LogRecord) -> typing.Mapping:
        return {
            attr: record.__dict__[attr] for attr in record.__dict__ if attr not in RESERVED_ATTRS
        }

    def default(self, obj: typing.Any) -> JsonSerializable:
        print(obj)
        return "this object can not be dumped"


def init_app(name: str, log_level: str, echo_sql: bool) -> None:
    app_logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    app_logger.addHandler(handler)
    app_logger.setLevel(log_level)

    if echo_sql:
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        logging.getLogger("sqlalchemy.engine").addHandler(handler)
        logging.getLogger("sqlalchemy.engine").setLevel(log_level)
        logging.getLogger("sqlalchemy.pool").addHandler(handler)
        logging.getLogger("sqlalchemy.pool").setLevel(log_level)
