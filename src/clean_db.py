from config import create_app, db
from models import (
    Material, Cliente, Mantenimiento, Proveedor, Productos,
    Pedido, ClienteProducto, TecnicoMantenimiento, MaterialMantenimiento
)

app = create_app()

def limpiar_db():
    with app.app_context():
        try:
            # Limpiar datos existentes
            db.session.query(MaterialMantenimiento).delete()
            db.session.query(Pedido).delete()
            db.session.query(ClienteProducto).delete()
            db.session.query(Material).delete()
            db.session.query(Mantenimiento).delete()
            db.session.query(TecnicoMantenimiento).delete()
            db.session.query(Productos).delete()
            db.session.query(Cliente).delete()
            db.session.query(Proveedor).delete()
            db.session.commit()
            print(f'buena mi papacho limpio la base de datos re mela')
        except Exception as e:
            db.session.rollback()
            print(f'Error al limpiar la base de datos: {str(e)}')
            
            
if __name__ == '__main__':
    limpiar_db()