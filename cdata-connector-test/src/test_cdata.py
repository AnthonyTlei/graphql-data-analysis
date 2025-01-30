import cdata.graphql as graphql
import pandas as pd
from sqlalchemy import create_engine

# Define GraphQL API endpoint
GRAPHQL_ENDPOINT = "https://countries.trevorblades.com/"

# Create CData SQLAlchemy connection
engine = create_engine(f"graphql://?URL={GRAPHQL_ENDPOINT}")

# Query
query = "SELECT capital, code, continent_name FROM countries WHERE continent_name = 'Africa'"

# Execute the query and fetch results
df = pd.read_sql(query, con=engine)

# Display the DataFrame
print(df)
