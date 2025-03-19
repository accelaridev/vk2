#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time
import datetime
import shutil
import webbrowser

# Hilfsfunktionen für farbige Ausgabe
def print_info(message):
    print("\033[94m[INFO]\033[0m", message)

def print_success(message):
    print("\033[92m[ERFOLG]\033[0m", message)

def print_warning(message):
    print("\033[93m[WARNUNG]\033[0m", message)

def print_error(message):
    print("\033[91m[FEHLER]\033[0m", message)

# Backend starten
def start_backend():
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
    os.chdir(backend_dir)

    # Virtuelle Umgebung
    venv_dir = os.path.join(backend_dir, 'venv')
    if not os.path.exists(venv_dir):
        print_error("Virtuelle Umgebung nicht gefunden! Bitte führen Sie die Installation erneut aus.")
        return None

    # Python-Pfad
    if os.name == 'nt':  # Windows
        python_path = os.path.join(venv_dir, 'Scripts', 'python')
    else:  # macOS/Linux
        python_path = os.path.join(venv_dir, 'bin', 'python')

    # Datenbank prüfen
    db_path = os.path.join(backend_dir, 'database.db')
    if not os.path.exists(db_path):
        print_info("SQLite-Datenbank nicht gefunden. Initialisiere...")
        subprocess.call([python_path, 'init_db.py'])

    # Flask-App starten
    print_info("Starte Flask-Backend mit SQLite...")
    flask_process = subprocess.Popen([python_path, 'app.py'])

    return flask_process

# Datenbankoperationen
def manage_database():
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')

    # Python-Pfad
    venv_dir = os.path.join(backend_dir, 'venv')
    if os.name == 'nt':  # Windows
        python_path = os.path.join(venv_dir, 'Scripts', 'python')
    else:  # macOS/Linux
        python_path = os.path.join(venv_dir, 'bin', 'python')

    menu_options = {
        "1": "Datenbank initialisieren (Neuerstellung)",
        "2": "Datenbank-Backup erstellen",
        "3": "Zurück zum Hauptmenü"
    }

    while True:
        print("\n" + "="*50)
        print("DATENBANKMANAGER")
        print("="*50)

        for key, value in menu_options.items():
            print(f"{key}. {value}")

        choice = input("\nBitte wählen Sie eine Option (1-3): ")

        if choice == "1":
            confirm = input("Dies wird die bestehende Datenbank überschreiben! Fortfahren? (j/n): ")
            if confirm.lower() == "j":
                os.chdir(backend_dir)
                subprocess.call([python_path, 'init_db.py'])
                print_success("Datenbank wurde neu initialisiert.")

        elif choice == "2":
            # Backup erstellen
            db_path = os.path.join(backend_dir, 'database.db')
            backup_dir = os.path.join(backend_dir, 'backups')
            os.makedirs(backup_dir, exist_ok=True)

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f"database_backup_{timestamp}.db")

            if os.path.exists(db_path):
                shutil.copy2(db_path, backup_path)
                print_success(f"Backup erstellt: {backup_path}")
            else:
                print_error("Datenbank nicht gefunden! Kein Backup erstellt.")

        elif choice == "3":
            break

        else:
            print_error("Ungültige Auswahl!")

        input("\nDrücken Sie Enter, um fortzufahren...")

# Hauptmenü
def main_menu():
    menu_options = {
        "1": "Anwendung starten",
        "2": "Datenbankoperationen",
        "3": "Beenden"
    }

    backend_process = None

    while True:
        print("\n" + "="*50)
        print("WEBANWENDUNG STARTMENÜ")
        print("="*50)

        # Status anzeigen
        if backend_process and backend_process.poll() is None:
            backend_status = "\033[92mLäuft\033[0m"
        else:
            backend_status = "\033[91mStopped\033[0m"

        print(f"Backend-Status: {backend_status}")
        print("-"*50)

        for key, value in menu_options.items():
            print(f"{key}. {value}")

        choice = input("\nBitte wählen Sie eine Option (1-3): ")

        if choice == "1":
            # Stoppe bestehenden Prozess
            if backend_process and backend_process.poll() is None:
                backend_process.terminate()

            # Starte neu
            backend_process = start_backend()

            # Kurz warten, damit der Server starten kann
            time.sleep(2)

            # Browser öffnen
            webbrowser.open("http://127.0.0.1:5000")

            print_info("Anwendung läuft.")
            print_info("Web-Interface ist unter http://127.0.0.1:5000 verfügbar")
            print_info("API-Endpunkte sind unter http://127.0.0.1:5000/api/* verfügbar")

        elif choice == "2":
            manage_database()

        elif choice == "3":
            # Beenden und alle Prozesse sauber terminieren
            if backend_process and backend_process.poll() is None:
                backend_process.terminate()
            print_info("Anwendung beendet.")
            break

        else:
            print_error("Ungültige Auswahl!")

if __name__ == "__main__":
    main_menu()
