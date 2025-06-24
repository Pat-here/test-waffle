#!/usr/bin/env python3
"""
Gofry Business System - Inicjalizacja danych przykładowych
Uruchom ten skrypt po pierwszym starcie aplikacji aby dodać przykładowe dane
"""

from app import app, db, Kategorie, Dodatki, KosztyWykonania, Gofry, Kompozycje, KompozycjeDodatki
import sys

def init_sample_data():
    """Dodaje przykładowe dane do bazy"""
    with app.app_context():
        print("Dodawanie przykładowych danych...")

        # Sprawdź czy dane już istnieją
        if Kategorie.query.count() > 0:
            print("✓ Dane już istnieją w bazie")
            return

        # Kategorie
        kategorie = [
            Kategorie(nazwa="Podstawowe", kolor="#28a745"),
            Kategorie(nazwa="Premium", kolor="#dc3545"), 
            Kategorie(nazwa="Owocowe", kolor="#ffc107"),
            Kategorie(nazwa="Specjalne", kolor="#6f42c1")
        ]

        for kat in kategorie:
            db.session.add(kat)
        db.session.commit()
        print("✓ Kategorie dodane")

        # Dodatki z prawdziwymi cenami
        dodatki_data = [
            # Podstawowe
            ("Cukier puder", 1, 4.00, "kg", 5, 1.00),
            ("Posypka kolorowa", 1, 4.50, "g", 5, 2.00),
            ("Sos czekoladowy", 1, 27.00, "kg", 25, 2.50),
            ("Sos karmelowy", 1, 25.00, "kg", 25, 2.50),
            ("Sos truskawkowy", 1, 24.00, "kg", 25, 2.50),

            # Premium
            ("Oreo pokruszone", 2, 4.40, "g", 20, 3.50),
            ("Kinder Bueno pokruszone", 2, 76.50, "g", 15, 4.00),
            ("Bita śmietana", 2, 24.00, "ml", 50, 4.00),
            ("Wiórki kokosowe", 2, 6.55, "g", 10, 2.00),

            # Owocowe
            ("Truskawki świeże", 3, 18.50, "kg", 100, 4.50),
            ("Maliny świeże", 3, 22.00, "kg", 50, 4.50),
            ("Banany", 3, 5.50, "kg", 50, 2.00),

            # Specjalne
            ("Nutella", 4, 18.00, "g", 30, 5.00),
            ("Pasta pistacjowa", 4, 37.00, "g", 30, 7.50),
            ("Raffaello", 4, 11.70, "g", 30, 5.00),
            ("Masło orzechowe", 4, 12.99, "g", 20, 3.50)
        ]

        for nazwa, kat_id, koszt_op, jednostka, porcja, cena in dodatki_data:
            # Oblicz koszt porcyjny
            if jednostka == "kg":
                koszt_porcyjny = (koszt_op / 1000) * porcja
            else:
                koszt_porcyjny = (koszt_op / 100) * porcja if jednostka == "g" else (koszt_op / 1000) * porcja

            # Oblicz marżę
            marza = ((cena - koszt_porcyjny) / cena) * 100 if cena > 0 else 0

            dodatek = Dodatki(
                nazwa=nazwa,
                kategoria_id=kat_id,
                koszt_opakowania=koszt_op,
                jednostka=jednostka,
                porcja=porcja,
                koszt_porcyjny=koszt_porcyjny,
                cena_sprzedazy=cena,
                marza=round(marza, 1)
            )
            db.session.add(dodatek)

        db.session.commit()
        print("✓ Dodatki dodane")

        # Koszty wykonania
        koszt_wykonania = KosztyWykonania(
            nazwa="Standard",
            koszt_mieszanki_kg=12.0,
            zuzycie_mieszanki_g=80.0,
            koszt_energii=0.15,
            koszt_gazu=0.05,
            koszt_pracy=1.50,
            koszt_calkowity=2.66
        )
        db.session.add(koszt_wykonania)
        db.session.commit()
        print("✓ Koszty wykonania dodane")

        # Gofry bazowe
        gofry = [
            Gofry(nazwa="Gofr suchy", cena_sprzedazy=10.00, koszt_wykonania_id=1, koszt_calkowity=2.66, marza=73.4),
            Gofry(nazwa="Gofr z cukrem pudrem", cena_sprzedazy=11.00, koszt_wykonania_id=1, koszt_calkowity=2.68, marza=75.6)
        ]

        for gofr in gofry:
            db.session.add(gofr)
        db.session.commit()
        print("✓ Gofry bazowe dodane")

        # Kompozycje
        kompozycje_data = [
            ("OREO DREAMS", 1, 20.00),
            ("KINDER PARADISE", 1, 23.00),
            ("NUTELLA CLASSIC", 1, 21.50),
            ("FRUIT DELIGHT", 1, 21.00),
            ("CARAMEL DREAM", 1, 20.50),
            ("DOUBLE CHOCO", 1, 21.00),
            ("SUMMER FRESH", 1, 19.00),
            ("PREMIUM MIX", 1, 24.00)
        ]

        for nazwa, gofr_id, cena in kompozycje_data:
            kompozycja = Kompozycje(
                nazwa=nazwa,
                gofr_id=gofr_id,
                cena_sprzedazy=cena,
                koszt_surowcow=5.0,  # Przykładowa wartość
                marza=75.0  # Przykładowa wartość
            )
            db.session.add(kompozycja)

        db.session.commit()
        print("✓ Kompozycje dodane")

        print("\n🎉 Wszystkie przykładowe dane zostały dodane!")
        print("Możesz teraz uruchomić aplikację i zalogować się jako admin/admin123")

if __name__ == '__main__':
    init_sample_data()
