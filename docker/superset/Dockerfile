FROM apache/superset:latest

# Install netcat-openbsd
USER root
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Copy init script
COPY init_superset.sh /app/init_superset.sh

# Ensure script is executable
RUN chmod +x /app/init_superset.sh

CMD ["/app/init_superset.sh"]
