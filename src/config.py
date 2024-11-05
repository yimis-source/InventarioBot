import os
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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'inventario.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'supersecretkey'
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Importar modelos aquí para registrar las tablas
    with app.app_context():
        db.create_all()

    return app