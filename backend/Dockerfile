FROM python:3.11-slim

# Evitar .pyc y forzar stdout sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias de compilación mínimas (para asyncpg/pgvector, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
  && rm -rf /var/lib/apt/lists/*

# Instalar dependencias del proyecto (backend)
COPY pyproject.toml ./
RUN pip install --no-cache-dir .

# Copiar código fuente
COPY src ./src
COPY db ./db

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

