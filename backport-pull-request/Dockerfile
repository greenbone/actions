ARG DEBIAN_FRONTEND=noninteractive

FROM python:3.9-slim

RUN apt-get update && \
    apt-get install --no-install-recommends --no-install-suggests -y \
    git && \
    apt-get remove --purge --auto-remove -y && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python3 -m pip install poetry

COPY . /action
WORKDIR /action

RUN poetry build -f wheel && python3 -m pip install dist/*

CMD ["backport-pull-request" ]

