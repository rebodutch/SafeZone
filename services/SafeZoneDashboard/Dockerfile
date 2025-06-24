FROM python:3.13-slim

# Copy requirements file into the container
COPY services/SafeZoneDashboard/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

# Copy all project files into the container
COPY services/SafeZoneDashboard/app /app
# copy utils
COPY utils /app/utils

ENV PYTHONPATH=/app

CMD ["python", "/app/main.py"]