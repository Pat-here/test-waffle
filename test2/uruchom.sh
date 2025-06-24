#!/bin/bash

echo "==============================================="
echo "    Gofry Business System - Uruchomienie"
echo "==============================================="
echo

echo "Sprawdzanie Pythona..."
if ! command -v python3 &> /dev/null; then
    echo "BŁĄD: Python3 nie jest zainstalowany!"
    echo "Zainstaluj Python3 za pomocą menedżera pakietów"
    exit 1
fi

echo "Instalowanie wymaganych pakietów..."
pip3 install -r requirements.txt

echo
echo "Uruchamianie aplikacji..."
echo "Aplikacja będzie dostępna pod adresem: http://localhost:5000"
echo
echo "Login: admin"
echo "Hasło: admin123"
echo
echo "Aby zatrzymać aplikację, naciśnij Ctrl+C"
echo

python3 app.py
