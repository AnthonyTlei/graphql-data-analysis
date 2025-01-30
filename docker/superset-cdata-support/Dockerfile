FROM apache/superset:latest

# Install necessary dependencies
USER root
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Copy and install CData GraphQL Connector inside the Superset container
COPY cdata-graphql-connector-24.0.9111-python3.tar.gz /app/
RUN pip install /app/cdata-graphql-connector-24.0.9111-python3.tar.gz

# Copy the initialization script
COPY init_superset.sh /app/init_superset.sh

# Set Python path for custom configuration
ENV PYTHONPATH="/app/pythonpath:$PYTHONPATH"

CMD ["/app/init_superset.sh"]
