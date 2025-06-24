# Gofry Business System

Kompletny system zarządzania biznesem dla budki z goframi w Szklarskiej Porębie.

## ✨ Funkcjonalności

### 🔐 System logowania
- Bezpieczny dostęp z jednym kontem administratora
- Domyślne dane: `admin` / `admin123`

### 📊 Dashboard
- Przegląd kluczowych statystyk
- Szybkie akcje
- Status dnia

### 📝 Notatki
- Dodawanie, edycja i usuwanie notatek
- System priorytetów (niski, średni, wysoki)
- Kolorowe oznaczenia

### 🛒 Zamówienia
- Lista zamówień do dostawców
- Wielopozycyjne zamówienia
- Status: oczekujące, zamówione, dostarczone
- Automatyczne obliczanie kosztów

### ⏰ Czas pracy
- Rejestracja czasu pracy pracowników
- Automatyczne obliczanie wypłat
- Statystyki miesięczne
- Uwzględnienie przerw

### 📈 Raporty dzienne
- Obrót, koszty, zysk
- Liczba sprzedanych gofrów
- Warunki pogodowe
- Automatyczne podsumowania miesięczne

## 🚀 Uruchomienie

### Windows
1. Kliknij dwukrotnie na `uruchom.bat`
2. Aplikacja zainstaluje zależności i wystartuje
3. Otwórz http://localhost:5000

### Linux/Mac
```bash
./uruchom.sh
```

### Ręczne uruchomienie
```bash
pip install -r requirements.txt
python app.py
```

## 🌐 Deployment na Render

### Przygotowanie
1. Utwórz konto na [render.com](https://render.com)
2. Połącz z GitHub/GitLab
3. Wgraj pliki projektu do repozytorium

### Konfiguracja
1. Utwórz nowy "Web Service"
2. Wybierz repozytorium
3. Ustawienia:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: `Python 3`

### Zmienne środowiskowe
```
PYTHON_VERSION=3.11.0
```

### Baza danych
Render automatycznie utworzy SQLite, ale dla produkcji zaleca się PostgreSQL:
1. Dodaj PostgreSQL database w Render
2. Zmień `SQLALCHEMY_DATABASE_URI` w app.py

## 📁 Struktura projektu

```
gofry_biznes_system/
├── app.py                 # Główny backend Flask
├── requirements.txt       # Zależności Python
├── render.yaml           # Konfiguracja Render
├── Procfile              # Backup dla Heroku
├── uruchom.bat           # Skrypt Windows
├── uruchom.sh            # Skrypt Linux/Mac
├── static/
│   ├── css/
│   │   └── style.css     # Style aplikacji
│   └── js/
│       ├── main.js       # Główny JavaScript
│       ├── notes.js      # Logika notatek
│       ├── orders.js     # Logika zamówień
│       ├── work_hours.js # Logika czasu pracy
│       └── reports.js    # Logika raportów
└── templates/
    ├── layout.html       # Główny szablon
    ├── auth/
    │   └── login.html    # Strona logowania
    └── dashboard/
        ├── index.html    # Dashboard główny
        ├── notes.html    # Strona notatek
        ├── orders.html   # Strona zamówień
        ├── work_hours.html # Czas pracy
        └── reports.html  # Raporty
```

## 🔧 Dane początkowe

### Administrator
- **Login**: admin
- **Hasło**: admin123

### Kategorie dodatków
- Podstawowe (zielone)
- Premium (czerwone)  
- Owocowe (żółte)
- Specjalne (fioletowe)

### Dodatki z cenami
System zawiera wszystkie dodatki z poprzednich analiz:
- Oreo pokruszone: 4,40 zł za opakowanie
- Kinder Bueno: 76,50 zł za opakowanie
- Nutella: 18,00 zł za słoik
- Wszystkie sosy i posypki

## 🛠️ Rozszerzenia systemu

### Możliwe usprawnienia
1. **Integracja z kasą fiskalną**
2. **System powiadomień SMS/Email**
3. **Aplikacja mobilna**
4. **Zarządzanie zapasami**
5. **Program lojalnościowy**
6. **Analiza sprzedaży AI**

### API Endpoints
- `/api/notes` - Zarządzanie notatkami
- `/api/orders` - Zarządzanie zamówieniami  
- `/api/work-hours` - Czas pracy
- `/api/reports` - Raporty dzienne
- `/api/monthly-summary` - Podsumowania miesięczne

## 🎯 Optymalizacja biznesu

### Kluczowe wskaźniki
- **Średnia marża**: 72%
- **Najrentowniejszy dodatek**: Cukier puder (98% marży)
- **Optymalna cena kompozycji**: 19-24 zł
- **Koszt wykonania gofra**: 2,66 zł

### Rekomendacje
1. Promuj dodatki z wysoką marżą
2. Monitoruj pogodę vs sprzedaż
3. Optymalizuj godziny pracy
4. Analizuj miesięczne trendy

## 📞 Wsparcie

W przypadku problemów sprawdź:
1. Czy Python jest zainstalowany
2. Czy port 5000 jest wolny
3. Czy wszystkie pliki są w miejscu
4. Logi błędów w konsoli

System został zaprojektowany specjalnie dla budki z goframi przy ul. Kilińskiego 21 w Szklarskiej Porębie, przy wejściu na żółty szlak turystyczny.

**Powodzenia w biznesie! 🧇**
