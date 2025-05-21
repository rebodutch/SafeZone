FROM python:3.13-slim

# Copy requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

# Copy project files into the container
COPY app.py /app
COPY bin /app/bin
COPY job /app/job
COPY ../schemas /app/schemas

ENV PYTHONPATH=/app
WORKDIR /app

# Set the alias for the command
# This will allow you to run the command by simply typing 'szcli' in the terminal
RUN echo 'alias szcli="python3 app.py"' >> ~/.bashrc

# Set the entrypoint to the Python interpreter
ENTRYPOINT ["bash"]
