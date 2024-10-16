FROM python:3.12

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# install environment dependencies
RUN apt-get update -yqq \
  && apt-get install -yqq --no-install-recommends \
  openssl libopencv-dev \
  && apt-get -q clean

# add requirements (to leverage Docker cache)
COPY requirements.txt ./

# install requirements
RUN pip install -U --no-cache-dir -r requirements.txt

COPY ./app/ /usr/src/app/app
COPY ./migrations/ /usr/src/app/migrations
COPY ./alembic.ini /usr/src/app/alembic.ini
# COPY ./api_tests/ /usr/src/app/api_tests
COPY ./gunicorn.conf.py /usr/src/app/gunicorn.conf.py

CMD gunicorn -k uvicorn.workers.UvicornWorker -c /usr/src/app/gunicorn.conf.py app.main:app