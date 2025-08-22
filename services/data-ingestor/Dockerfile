# stage 1: build dependencies
FROM python:3.13-slim AS builder

# Copy requirements file into the container
COPY services/data-ingestor/requirements.txt .

# Install dependencies
RUN pip install --upgrade pip \
    && pip install --only-binary=:all: --no-cache-dir -r requirements.txt 

# Clean up to reduce image size
RUN pip cache purge \
    && find /usr/local/lib/python3.13 -type d -name "__pycache__" -exec rm -r {} +

# stage 2: build the application
FROM python:3.13-slim AS runner

# Copy the installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

# Copy the application code into the container
COPY services/data-ingestor/app /app

# Copy additional directories
COPY utils/logging /app/utils/logging
COPY utils/pydantic_model /app/utils/pydantic_model
COPY utils/context.py /app/utils/context.py

ENV PYTHONPATH=/app
WORKDIR /app

CMD ["python", "main.py"]