#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import Base, engine, Session, User, Product, SalesData
import os

def init_db():
    # Datenbank erstellen, falls sie nicht existiert
    if os.path.exists('database.db'):
        print("Lösche bestehende Datenbank...")
        os.remove('database.db')

    # Tabellen erstellen
    print("Erstelle Datenbanktabellen...")
    Base.metadata.create_all(engine)

    # Beispieldaten einfügen
    print("Füge Beispieldaten ein...")
    session = Session()

    # Benutzer
    users = [
        User(username="admin", email="admin@example.com", role="admin"),
        User(username="user1", email="user1@example.com", role="user"),
        User(username="user2", email="user2@example.com", role="user"),
        User(username="manager", email="manager@example.com", role="manager")
    ]

    # Produkte
    products = [
        Product(name="Laptop", description="Leistungsstarker Laptop für Büroarbeiten", 
                price=999.99, category="Elektronik", stock=15),
        Product(name="Smartphone", description="Neuestes Smartphone-Modell mit Kamera", 
                price=699.99, category="Elektronik", stock=25),
        Product(name="Kopfhörer", description="Kabellose Kopfhörer mit Geräuschunterdrückung", 
                price=129.99, category="Audio", stock=50),
        Product(name="Monitor", description="27-Zoll 4K-Display", 
                price=349.99, category="Elektronik", stock=10),
        Product(name="Tastatur", description="Mechanische Gaming-Tastatur", 
                price=89.99, category="Peripherie", stock=30),
        Product(name="Maus", description="Ergonomische Maus", 
                price=49.99, category="Peripherie", stock=40)
    ]

    # Verkaufsdaten
    sales_data = [
        SalesData(product_id=1, quantity=3, sale_date="2023-10-15", total_amount=2999.97),
        SalesData(product_id=2, quantity=5, sale_date="2023-10-16", total_amount=3499.95),
        SalesData(product_id=3, quantity=10, sale_date="2023-10-17", total_amount=1299.90),
        SalesData(product_id=4, quantity=2, sale_date="2023-10-18", total_amount=699.98),
        SalesData(product_id=1, quantity=1, sale_date="2023-10-19", total_amount=999.99),
        SalesData(product_id=5, quantity=7, sale_date="2023-10-20", total_amount=629.93),
        SalesData(product_id=6, quantity=12, sale_date="2023-10-21", total_amount=599.88),
        SalesData(product_id=2, quantity=3, sale_date="2023-10-22", total_amount=2099.97)
    ]

    # Daten zur Sitzung hinzufügen
    session.add_all(users)
    session.add_all(products)

    # Änderungen bestätigen, um IDs zu generieren
    session.commit()

    # Verkaufsdaten hinzufügen
    for sale in sales_data:
        session.add(sale)

    # Finale Bestätigung
    session.commit()
    session.close()

    print("Datenbankinitialisierung abgeschlossen.")

if __name__ == "__main__":
    init_db()
