FROM python:3.13-slim

COPY services/SafeZoneAnalyticsAPI/environments/test/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

COPY tools/cli /app

ENV PYTHONPATH=/app