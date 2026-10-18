# ==============================================================================
# Drishti — Multi-Stage Production Container (Unified Frontend + Backend Core)
# ==============================================================================

# Stage 1: Build React / Vite Frontend Single Page Application
FROM node:20-alpine AS frontend-builder
WORKDIR /app/web
COPY web/package.json web/package-lock.json ./
RUN npm ci
COPY web/ ./
ENV VITE_API_BASE=""
RUN npm run build

# Stage 2: Production Python Backend Runtime
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY backend/ ./backend/
COPY agents/ ./agents/
COPY simulator/ ./simulator/
COPY eval/ ./eval/
COPY assets/ ./assets/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Copy compiled frontend distribution from Stage 1
COPY --from=frontend-builder /app/web/dist ./web/dist

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
