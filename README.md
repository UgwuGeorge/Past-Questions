# Reharz: The Professional Exam Architect

Reharz is a production-grade examination simulation platform designed for high-stakes professional and academic certifications (ICAN, JAMB, WAEC, IELTS). It features expert-powered grading, adaptive practice sessions, and a proctored simulation environment.

## 🚀 Production Quick Start

To launch the full orchestrated environment (Nginx + Backend + Frontend + PostgreSQL):

1. **Configure Environment**: Ensure `.env` is populated with valid `OPENAI_API_KEY`, `JWT_SECRET_KEY`, and `PAYSTACK_SECRET_KEY`.
2. **Launch Services**:
   ```bash
   start_production.bat
   ```
   Or manually:
   ```bash
   docker-compose up --build -d
   ```
3. **Seed Data**: Populating the production database with official past questions:
   ```bash
   sync_data.bat
   ```

## 🛠 Tech Stack

- **Frontend**: React (Vite), Framer Motion, Lucide Icons, Vanilla CSS.
- **Backend**: FastAPI (Python), SQLAlchemy, JWT Auth, Httpx.
- **AI Engine**: GPT-4o powered Adaptive Learning & Essay Grading.
- **Database**: PostgreSQL (Production) / SQLite (Local Dev).
- **Proxy**: Nginx with SSL/TLS termination and security hardening.

## 🔐 Security & Monetization

- **JWT Authentication**: Secure stateless auth across all endpoints.
- **Tiered Access**: Support for `FREE`, `PREMIUM`, and `ELITE` tiers.
- **Content Gating**: Automatic restriction of professional exam content based on subscription level.
- **Payment Gateway**: Integrated Paystack Inline for real-time secure upgrades.

## 📁 Project Structure

- `agent_core/`: Python backend source, models, and Docker configuration.
- `frontend/`: React source code and build pipeline.
- `data/`: Curated reference datasets and question banks.
- `nginx.conf`: Secure reverse proxy configuration.
- `docker-compose.yml`: Production orchestration manifest.

---
© 2026 Reharz Team. Confidential & Proprietary.
