FROM python:3.13-slim

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

COPY . /app

ENV PYTHONPATH=/app
WORKDIR /app

CMD ["python", "app.py"]