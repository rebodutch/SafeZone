FROM python:3.13-slim

COPY tools/cli/relay/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

COPY tools/cli/relay /app
COPY tools/cli/schemas /app/schemas
COPY utils /app/utils

ENV PYTHONPATH=/app

WORKDIR /app

CMD ["python", "app.py"]