# Webanwendung mit Flask und SQLite

## Übersicht
Diese Webanwendung besteht aus einem Flask-Backend mit SQLite-Datenbank. Sie bietet eine vollständige Benutzeroberfläche und eine RESTful API für Datenzugriff.

## Funktionen
- **Webbasierte Benutzeroberfläche**: Zugriff über den Browser
- **RESTful API**: Für Integrationen mit anderen Anwendungen
- **SQLite-Datenbank**: Persistente Datenspeicherung ohne separate Datenbankinstallation
- **Bootstrap UI**: Moderne, responsive Benutzeroberfläche

## Starten der Anwendung
1. Doppelklicken Sie auf die Desktop-Verknüpfung **"Webanwendung Starten"**
2. Oder führen Sie das Startskript direkt aus:
   ```
   python start_app.py
   ```
3. Wählen Sie Option 1 im Menü, um die Anwendung zu starten
4. Ein Browser-Fenster öffnet sich automatisch mit der Anwendung

## Zugriff auf die Anwendung
- **Web-Interface**: http://127.0.0.1:5000
- **API-Endpunkte**: http://127.0.0.1:5000/api/*

## Verfügbare API-Endpunkte
- `/api/hello` - Test-Endpunkt
- `/api/users` - Liste aller Benutzer
- `/api/products` - Liste aller Produkte
- `/api/statistics` - Anwendungsstatistiken

## Datenbankmanagement
1. Starten Sie die Anwendung mit `python start_app.py`
2. Wählen Sie Option 2 (Datenbankoperationen)
3. Folgen Sie den Anweisungen im Menü für:
   - Datenbank-Initialisierung (Zurücksetzen)
   - Datenbank-Backup erstellen

## Projektstruktur
```
Webanwendung/
├── backend/
│   ├── venv/              # Virtuelle Python-Umgebung
│   ├── app.py             # Flask-Anwendung
│   ├── init_db.py         # Datenbank-Initialisierungsskript
│   ├── database.db        # SQLite-Datenbank
│   ├── templates/         # HTML-Templates
│   └── backups/           # Datenbankbackups
└── start_app.py           # Startskript
```

## Technologien
- **Backend**: Flask, SQLAlchemy
- **Datenbank**: SQLite
- **Frontend**: Bootstrap5, Jinja2-Templates
- **Paketmanagement**: Python venv
