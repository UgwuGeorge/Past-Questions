@echo off
echo.
echo ============================================================
echo   REHARZ AI - SECURE PRODUCTION SUITE (ORCHESTRATED)
echo ============================================================
echo.
echo [1/3] Building Secure Environment...
docker-compose build

echo [2/3] Initializing Hardened Services (Postgres, Nginx, Engine)...
docker-compose up -d

echo [3/3] System Online.
echo        Frontend & Secure Proxy: https://localhost
echo        Backend API Hardening: Active
echo.
echo Press any key to shutdown the secure suite...
pause
docker-compose down
echo Done.
