@echo off
title SplitEase 2.0 — Production Server (React + Python REST + Cloud Firebase)
echo ====================================================
echo           ⚡ SplitEase 2.0 Local Web Server
echo ====================================================
echo.
echo Starting server on http://localhost:5000 ...
echo.

start http://localhost:5000

python server.py
if %errorlevel% neq 0 (
    echo.
    echo Server stopped or python error.
    pause
)
