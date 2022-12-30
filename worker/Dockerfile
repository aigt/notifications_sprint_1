FROM python:3.10 as requirements-stage

WORKDIR /tmp

# hadolint ignore=DL3013
RUN  pip install --upgrade pip --no-cache-dir && \
    pip install poetry==1.2.2 --no-cache-dir

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Сборка финального контейнера
FROM python:3.10

ARG APP_USER=appuser
ARG APP_USER_UID=1000
ARG APP_ROOT=/opt/app

EXPOSE 8000/tcp

ENV  PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ROOT=${APP_ROOT}

RUN useradd --create-home --uid=${APP_USER_UID} ${APP_USER}

WORKDIR ${APP_ROOT}

# hadolint ignore=DL3013
RUN  apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip --no-cache-dir \
    && chown ${APP_USER}:${APP_USER} ${APP_ROOT}

COPY --from=requirements-stage /tmp/requirements.txt ${APP_ROOT}requirements.txt

RUN pip install --no-cache-dir --upgrade -r ${APP_ROOT}requirements.txt

COPY --chown=${APP_USER}:${APP_USER} ./src .

USER ${APP_USER}:${APP_USER}

ENTRYPOINT ["python3", "main.py", "main"]
