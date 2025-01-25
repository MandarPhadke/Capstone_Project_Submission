# Use a lightweight Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Install required dependencies for venv creation
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential libssl-dev libffi-dev python3 && \
    rm -rf /var/lib/apt/lists/*

# Copy the application code into the container
COPY . /app


# Upgrade pip and install dependencies inside the virtual environment
RUN python -m pip install --upgrade pip && \
    python -m pip install -r /app/requirements.txt

# Expose the Flask app port
EXPOSE 5000

# Command to activate the virtual environment and start the app
CMD ["/bin/bash", "-c", "flask run --host=0.0.0.0 --port=5000"]
