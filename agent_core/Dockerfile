# Use a lightweight Python base image
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for PostgreSQL and SQLite
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Optimize for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Expose backend port
EXPOSE 8000

# Start with uvicorn (Nginx will handle SSL termination in compose if we use it there, but we can also use python main.py)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
