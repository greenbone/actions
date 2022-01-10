ARG DEBIAN_FRONTEND=noninteractive

FROM debian:stable-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install --no-install-recommends --no-install-suggests -y \
    git \
    python3 \
    python3-pip && \
    apt-get remove --purge --auto-remove -y && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install poetry

COPY . /action
WORKDIR /action

RUN poetry build -f wheel && python3 -m pip install dist/*

CMD ["backport-pull-request" ]

