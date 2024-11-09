import os
from datetime import datetime, timedelta
import logging
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from config import create_app, db
from models import (
    Material, Cliente, Mantenimiento, Oferta, Proveedor, Productos,
    Pedido, ClienteProducto, TecnicoMantenimiento, 
)

logging.basicConfig(
    filename='bot_automatization.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class AutomatizationBot:
    def __init__(self):
        self.app = create_app()
        self.email = os.getenv('EMAIL_USER', 'empresatroll466@gmail.com')
        self.password = os.getenv('EMAIL_PASSWORD', 'xjps xhrb nbni plue')
        
    def send_email(self, subject, body, to_email):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            logging.info(f"Email enviado exitosamente a {to_email}")
            return True
        except Exception as e:
            logging.error(f"Error enviando email: {str(e)}")
            return False

    def check_inventory_and_create_orders(self):
        """Revisa inventario y crea pedidos automáticos"""
        with self.app.app_context():
            try:
                # Revisar materiales bajo mínimos
                materiales_bajos = Material.query.filter(
                    Material.cantidad_actual < Material.cantidad_minima
                ).all()
                
                for material in materiales_bajos:
                    # Verificar si no hay pedidos pendientes
                    pedido_pendiente = Pedido.query.filter_by(
                        material_id=material.id,
                        estado='pendiente'
                    ).first()
                    
                    if not pedido_pendiente:
                        # Calcular cantidad óptima de pedido
                        cantidad_pedido = (material.cantidad_minima - material.cantidad_actual) * 1.5
                        
                        nuevo_pedido = Pedido(
                            material_id=material.id,
                            proveedor_id=material.proveedor_id,
                            cantidad=int(cantidad_pedido),
                            estado='pendiente'
                        )
                        db.session.add(nuevo_pedido)
                        
                        # Notificar al proveedor
                        mensaje = f"""
                        Pedido Automático - {material.nombre}
                        Cantidad: {int(cantidad_pedido)}
                        Nivel actual: {material.cantidad_actual}
                        Nivel mínimo: {material.cantidad_minima}
                        """
                        self.send_email(
                            "Nuevo Pedido Automático",
                            mensaje,
                            material.proveedor_rel.email
                        )
                
                db.session.commit()
                logging.info("Revisión de inventario completada")
                
            except Exception as e:
                logging.error(f"Error en revisión de inventario: {str(e)}")
                db.session.rollback()

    def check_and_manage_offers(self):
        with self.app.app_context():
            try:
                fecha_actual = datetime.now()
            
                # Revisar ofertas activas que no han sido notificadas
                ofertas = Oferta.query.all()
                for oferta in ofertas:
                    producto = oferta.producto
                    cliente = oferta.cliente
                
                    # Verificar si hay suficientes lotes disponibles
                    lotes_disponibles = producto.cantidad_lotes
                    if lotes_disponibles >= oferta.lotes_ofrecidos:
                        # Notificar al cliente sobre la disponibilidad
                        mensaje = f"""
                        Oferta Disponible - {producto.nombre}
                    
                        Estimado/a {cliente.nombre},
                    
                        Los lotes que solicitó están disponibles:
                        - Producto: {producto.nombre}
                        - Lotes solicitados: {oferta.lotes_ofrecidos}
                        - Precio por unidad: ${producto.precio}
                        - Total unidades: {oferta.lotes_ofrecidos * producto.lotes}
                    
                        Por favor, contáctenos para confirmar la compra.
                        """
                        if self.send_email(
                            f"Oferta Disponible - {producto.nombre}",
                            mensaje,
                            cliente.email
                        ):
                            logging.info(f"Notificación de oferta enviada a {cliente.email} para {producto.nombre}")
                
                    # Verificar ofertas próximas a vencer (7 días desde creación)
                    dias_activa = (fecha_actual - oferta.fecha_creacion).days
                    if dias_activa >= 7:
                        mensaje_expiracion = f"""
                        Recordatorio de Oferta - {producto.nombre}
                    
                        Estimado/a {cliente.nombre},
                    
                        Le recordamos que tiene una oferta pendiente:
                        - Producto: {producto.nombre}
                        - Lotes ofrecidos: {oferta.lotes_ofrecidos}
                        - Fecha de creación: {oferta.fecha_creacion.strftime('%Y-%m-%d')}
                    
                        Por favor, contáctenos si aún está interesado/a.
                        """
                        if self.send_email(
                            f"Recordatorio de Oferta - {producto.nombre}",
                            mensaje_expiracion,
                            cliente.email
                        ):
                            logging.info(f"Recordatorio de oferta enviado a {cliente.email} para {producto.nombre}")
            
                db.session.commit()
                logging.info("Gestión de ofertas completada")
            
            except Exception as e:
                logging.error(f"Error en gestión de ofertas: {str(e)}")
                db.session.rollback()
                
    def manage_maintenance_schedule(self):
        """Gestiona programación y seguimiento de mantenimientos"""
        with self.app.app_context():
            try:
                fecha_actual = datetime.now()
                
                # Mantenimientos próximos (7 días)
                proximos = Mantenimiento.query.filter(
                    Mantenimiento.fecha_mantenimiento.between(
                        fecha_actual.date(),
                        (fecha_actual + timedelta(days=7)).date()
                    ),
                    Mantenimiento.estado == 'programado'
                ).all()
                
                for mantenimiento in proximos:
                    # Notificar al técnico si está asignado
                    if mantenimiento.tecnico:
                        mensaje = f"""
                        Mantenimiento Programado - {mantenimiento.equipo}
                        Fecha: {mantenimiento.fecha_mantenimiento}
                        Detalles: {mantenimiento.detalles}
                        """
                        self.send_email(
                            f"Próximo Mantenimiento - {mantenimiento.equipo}",
                            mensaje,
                            mantenimiento.tecnico.email
                        )
                
                db.session.commit()
                logging.info("Gestión de mantenimientos completada")
                
            except Exception as e:
                logging.error(f"Error en gestión de mantenimientos: {str(e)}")
                db.session.rollback()

    def check_system_health(self):
        """Verifica el estado general del sistema"""
        with self.app.app_context():
            try:
                # Verificar conexión a DB
                db.session.execute('SELECT 1')
                
                # Verificar tablas críticas
                tables = [Material, Cliente, Productos, Proveedor, Mantenimiento]
                for table in tables:
                    count = table.query.count()
                    logging.info(f"Tabla {table.__tablename__}: {count} registros")
                
                # Verificar servicio de email
                test_result = self.send_email(
                    "Test de Sistema",
                    "Verificación automática de sistema",
                    self.email
                )
                
                if test_result:
                    logging.info("Verificación de sistema completada exitosamente")
                else:
                    logging.warning("Problemas con el servicio de email")
                    
            except Exception as e:
                logging.error(f"Error en verificación de sistema: {str(e)}")
                return False
            
            return True

    def run(self):
        """Ejecuta el ciclo principal del bot"""
        logging.info("Iniciando bot de automatización")
        
        while True:
            try:
                # Verificar estado del sistema cada hora
                if datetime.now().minute == 0:
                    self.check_system_health()
                
                # Revisar inventario y crear pedidos
                self.check_inventory_and_create_orders()
                
                # Revisar productos y notificar clientes
                self.check_and_manage_offers()
                
                # Gestionar mantenimientos
                self.manage_maintenance_schedule()
                
                # Esperar antes del siguiente ciclo
                time.sleep(60)  # 1 minuto entre ciclos
                
            except Exception as e:
                logging.error(f"Error en ciclo principal: {str(e)}")
                time.sleep(60)  # 1 minuto si hay error

if __name__ == '__main__':
    bot = AutomatizationBot()
    bot.run()