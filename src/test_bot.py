from config import create_app, db
from models import (
    Material, Cliente, Mantenimiento, Proveedor, Productos,
    Pedido, ClienteProducto, TecnicoMantenimiento, MaterialMantenimiento
)
from datetime import datetime, timedelta
from bot import bot_automatizacion
import threading
import time

# Crear la aplicación
app = create_app()

def crear_datos_prueba():
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
            
            # Crear proveedor de prueba
            proveedor = Proveedor(
                nombre="Proveedor Test",
                telefono="1234567890",
                email="empresatroll466@gmail.com"
            )
            db.session.add(proveedor)
            db.session.flush()  # Para obtener el ID generado
            
            # Crear producto de prueba
            producto = Productos(
                nombre="Producto Test",
                precio=100.0,
                lotes=10,
                cantidad=95
            )
            db.session.add(producto)
            db.session.flush()  # Para obtener el ID generado
            
            # Crear material con nivel bajo
            material = Material(
                nombre="Material Test",
                cantidad_actual=5,
                cantidad_minima=20,
                proveedor_id=proveedor.id,
                productos_id=producto.id
            )
            db.session.add(material)
            db.session.flush()
            
            # Crear cliente
            cliente = Cliente(
                nombre="Cliente Test",
                telefono="0987654321",
                email="empresatroll466@gmail.com"
            )
            db.session.add(cliente)
            db.session.flush()
            
            # Crear asignación cliente-producto
            cliente_producto = ClienteProducto(
                cliente_id=cliente.id,
                producto_id=producto.id,
                cantidad_minima=5
            )
            db.session.add(cliente_producto)
            
            # Crear técnico
            tecnico = TecnicoMantenimiento(
                nombre="Técnico Test",
                email="empresatroll466@gmail.com",
                telefono="1122334455",
                especialidad="General"
            )
            db.session.add(tecnico)
            db.session.flush()
            
            # Crear mantenimientos
            # Uno próximo
            mant_proximo = Mantenimiento(
                equipo="Equipo Test 1",
                fecha_mantenimiento=datetime.now().date() + timedelta(days=2),
                detalles="Mantenimiento de prueba próximo",
                tecnico_id=tecnico.id
            )
            db.session.add(mant_proximo)
            db.session.flush()
            
            # Uno vencido
            mant_vencido = Mantenimiento(
                equipo="Equipo Test 2",
                fecha_mantenimiento=datetime.now().date() - timedelta(days=2),
                detalles="Mantenimiento de prueba vencido",
                tecnico_id=tecnico.id
            )
            db.session.add(mant_vencido)
            db.session.flush()
            
            # Crear requerimiento de material para mantenimiento
            material_mant = MaterialMantenimiento(
                material_id=material.id,
                mantenimiento_id=mant_proximo.id,
                cantidad_requerida=10
            )
            db.session.add(material_mant)
            
            db.session.commit()
            print("Datos de prueba creados exitosamente")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear datos de prueba: {str(e)}")
            raise

def iniciar_pruebas():
    print("Iniciando pruebas del bot...")
    
    # Crear datos de prueba
    crear_datos_prueba()
    
    # Iniciar el bot en un hilo separado
    bot_thread = threading.Thread(target=bot_automatizacion)
    bot_thread.daemon = True
    bot_thread.start()
    
    print("Bot iniciado. Ejecutando durante 30 segundos para ver resultados...")
    time.sleep(30)
    
    print("\nVerificando resultados...")
    with app.app_context():
        # Verificar pedidos generados
        pedidos = Pedido.query.all()
        print(f"\nPedidos generados: {len(pedidos)}")
        for pedido in pedidos:
            print(f"- Pedido #{pedido.id} para {pedido.material.nombre}: {pedido.cantidad} unidades")
        
        # Verificar mantenimientos procesados
        mantenimientos = Mantenimiento.query.all()
        print(f"\nMantenimientos procesados: {len(mantenimientos)}")
        for mant in mantenimientos:
            print(f"- {mant.equipo}: {mant.fecha_mantenimiento} ({mant.estado})")

if __name__ == '__main__':
    iniciar_pruebas()