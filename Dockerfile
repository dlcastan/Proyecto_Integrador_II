# Version Python para el contenedor Docker
FROM python:3.10

# Instalo dbt para PostgreSQL
RUN pip install dbt-postgres

# Directorio de trabajo dentro del contenedor
WORKDIR /app    