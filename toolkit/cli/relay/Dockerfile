FROM python:3.13-slim

COPY toolkit/cli/relay/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

COPY toolkit/cli/relay /app
COPY toolkit/cli/schemas /app/schemas
COPY utils /app/utils

ENV PYTHONPATH=/app
WORKDIR /app

CMD ["python", "main.py"]