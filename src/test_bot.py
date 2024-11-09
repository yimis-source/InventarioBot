from config import create_app, db
from models import (
    Material, Cliente, Mantenimiento, Proveedor, Productos, Oferta, Pedido,
    ClienteProducto, TecnicoMantenimiento, 
)
from datetime import datetime, timedelta
from bot import AutomatizationBot
import threading
import time
import logging
import random

# Configuración de logging para pruebas
logging.basicConfig(
    filename='test_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Crear la aplicación
app = create_app()

def crear_datos_prueba():
    with app.app_context():
        try:
            # Limpiar datos existentes
        
            db.session.query(Pedido).delete()
            db.session.query(Oferta).delete()
            db.session.query(ClienteProducto).delete()
            db.session.query(Material).delete()
            db.session.query(Mantenimiento).delete()
            db.session.query(TecnicoMantenimiento).delete()
            db.session.query(Productos).delete()
            db.session.query(Cliente).delete()
            db.session.query(Proveedor).delete()
            
            # Crear múltiples proveedores
            proveedores = []
            for i in range(3):
                proveedor = Proveedor(
                    nombre=f"Proveedor Test {i+1}",
                    telefono=f"123456789{i}",
                    email="empresatroll466@gmail.com"
                )
                db.session.add(proveedor)
                proveedores.append(proveedor)
            db.session.flush()
            
            # Crear múltiples productos
            productos = []
            for i in range(5):
                producto = Productos(
                    nombre=f"Producto Test {i+1}",
                    precio=100.0 * (i+1),
                    lotes=10,
                    cantidad=random.randint(5, 95)
                )
                db.session.add(producto)
                productos.append(producto)
            db.session.flush()
            
            # Crear materiales con diferentes niveles
            for i in range(6):
                cantidad_actual = random.randint(1, 30)
                material = Material(
                    nombre=f"Material Test {i+1}",
                    cantidad_actual=cantidad_actual,
                    cantidad_minima=25,
                    proveedor_id=random.choice(proveedores).id,
                    productos_id=random.choice(productos).id
                )
                db.session.add(material)
            db.session.flush()
            
            # Crear múltiples clientes
            clientes = []
            for i in range(4):
                cliente = Cliente(
                    nombre=f"Cliente Test {i+1}",
                    telefono=f"098765432{i}",
                    email="empresatroll466@gmail.com"
                )
                db.session.add(cliente)
                clientes.append(cliente)
            db.session.flush()
            
            # Crear asignaciones cliente-producto
            for cliente in clientes:
                for _ in range(2):
                    cliente_producto = ClienteProducto(
                        cliente_id=cliente.id,
                        producto_id=random.choice(productos).id,
                        cantidad_minima=random.randint(3, 8)
                    )
                    db.session.add(cliente_producto)
            
            # Crear técnicos
            tecnicos = []
            especialidades = ['Eléctrico', 'Mecánico', 'General', 'Electrónico']
            for i in range(3):
                tecnico = TecnicoMantenimiento(
                    nombre=f"Técnico Test {i+1}",
                    email="empresatroll466@gmail.com",
                    telefono=f"11223344{i}",
                    especialidad=random.choice(especialidades)
                )
                db.session.add(tecnico)
                tecnicos.append(tecnico)
            db.session.flush()
            
            # Crear varios mantenimientos con diferentes estados y fechas
            estados = ['programado', 'en_proceso', 'completado']
            fechas = [
                datetime.now().date() + timedelta(days=x) 
                for x in [-5, -2, 1, 3, 7, 14]
            ]
            
            for i, fecha in enumerate(fechas):
                mantenimiento = Mantenimiento(
                    equipo=f"Equipo Test {i+1}",
                    fecha_mantenimiento=fecha,
                    detalles=f"Mantenimiento de prueba {i+1}",
                    tecnico_id=random.choice(tecnicos).id,
                    estado=random.choice(estados)
                )
                db.session.add(mantenimiento)
                db.session.flush()
                
            
            
            # Crear ofertas de prueba
            for i, producto in enumerate(productos):
                oferta = Oferta(
                    producto_id=producto.id,
                    cliente_id=random.choice(clientes).id,
                    lotes_ofrecidos=random.randint(3, 8),
                    fecha_creacion=datetime.now() - timedelta(days=i),
                )
                db.session.add(oferta)
            
            db.session.commit()
            logging.info("Datos de prueba creados exitosamente")
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error al crear datos de prueba: {str(e)}")
            raise

def verificar_resultados():
    with app.app_context():
        try:
            # Verificar pedidos generados
            pedidos = Pedido.query.all()
            logging.info(f"\nPedidos generados: {len(pedidos)}")
            for pedido in pedidos:
                logging.info(f"- Pedido #{pedido.id}: {pedido.material.nombre} - {pedido.cantidad} unidades - Estado: {pedido.estado}")
            
            # Verificar mantenimientos procesados
            mantenimientos = Mantenimiento.query.all()
            logging.info(f"\nMantenimientos procesados: {len(mantenimientos)}")
            for mant in mantenimientos:
                logging.info(f"- {mant.equipo}: {mant.fecha_mantenimiento} - Estado: {mant.estado}")
                
            # Verificar niveles de materiales
            materiales = Material.query.all()
            logging.info("\nNiveles de materiales:")
            for material in materiales:
                logging.info(f"- {material.nombre}: {material.cantidad_actual}/{material.cantidad_minima}")
                
            # Verificar asignaciones cliente-producto
            asignaciones = ClienteProducto.query.all()
            logging.info(f"\nAsignaciones cliente-producto: {len(asignaciones)}")
            
            # Verificar ofertas
            ofertas = Oferta.query.all()
            logging.info(f"\nOfertas generadas: {len(ofertas)}")
            for oferta in ofertas:
                logging.info(f"- Oferta #{oferta.id}: {oferta.producto.nombre} - {oferta.lotes_ofrecidos} lotes")
            
            return True
            
        except Exception as e:
            logging.error(f"Error al verificar resultados: {str(e)}")
            return False

def simular_cambios_inventario():
    """Simula cambios aleatorios en el inventario para probar el sistema"""
    with app.app_context():
        try:
            materiales = Material.query.all()
            for material in materiales:
                # Simular consumo aleatorio
                consumo = random.randint(1, 5)
                if material.cantidad_actual >= consumo:
                    material.cantidad_actual -= consumo
                    logging.info(f"Simulando consumo de {consumo} unidades de {material.nombre}")
            
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error al simular cambios de inventario: {str(e)}")

def simular_ciclo_completo():
    """Ejecuta un ciclo completo de pruebas del bot"""
    try:
        # Crear datos iniciales
        crear_datos_prueba()
        
        # Inicializar el bot
        bot = AutomatizationBot()
        
        # Ejecutar ciclo de pruebas
        for _ in range(3):  # 3 ciclos de prueba
            # Simular cambios en inventario
            simular_cambios_inventario()
            
            # Ejecutar funciones del bot
            bot.check_inventory_and_create_orders()
            bot.check_and_manage_offers()
            bot.manage_maintenance_schedule()
            bot.check_system_health()
            
            # Esperar entre ciclos
            time.sleep(5)
        
        # Verificar resultados
        verificar_resultados()
        
    except Exception as e:
        logging.error(f"Error en el ciclo de pruebas: {str(e)}")
        raise

def iniciar_pruebas(duracion_prueba=60):
    """Inicia las pruebas del bot con una duración específica"""
    logging.info("Iniciando pruebas del bot...")
    
    try:
        # Ejecutar primer ciclo de pruebas
        simular_ciclo_completo()
        
        # Iniciar el bot en un hilo separado
        bot = AutomatizationBot()
        bot_thread = threading.Thread(target=bot.run)
        bot_thread.daemon = True
        bot_thread.start()
        
        # Simular actividad durante el período de prueba
        start_time = time.time()
        while time.time() - start_time < duracion_prueba:
            simular_cambios_inventario()
            time.sleep(10)
        
        logging.info("Pruebas completadas exitosamente")
        
    except Exception as e:
        logging.error(f"Error en las pruebas: {str(e)}")
        raise

if __name__ == '__main__':
    iniciar_pruebas()