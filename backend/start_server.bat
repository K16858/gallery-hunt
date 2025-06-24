@echo off
echo Museum Quiz API サーバーを起動しています...
cd /d "%~dp0"
uvicorn server:app --reload --host 0.0.0.0 --port 8000
pause
