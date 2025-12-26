FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

ARG ENV=prod
ENV ENV=${ENV}

RUN if [ "$ENV" = "dev" ]; then pip install debugpy; fi

COPY src ./src
COPY entrypoint.sh ./entrypoint.sh
COPY entrypoint.dev.sh ./entrypoint.dev.sh


RUN if [ "$ENV" = "dev" ]; then \
    cp /app/entrypoint.dev.sh /app/entrypoint.sh; \
    fi

RUN chmod +x /app/entrypoint.sh

ENV PYTHONPATH=/app/src

EXPOSE 8000


CMD ["./entrypoint.sh"]

