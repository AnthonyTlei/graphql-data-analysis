# Superset with CData GraphQL Connector

This setup runs **Apache Superset** with **CData GraphQL Connector**, allowing Superset to **query GraphQL APIs using SQLAlchemy**.

---

## **📌 1. Prerequisites**
Before proceeding, ensure you have:
- **Docker & Docker Compose installed**
- **CData Python Connector for GraphQL**

For more steps on installing superset (standalone) or using Cdata's connector in a python app check Additional Resources.


---

## **🚀 2. Setup & Installation**

### **Place the CData Connector inside the build directory**
Ensure `cdata-graphql-connector-24.0.9111-python3.tar.gz` is inside:
```
graphql-data-analysis/docker/superset-cdata-support/
```

## **Docker Compose File: `docker-compose.yml`**
The `docker-compose.yml` defines **Superset and PostgreSQL services**.

```yaml
version: "3.8"

services:
  superset:
    build: ./docker/superset-cdata-support
    container_name: superset
    restart: always
    ports:
      - "8088:8088"
    environment:
      - SUPERSET_SECRET_KEY=superset
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
      device: /home/<your-username>/dev/tools/superset
  superset_db_data:

```

### **Build and Start Superset**
```bash
docker compose build superset
docker compose up -d
```

This will:
- Build the **Superset + CData** image.
- Start **Superset and PostgreSQL**.

---

## **🔑 3. Activate CData License**
CData requires a **license activation** inside the container.

### **Step 1: Enter the Superset Container**
```bash
docker exec -it superset bash
```

### **Step 2: Navigate to the License Activation Directory**
```bash
cd /usr/local/lib/python3.10/site-packages/cdata/installlic_graphql
```

### **Step 3: Run the License Activation Command**
```bash
./install-license.sh <YOUR_LICENSE_KEY>
```
If you don't have a license key, you can activate a **trial license**:
```bash
./install-license.sh
```

### **Step 4: Restart Superset**
After activation, restart the Superset service:
```bash
docker compose restart superset
```

---

## **🧪 4. Test Connection in Superset**

### **Step 1: Open Superset UI**
Go to **[http://localhost:8088](http://localhost:8088)**.

### **Step 2: Add a New Database**
1. Navigate to **Settings → Database Connections**.
2. Click **`+ Database`** and choose **`Other`**.
3. **Enter the SQLAlchemy URI:**
   ```
   graphql://?URL=https://countries.trevorblades.com/
   ```
4. Click **`Test Connection`**.
5. If successful, **Save** the connection.

---

## **📊 5. Running SQL Queries on GraphQL**

Once connected, **go to SQL Lab** and run:
```sql
SELECT * FROM countries
WHERE continent_name = 'Africa';
```
This queries the GraphQL API **as if it were a SQL database!** 🎉

---

## **📌 7. Cleanup**

To stop and remove all containers:
```bash
docker compose down
```
To rebuild everything:
```bash
docker compose build
docker compose up -d
```

---

## **🔗 8. Additional Resources**
For more steps on using Superset (standalone) or using CData's connector (in a Python app), check:
- [Superset Standalone Guide](../docker/superset/README.md)
- [CData Python Connector Guide](../cdata-connector-test/README.md)

---

## **🚀 Success!**
Now, **Superset is fully set up with CData GraphQL support.** 🎉  
You can visualize **GraphQL data using SQL directly in Superset!** 🔥

