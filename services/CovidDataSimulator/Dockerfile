FROM python:3.13-slim

# Copy all project files into the container
COPY . .

# Install dependencies specified in requirements.txt
# Note: When running 'pip install' as root, a warning is generated 
# because running pip as root without using a virtual environment can lead to permission issues or conflicts.
# To suppress the warning, the '--root-user-action=ignore' option 
# is used to indicate that this behavior is intentional and safe within the Docker context.
RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

# Set the working directory to /app
WORKDIR /app

# Define the entrypoint command to run the application
CMD ["python3", "main.py"]
