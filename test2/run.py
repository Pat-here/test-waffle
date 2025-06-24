#!/usr/bin/env python3
"""
Gofry Business System - Alternatywny punkt uruchomienia
Używaj tego pliku jeśli app.py nie działa poprawnie
"""

import os
import sys
from app import app, db, User
from werkzeug.security import generate_password_hash

def check_requirements():
    """Sprawdza czy wszystkie wymagane pakiety są zainstalowane"""
    try:
        import flask
        import flask_sqlalchemy
        print("✓ Flask zainstalowany")
        return True
    except ImportError as e:
        print(f"✗ Brak wymaganego pakietu: {e}")
        print("Uruchom: pip install -r requirements.txt")
        return False

def setup_database():
    """Inicjalizuje bazę danych i tworzy konto administratora"""
    with app.app_context():
        # Utwórz tabele
        db.create_all()
        print("✓ Baza danych utworzona")

        # Sprawdź czy admin istnieje
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                email='admin@gofry.pl',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✓ Konto administratora utworzone")
            print("  Login: admin")
            print("  Hasło: admin123")
        else:
            print("✓ Konto administratora już istnieje")

def main():
    """Główna funkcja uruchamiająca aplikację"""
    print("=" * 50)
    print("    Gofry Business System")
    print("    Alternatywny launcher")
    print("=" * 50)

    # Sprawdź wymagania
    if not check_requirements():
        sys.exit(1)

    # Sprawdź czy jesteśmy w poprawnym katalogu
    if not os.path.exists('templates'):
        print("✗ Nie znaleziono katalogu templates")
        print("Upewnij się, że uruchamiasz skrypt z katalogu projektu")
        sys.exit(1)

    # Inicjalizuj bazę danych
    setup_database()

    print("\n" + "=" * 50)
    print("Uruchamianie serwera...")
    print("Aplikacja będzie dostępna pod: http://localhost:5000")
    print("Aby zatrzymać serwer, naciśnij Ctrl+C")
    print("=" * 50 + "\n")

    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n\nSerwer zatrzymany przez użytkownika")
    except Exception as e:
        print(f"\n\nBłąd uruchamiania serwera: {e}")
        print("Sprawdź czy port 5000 nie jest zajęty")

if __name__ == '__main__':
    main()
