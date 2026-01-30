FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias mínimas para el MCP
COPY pyproject.toml ./
RUN pip install --no-cache-dir .

# Copiar código del servidor MCP
COPY src ./src

EXPOSE 8080

# Ejecutar servidor MCP (el transporte se define via MCP_TRANSPORT env var)
CMD ["python", "src/server.py"]

