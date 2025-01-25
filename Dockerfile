# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install required dependencies for venv creation
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-venv python3-dev gcc build-essential libssl-dev libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy the application code into the container
COPY . /app

# Explicitly call python3 for venv creation
RUN python3 -m venv /app/venv

# Upgrade pip and install dependencies inside the virtual environment
RUN /app/venv/bin/python -m pip install --upgrade pip && \
    /app/venv/bin/python -m pip install -r /app/requirements.txt

# Expose the Flask app port
EXPOSE 5000

# Command to activate the virtual environment and start the app
CMD ["/bin/bash", "-c", "source /app/venv/bin/activate && flask run --host=0.0.0.0 --port=5000"]
