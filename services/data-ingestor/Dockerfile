FROM python:3.13-slim

# Copy requirements file into the container
COPY services/data-ingestor/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

COPY services/data-ingestor/app /app
COPY utils /app/utils

ENV PYTHONPATH=/app
WORKDIR /app

CMD ["python", "main.py"]