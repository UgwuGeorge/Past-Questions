# Deployment Guide - AI Exam Prep Platform

This guide covers how to deploy the full-stack application (FastAPI + React + PostgreSQL) using Docker.

## Local Deployment (Docker Compose)

### Prerequisites
- Docker and Docker Compose installed.
- OpenAI API Key.

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/UgwuGeorge/Past-Questions.git
   cd Past-Questions
   ```

2. **Configure Environment**:
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=password
   POSTGRES_DB=exam_db
   ```

3. **Launch the Stack**:
   ```bash
   docker-compose up --build
   ```

4. **Access the Application**:
   - **Frontend**: http://localhost (or http://localhost:80)
   - **Backend API**: http://localhost:8000
   - **API Docs (Swagger)**: http://localhost:8000/docs

---

## Cloud Deployment

### Option 1: Railway (Easiest)
1. Connect your GitHub repository to [Railway](https://railway.app/).
2. Add a PostgreSQL database plugin in Railway.
3. Configure the environment variables in the Railway dashboard (`DATABASE_URL`, `OPENAI_API_KEY`).
4. Railway will automatically detect the `docker-compose.yml` or the Dockerfiles and deploy.

### Option 2: VPS (Universal)
1. SSH into your server.
2. Install Docker and Docker Compose.
3. Follow the **Local Deployment** steps above.
4. Use a reverse proxy like Nginx or Traefik if you need SSL/TLS (HTTPS).

## Maintenance

### Updating the Application
To deploy updates:
```bash
git pull origin main
docker-compose up --build -d
```

### Checking Logs
```bash
docker-compose logs -f
```
