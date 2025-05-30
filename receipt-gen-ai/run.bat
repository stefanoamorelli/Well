@echo off
echo 🚀 Launching Receipt Gen AI API...
echo.

REM Activate the virtual environment
call venv\Scripts\activate

REM Add the src folder to PYTHONPATH
set PYTHONPATH=%cd%\src

REM Start the API with auto-reload
uvicorn core.api.app:app --reload

pause
