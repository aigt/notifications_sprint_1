FROM python:3.10

WORKDIR /opt/app

COPY requirements.txt requirements.txt

# hadolint ignore=DL3013
RUN  pip install --upgrade pip --no-cache-dir && \
    pip install -r requirements.txt --no-cache-dir

COPY ./src .
