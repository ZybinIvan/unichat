FROM python:3.12-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD pyproject.toml /app
RUN apk add --virtual .build-deps --no-cache postgresql-dev gcc python3-dev musl-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir poetry && \
    apk --purge del .build-deps


RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY . .

CMD ["uvicorn","src.main:app", "--host", "0.0.0.0"]