# Apache Superset Docker Setup

## Overview
This document provides step-by-step instructions for setting up **Apache Superset** using **Docker and PostgreSQL**. The setup includes:
- **A custom Dockerfile** to allow modifications.
- **A `docker-compose.yml` file** to orchestrate Superset and PostgreSQL.
- **An initialization script** to automate database setup.
- **Persistent storage** for Superset metadata.

## Prerequisites
- **Docker** installed ([Guide](https://docs.docker.com/get-docker/))
- **Docker Compose** installed ([Guide](https://docs.docker.com/compose/install/))

## **Project Structure**
```
graphql-data-analysis/
├── docker/
│   ├── superset/
│   │   ├── Dockerfile
│   │   ├── init_superset.sh
│   ├── postgres/
├── docker-compose.yml
```

---

## **1️⃣ Dockerfile for Superset**
Located at **`docker/superset/Dockerfile`**, this file builds a custom Superset image.

```dockerfile
FROM apache/superset:latest

# Install additional dependencies if needed
USER root
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Copy the initialization script
COPY init_superset.sh /app/init_superset.sh

CMD ["/app/init_superset.sh"]
```

---

## **2️⃣ Initialization Script: `init_superset.sh`**
This script ensures Superset is properly initialized. Make sure to give it execute perms before copying to Docker. 

```bash
#!/bin/bash

# Wait for PostgreSQL to be ready
while ! nc -z superset-db 5432; do
  sleep 1
done
echo "Database is ready!"

# Initialize Superset
superset db upgrade
superset fab create-admin --username admin --firstname Superset --lastname Admin --email admin@example.com --password admin
superset init

# Start Superset
exec gunicorn -w 2 -b 0.0.0.0:8088 "superset.app:create_app()"
```

---

## **3️⃣ Docker Compose File: `docker-compose.yml`**
The `docker-compose.yml` defines **Superset and PostgreSQL services**.

```yaml
version: "3.8"

services:
  superset:
    build: ./docker/superset
    container_name: superset
    restart: always
    ports:
      - "8088:8088"
    environment:
      - SUPERSET_SECRET_KEY=your_secret_key_here
      - SQLALCHEMY_DATABASE_URI=postgresql://superset:superset@superset-db:5432/superset
    depends_on:
      - superset-db
    volumes:
      - superset_home:/app/superset_home

  superset-db:
    image: postgres:15
    container_name: superset-db
    restart: always
    environment:
      POSTGRES_USER: superset
      POSTGRES_PASSWORD: superset
      POSTGRES_DB: superset
    volumes:
      - superset_db_data:/var/lib/postgresql/data

volumes:
  superset_home:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /home/your-username/dev/tools/superset
  superset_db_data:
```

---

## **4️⃣ Running Superset**
After setting up the project, **build and start Superset**:
```bash
docker compose up -d --build
```

### **Access Superset**
- Open: **http://localhost:8088**
- Login with:
  - **Username:** `admin`
  - **Password:** `admin`

To stop containers:
```bash
docker compose down
```

---

## **5️⃣ Persistent Storage**
- **Superset metadata** is stored in `~/dev/tools/superset/` on your Ubuntu machine.
- **PostgreSQL data** is persisted in a Docker volume.

---

## **6️⃣ Troubleshooting**

### **Check Logs**
To see Superset logs:
```bash
docker logs superset --follow
```
To check PostgreSQL logs:
```bash
docker logs superset-db --follow
```

---



