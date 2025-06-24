@echo off
echo ===============================================
echo    Gofry Business System - Uruchomienie
echo ===============================================
echo.

echo Sprawdzanie Pythona...
python --version >nul 2>&1
if errorlevel 1 (
    echo BŁĄD: Python nie jest zainstalowany!
    echo Pobierz Python z: https://python.org
    pause
    exit /b 1
)

echo Instalowanie wymaganych pakietów...
pip install -r requirements.txt

echo.
echo Uruchamianie aplikacji...
echo Aplikacja będzie dostępna pod adresem: http://localhost:5000
echo.
echo Login: admin
echo Hasło: admin123
echo.
echo Aby zatrzymać aplikację, naciśnij Ctrl+C
echo.

python app.py

pause
