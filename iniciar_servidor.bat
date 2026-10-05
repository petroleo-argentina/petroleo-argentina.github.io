@echo off
title Petroleo en Argentina - Servidor y Mapa Interactivo
echo ===================================================================
echo   PETROLEO EN ARGENTINA: DEL POZO AL PAIS
echo   Mapa Interactivo de Datos, Scrollytelling y Respuestas Clave
echo ===================================================================
echo.
echo [1/2] Abriendo el navegador en http://localhost:8000 ...
start "" http://localhost:8000

echo [2/2] Iniciando servidor FastAPI con DuckDB y datasets auditados...
cd /d "%~dp0"
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
pause
