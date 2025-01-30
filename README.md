# GraphQL Data Analysis

## 📌 Overview
This project aims to **perform data analysis on GraphQL endpoints** using different methods. The goal is to seamlessly query GraphQL APIs using SQL-like syntax, enabling efficient data visualization and insights.

We explore multiple approaches to achieve this:
- **CData Python Connector** - Using Python to query GraphQL APIs via SQL.
- **Superset + CData** - Integrating CData with Apache Superset to visualize GraphQL data.


## 🚀 Available Methods

### **1️⃣ CData Python Connector**
Use the **CData Python Connector** to interact with GraphQL endpoints in a Python environment. This approach allows you to:
- Query GraphQL APIs using SQLAlchemy.
- Store and analyze the results in Pandas DataFrames.
- Integrate with other Python-based data analysis tools.

📖 **Read more:** [CData Python Connector Guide](cdata-connector-test/README.md)

---

### **2️⃣ Apache Superset + CData**
Integrate **CData GraphQL Connector** with **Apache Superset**, allowing GraphQL queries to be executed directly inside Superset’s SQL Lab. This method provides:
- A GUI-based interface for querying GraphQL APIs.
- Dashboard creation and data visualization.
- Easy SQL-based analytics over GraphQL datasets.

📖 **Read more:** [Superset with CData Guide](docker/superset-cdata-support/README.md)

---

### **3️⃣ Standalone Superset (For General Use)**
If you want to use **Apache Superset without CData**, you can set it up as a standalone tool for traditional SQL-based analytics.

📖 **Read more:** [Superset Standalone Guide](docker/superset/README.md)

---

## 📊 Getting Started
To start using any of these methods, follow the detailed instructions in each guide. Ensure you have **Docker installed** and the necessary dependencies configured.

