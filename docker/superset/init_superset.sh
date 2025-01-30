#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for database to be ready..."
while ! nc -z superset-db 5432; do
  sleep 1
done
echo "Database is ready!"

# Initialize the database
superset db upgrade

# Create an admin user (if not exists)
superset fab create-admin \
    --username admin \
    --firstname Superset \
    --lastname Admin \
    --email admin@example.com \
    --password admin

# Initialize roles and configurations
superset init

# Start Superset
exec gunicorn -w 2 -b 0.0.0.0:8088 "superset.app:create_app()"
