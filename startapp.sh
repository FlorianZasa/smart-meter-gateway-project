#!/bin/bash

# Start pomdan machine and Docker container
echo "Starting Docker container..."
podman machine init
podman machine start
podman-compose up -d

# Wait for the container to be ready (adjust the sleep time as needed)
echo "Waiting for container to be ready..."
sleep 10

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Start the Python application
echo "Starting Python application..."
python main.py
