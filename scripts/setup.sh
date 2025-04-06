#!/bin/bash

# Create necessary directories
mkdir -p logs plugins

# Set up environment variables
echo "AIRFLOW_UID=$(id -u)" > .env
echo "AIRFLOW_GID=0" >> .env

# Build and start the containers
docker-compose -f docker/docker-compose.yml up --build -d

# Wait for Airflow to be ready
echo "Waiting for Airflow to be ready..."
sleep 30

# Create an admin user
docker-compose -f docker/docker-compose.yml exec airflow-webserver airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

echo "Setup completed! Airflow is running at http://localhost:8080"
echo "Username: admin"
echo "Password: admin" 