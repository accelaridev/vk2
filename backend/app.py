#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_cors import CORS
from flask_bootstrap import Bootstrap5
import os
import json
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# SQLite-Datenbankeinrichtung
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
engine = create_engine(f'sqlite:///{db_path}', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Datenbankmodelle
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(String(20), default='user')

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category = Column(String(50))
    stock = Column(Integer, default=0)

class SalesData(Base):
    __tablename__ = 'sales_data'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product")
    quantity = Column(Integer, nullable=False)
    sale_date = Column(String(20), nullable=False)
    total_amount = Column(Float, nullable=False)

# Flask-App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'eine-sichere-zufällige-zeichenfolge'
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'flatly'
CORS(app)  # CORS für alle Routen aktivieren
bootstrap = Bootstrap5(app)

# Hilfsfunktionen für Templates
@app.context_processor
def utility_processor():
    def format_price(price):
        return f"{price:.2f} €"
    return dict(format_price=format_price)

# API-Routen
@app.route('/api/hello', methods=['GET'])
def api_hello():
    return jsonify({'message': 'Flask API mit SQLite ist aktiv!'})

@app.route('/api/users', methods=['GET'])
def api_get_users():
    session = Session()
    users = session.query(User).all()
    result = [
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
        for user in users
    ]
    session.close()
    return jsonify(result)

@app.route('/api/products', methods=['GET'])
def api_get_products():
    session = Session()
    products = session.query(Product).all()
    result = [
        {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'category': product.category,
            'stock': product.stock
        }
        for product in products
    ]
    session.close()
    return jsonify(result)

@app.route('/api/statistics', methods=['GET'])
def api_get_statistics():
    session = Session()

    # Anzahl der Benutzer
    user_count = session.query(User).count()

    # Anzahl der Produkte
    product_count = session.query(Product).count()

    # Gesamtwert des Inventars
    inventory_value = session.query(Product).with_entities(
        (Product.price * Product.stock).label('value')
    ).all()
    total_inventory_value = sum(item.value or 0 for item in inventory_value)

    # Anzahl der Verkäufe
    sales_count = session.query(SalesData).count()

    # Gesamtumsatz
    total_revenue = session.query(SalesData).with_entities(
        SalesData.total_amount
    ).all()
    total_revenue_value = sum(sale.total_amount for sale in total_revenue)

    result = {
        'user_count': user_count,
        'product_count': product_count,
        'total_inventory_value': total_inventory_value,
        'sales_count': sales_count,
        'total_revenue': total_revenue_value
    }

    session.close()
    return jsonify(result)

# Web-Interface Routen
@app.route('/')
def home():
    session = Session()
    stats = {
        'user_count': session.query(User).count(),
        'product_count': session.query(Product).count(),
        'sales_count': session.query(SalesData).count(),
        'total_inventory_value': sum(item.value or 0 for item in session.query(Product).with_entities(
            (Product.price * Product.stock).label('value')
        ).all()),
        'total_revenue': sum(sale.total_amount for sale in session.query(SalesData).with_entities(
            SalesData.total_amount
        ).all())
    }
    recent_users = session.query(User).order_by(User.id.desc()).limit(5).all()
    recent_products = session.query(Product).order_by(Product.id.desc()).limit(5).all()
    session.close()

    return render_template('dashboard.html', stats=stats, users=recent_users, products=recent_products)

@app.route('/users')
def users():
    session = Session()
    all_users = session.query(User).all()
    session.close()
    return render_template('users.html', users=all_users)

@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        session = Session()
        # Prüfen, ob Benutzername bereits existiert
        existing_user = session.query(User).filter_by(username=request.form['username']).first()
        if existing_user:
            flash('Benutzername existiert bereits!', 'danger')
            session.close()
            return redirect(url_for('add_user'))

        # Neuen Benutzer erstellen
        new_user = User(
            username=request.form['username'],
            email=request.form['email'],
            role=request.form['role']
        )
        session.add(new_user)
        session.commit()
        session.close()

        flash('Benutzer erfolgreich erstellt!', 'success')
        return redirect(url_for('users'))

    return render_template('add_user.html')

@app.route('/products')
def products():
    session = Session()
    all_products = session.query(Product).all()
    session.close()
    return render_template('products.html', products=all_products)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        session = Session()
        # Neues Produkt erstellen
        new_product = Product(
            name=request.form['name'],
            description=request.form['description'],
            price=float(request.form['price']),
            category=request.form['category'],
            stock=int(request.form['stock'])
        )
        session.add(new_product)
        session.commit()
        session.close()

        flash('Produkt erfolgreich erstellt!', 'success')
        return redirect(url_for('products'))

    return render_template('add_product.html')

@app.route('/db_info')
def db_info():
    session = Session()

    # Tabelleninformationen
    tables = {
        'users': {
            'count': session.query(User).count(),
            'columns': ['ID', 'Benutzername', 'E-Mail', 'Rolle']
        },
        'products': {
            'count': session.query(Product).count(),
            'columns': ['ID', 'Name', 'Beschreibung', 'Preis', 'Kategorie', 'Lagerbestand']
        },
        'sales_data': {
            'count': session.query(SalesData).count(),
            'columns': ['ID', 'Produkt-ID', 'Menge', 'Verkaufsdatum', 'Gesamtbetrag']
        }
    }

    session.close()
    return render_template('db_info.html', tables=tables)

if __name__ == '__main__':
    # Erstelle den templates-Ordner, falls er nicht existiert
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    os.makedirs(templates_dir, exist_ok=True)

    app.run(host='0.0.0.0', port=5000)
