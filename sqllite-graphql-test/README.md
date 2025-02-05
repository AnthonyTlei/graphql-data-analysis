# SQLite DB GraphQL Demo

This project demonstrates a dynamic approach to ingest data from a GraphQL endpoint and materialize it as a SQLite database. We leverage GraphQL introspection to dynamically map the schema, flatten nested objects, and then query the resulting SQL database using SQLAlchemy.

---

## Table of Contents

- [Goal](#goal)
- [Overview](#overview)
- [Setup](#setup)
- [Detailed Workflow](#detailed-workflow)
  - [Introspection and Dynamic Mapping](#introspection-and-dynamic-mapping)
  - [Materializing the SQL Database](#materializing-the-sql-database)
  - [Querying the Database with SQLAlchemy](#querying-the-database-with-sqlalchemy)
- [GraphQL Endpoint](#graphql-endpoint)
- [Challenges and Limitations](#challenges-and-limitations)
- [Future Improvements](#future-improvements)

---

## Goal

The goal of this project is to create a proof-of-concept that:

- **Dynamically retrieves the schema** of a GraphQL endpoint using introspection.
- **Maps the GraphQL schema** (with support for nested objects) into a relational SQLite database.
- **Materializes the data** from a live GraphQL API into a persistent SQLite file (`countries.db`).
- **Queries the database** using SQLAlchemy to validate that the data was correctly ingested.


## Overview

This demo uses the public **Countries GraphQL API** as its data source. The process includes:

1. **Introspection**: Fetches the schema metadata using a GraphQL introspection query.
2. **Dynamic Mapping and Table Creation**: Generates an SQLite table based on the schema.
3. **Data Ingestion**: Queries the GraphQL API, flattens JSON responses, and inserts data into SQLite.
4. **SQL Querying**: Uses SQLAlchemy to validate data persistence.


## Setup

Follow these steps to set up and run the project:

### 1. Use project root

Ensure you're in `sqlite-db-graphql` dir with the following structure:

```
sqlite-db-graphql/
├── countries.db   # (This file will be created automatically after running the script)
├── src/
│   └── app.py
└── requirements.txt
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

From the `sqlite-db-graphql` directory, execute:

```bash
python src/app.py
```

The script will:

- Fetch GraphQL introspection data.
- Create and populate the SQLite database (`countries.db`).
- Run sample SQL queries using SQLAlchemy to verify the data.

---

## Detailed Workflow

### Introspection and Dynamic Mapping

#### 1. Introspection Query

The script sends a GraphQL introspection query to retrieve schema metadata, saving it to `schema_metadata.json` for debugging.

#### 2. Dynamic Column Extraction

- The function `get_columns_for_type` inspects the schema to:
  - Extract scalar fields and map them to SQL columns (`TEXT` type).
  - Flatten nested objects by concatenating keys (e.g., `continent_code`, `continent_name`).

#### 3. Table Creation

- The function `create_table_for_type` generates a `CREATE TABLE` statement and initializes the SQLite database.

---

### Materializing the SQL Database

- **Database File**: `countries.db` is created at the project root.
- **Data Insertion**: Flattened JSON records are inserted into SQLite via `insert_flattened_data`.

---

### Querying the Database with SQLAlchemy

- **SQLAlchemy Engine**: Connects to the SQLite database for querying.
- **Example Queries**:
  - **Count Query**: Retrieves the total number of records.
  - **Sample Query**: Fetches a few rows to confirm data ingestion.

---

## GraphQL Endpoint

This demo uses the **Countries GraphQL API**, which provides data on countries, including fields such as:

- `code`, `name`, `capital`, `currency`
- Nested objects: `continent`, `languages`

The endpoint supports introspection, making it ideal for dynamic schema mapping.

## Challenges and Limitations

While this demo successfully materializes a GraphQL endpoint into a SQLite database, there are several limitations:

1. **Flattening Nested Structures**:
   - Simple key concatenation loses deeper relational context.
2. **Handling Lists**:
   - Simple lists are concatenated; complex nested objects are ignored.
3. **Uniform Data Types**:
   - All fields are mapped to `TEXT`, ignoring numbers, booleans, and dates.
4. **Complex GraphQL Features**:
   - Unions, interfaces, and federated schemas are not fully supported.
5. **Schema Evolution**:
   - No automatic handling of schema changes in the SQLite database.

## Future Improvements

To extend this demo, consider the following enhancements:

1. **Normalization**:
   - Generate separate tables for nested objects instead of flattening.
2. **Advanced Type Mapping**:
   - Map GraphQL scalar types to appropriate SQL types.
3. **Handling Complex Constructs**:
   - Support unions, interfaces, and object lists via join tables or JSON columns.
4. **Hybrid Storage Models**:
   - Use JSON columns in databases like PostgreSQL for deeply nested data.
5. **Dynamic Schema Updates**:
   - Implement schema change detection and database migration logic.

This project serves as a foundation for dynamic GraphQL data ingestion into SQL. For production use, further refinements will be necessary.

