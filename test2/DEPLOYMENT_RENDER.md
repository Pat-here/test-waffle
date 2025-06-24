# Deployment na Render.com - Instrukcja

## 🚀 Bezpłatne hostowanie aplikacji na Render

### Krok 1: Przygotowanie repozytorium
1. Utwórz konto na [GitHub](https://github.com) jeśli nie masz
2. Utwórz nowe repozytorium o nazwie `gofry-business-system`
3. Wgraj wszystkie pliki projektu do repozytorium

### Krok 2: Rejestracja na Render
1. Idź na [render.com](https://render.com)
2. Zarejestruj się używając konta GitHub
3. Połącz Render z Twoim kontem GitHub

### Krok 3: Utworzenie Web Service
1. Kliknij "New +" → "Web Service"
2. Wybierz repozytorium `gofry-business-system`
3. Wypełnij ustawienia:

```
Name: gofry-business-system
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

### Krok 4: Ustawienia zmiennych środowiskowych
W sekcji "Environment Variables" dodaj:

```
PYTHON_VERSION: 3.11.0
SECRET_KEY: twoj-super-sekretny-klucz-2025-render
```

### Krok 5: Deploy
1. Kliknij "Create Web Service"
2. Render automatycznie zbuduje i wdroży aplikację
3. Po 2-3 minutach otrzymasz link do aplikacji

### Krok 6: Testowanie
1. Otwórz link do aplikacji (np. https://gofry-business-system.onrender.com)
2. Zaloguj się jako: `admin` / `admin123`
3. Sprawdź wszystkie funkcjonalności

## 🎯 Optymalizacje dla produkcji

### Bezpieczeństwo
Zmień domyślne hasło administratora po pierwszym logowaniu!

### Baza danych
Render udostępnia SQLite, ale dla większej skalowalności rozważ PostgreSQL:
1. Dodaj PostgreSQL database w Render
2. Zmień connection string w app.py

### Backup
Regularnie pobieraj kopie zapasowe bazy danych z panelu Render.

### Custom Domain
W ustawieniach Web Service możesz dodać własną domenę.

## 🔧 Rozwiązywanie problemów

### Błąd podczas budowania
- Sprawdź logi w zakładce "Logs"
- Upewnij się że requirements.txt jest poprawny

### Aplikacja nie startuje
- Sprawdź czy Start Command to `gunicorn app:app`
- Sprawdź logi uruchomienia

### Błędy bazy danych
- Render automatycznie tworzy SQLite
- Sprawdź czy modele są poprawnie zdefiniowane

## 📞 Wsparcie
- Dokumentacja Render: https://render.com/docs
- Community Forum: https://community.render.com

**Twoja aplikacja będzie dostępna 24/7 za darmo!** 🎉
