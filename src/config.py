import os
import secrets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Configuración de la base de datos
basedir = os.path.abspath(os.path.dirname(__file__))

# Instancias globales de SQLAlchemy y Migrate
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configuración de base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URI',
        'sqlite:///' + os.path.join(basedir, 'inventario.db')
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Secret key segura desde variable de entorno o generada
    app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(32))

    # Configuraciones adicionales de seguridad
    app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Importar modelos aquí para registrar las tablas
    with app.app_context():
        db.create_all()

    return app