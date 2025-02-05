#!/usr/bin/env python3
import os
import json
import sqlite3
import requests
from sqlalchemy import create_engine, text

# GraphQL endpoint.
GRAPHQL_URL = "https://countries.trevorblades.com/"

def fetch_introspection(url):
    introspection_query = """
    {
      __schema {
        types {
          name
          kind
          fields {
            name
            type {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                }
              }
            }
          }
        }
      }
    }
    """
    response = requests.post(url, json={"query": introspection_query})
    if response.status_code != 200:
        raise Exception(f"Introspection query failed with status {response.status_code}")
    return response.json()

def unwrap_type(type_obj):
    while type_obj and type_obj.get("kind") in ["NON_NULL", "LIST"]:
        type_obj = type_obj.get("ofType")
    return type_obj

def get_type_definition(type_name, introspection_data):
    types = introspection_data.get("data", {}).get("__schema", {}).get("types", [])
    for t in types:
        if t.get("name") == type_name:
            return t
    raise ValueError(f"Type '{type_name}' not found in introspection data.")

def get_columns_for_type(type_name, introspection_data, prefix=""):
    type_def = get_type_definition(type_name, introspection_data)
    columns = []
    fields = type_def.get("fields", [])
    for field in fields:
        field_name = field["name"]
        unwrapped = unwrap_type(field["type"])
        if not unwrapped:
            continue
        kind = unwrapped.get("kind")
        if kind in ["SCALAR", "ENUM"]:
            columns.append((prefix + field_name, "TEXT"))
        elif kind == "OBJECT":
            try:
                subcolumns = get_columns_for_type(unwrapped.get("name"), introspection_data, prefix=prefix + field_name + "_")
                columns.extend(subcolumns)
            except Exception as e:
                print(f"Skipping nested field '{field_name}': {e}")
        else:
            print(f"Skipping field '{field_name}' of kind '{kind}'")
    return columns

def create_table_for_type(type_name, introspection_data, conn):
    columns = get_columns_for_type(type_name, introspection_data)
    if not columns:
        raise ValueError(f"No columns extracted for type '{type_name}'")
    table_name = type_name.lower()
    column_defs = ", ".join([f"{col_name} {col_type}" for col_name, col_type in columns])
    create_stmt = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_defs});"
    print("Creating table with statement:")
    print(create_stmt)
    conn.execute(create_stmt)
    conn.commit()
    return columns

def flatten_dict(d, parent_key=""):
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}_{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key))
        elif isinstance(v, list):
            if all(not isinstance(i, dict) for i in v):
                items[new_key] = ", ".join(str(i) for i in v)
        else:
            items[new_key] = v
    return items

def insert_flattened_data(table_name, columns, record, conn):
    col_names = [col for col, _ in columns]
    placeholders = ", ".join("?" for _ in col_names)
    insert_stmt = f"INSERT INTO {table_name} ({', '.join(col_names)}) VALUES ({placeholders})"
    row = tuple(record.get(col) for col in col_names)
    conn.execute(insert_stmt, row)

def fetch_data(url, query):
    response = requests.post(url, json={"query": query})
    if response.status_code != 200:
        raise Exception(f"Data query failed with status {response.status_code}")
    return response.json()

def main():
    db_path = os.path.join(os.getcwd(), "countries.db")
    conn = sqlite3.connect(db_path)

    print("Fetching introspection data...")
    introspection_data = fetch_introspection(GRAPHQL_URL)
    with open("schema_metadata.json", "w") as f:
        json.dump(introspection_data, f, indent=2)

    print("Creating table for type 'Country'...")
    columns = create_table_for_type("Country", introspection_data, conn)
    table_name = "country"

    print("Fetching countries data...")
    countries_query = """
    {
      countries {
        code
        name
        native
        phone
        capital
        currency
        continent {
          code
          name
        }
        languages {
          code
          name
          native
        }
      }
    }
    """
    data = fetch_data(GRAPHQL_URL, countries_query)
    countries = data.get("data", {}).get("countries", [])
    print(f"Number of countries fetched: {len(countries)}")

    inserted = 0
    for record in countries:
        flat_record = flatten_dict(record)
        try:
            insert_flattened_data(table_name, columns, flat_record, conn)
            inserted += 1
        except Exception as e:
            print(f"Error inserting record: {e}")
    conn.commit()
    conn.close()
    print(f"Inserted {inserted} records into table '{table_name}' in database '{db_path}'.")

    # --- SQLAlchemy querying---
    engine = create_engine("sqlite:///countries.db")
    with engine.connect() as connection:
        # Query 1: Count the number of records.
        result = connection.execute(text("SELECT COUNT(*) FROM country"))
        count = result.scalar()
        print(f"\n[SQLAlchemy] Total records in table 'country': {count}")

        # Query 2: Retrieve a few sample records with a non-null capital.
        result = connection.execute(
            text("SELECT code, name, capital FROM country WHERE capital IS NOT NULL LIMIT 5")
        )
        print("\n[SQLAlchemy] Sample records (code, name, capital):")
        for row in result:
            print(row)

if __name__ == "__main__":
    main()
