FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app
ENV GROUP=app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR ${APP_HOME}

COPY ./pyproject.toml ./poetry.lock /

RUN apt-get update \
    && apt-get install -y gettext \
    && apt install -y ncat \
    && python -m pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root

COPY ./src /

RUN groupadd -r ${GROUP} \
    && useradd -d ${APP_HOME} -r -g ${GROUP} ${GROUP} \
    && chown ${GROUP}:${GROUP} -R ${APP_HOME}     
USER ${GROUP}