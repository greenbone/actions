ARG DEBIAN_FRONTEND=noninteractive

FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python3 -m pip install poetry

COPY . /action
WORKDIR /action

RUN poetry build -f wheel && python3 -m pip install dist/*

CMD ["trigger-workflow"]

