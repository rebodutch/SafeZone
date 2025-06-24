FROM python:3.13-slim

COPY toolkit/time-server/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

COPY toolkit/time-server /app
COPY utils /app/utils

ENV PYTHONPATH=/app
WORKDIR /app

CMD ["python", "main.py"]