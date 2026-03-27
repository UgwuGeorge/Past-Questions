@echo off
echo.
echo ============================================================
echo   REHARZ AI - PRODUCTION DATA POPULATOR (INTERNAL SYNC)
echo ============================================================
echo.
echo [*] Identifying active backend container...
docker-compose exec -T backend python agent_core/scripts/import_data.py

echo.
echo [*] Production Sync Complete. The database is now populated.
pause
