FROM python:3.12-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONPATH $PYTHONPATH:/app

WORKDIR /app

COPY pyproject.toml uv.lock /app/

RUN uv pip install --system -r pyproject.toml


COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-delay=0.5"]
