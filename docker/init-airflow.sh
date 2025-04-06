#!/bin/bash

# Wait for postgres
echo "Waiting for postgres..."
until PGPASSWORD=airflow psql -h "postgres" -U "airflow" -d "airflow" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 5
done

>&2 echo "Postgres is up - executing commands"

# Initialize the database
echo "Initializing Airflow database..."
airflow db init

# Create default connections
echo "Creating default connections..."
airflow connections list | grep -q "postgres_default" || \
    airflow connections add 'postgres_default' \
    --conn-type 'postgres' \
    --conn-host 'postgres' \
    --conn-login 'airflow' \
    --conn-password 'airflow' \
    --conn-port '5432'

# Create admin user
echo "Creating admin user..."
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

echo "Airflow initialization completed!" 