import os
from config import create_app, db
from models import (
    Material, Cliente, Mantenimiento, Proveedor, Productos,
    Pedido, ClienteProducto, TecnicoMantenimiento, MaterialMantenimiento
)
import time
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

# Crear la aplicación
app = create_app()

# Configuración de logging
logging.basicConfig(
    filename='bot_debug.log',
    level=logging.DEBUG,  # Cambiado a DEBUG para más detalle
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configuración de email desde variables de entorno
EMAIL = os.getenv('EMAIL_USER', 'empresatroll466@gmail.com')
PASSWORD = os.getenv('EMAIL_PASSWORD', 'xjps xhrb nbni plue')

def send_notification(subject, body, to_email, to_phone=None):
    """Función unificada para enviar notificaciones por email y SMS"""
    # Intentar enviar email
    success_email = send_email(subject, body, to_email)   
    
    return success_email 


def send_email(subject, body, to_email):
    """Función de envío de email con mejor manejo de errores"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
        logging.info(f"Correo enviado exitosamente a {to_email}")
        return True
    except smtplib.SMTPAuthenticationError as e:
        logging.error(f"Error de autenticación SMTP: {e}")
        return False
    except Exception as e:
        logging.error(f"Error al enviar correo: {str(e)}")
        return False

def generar_pedido_automatico(material):
    """Versión mejorada de generación de pedidos con mejor logging"""
    try:
        logging.info(f"Intentando generar pedido para material: {material.nombre}")
        logging.info(f"Cantidad actual: {material.cantidad_actual}, Mínima: {material.cantidad_minima}")
        
        cantidad_pedido = int((material.cantidad_minima - material.cantidad_actual) * 1.5)
        
        # Verificar si ya existe un pedido pendiente
        pedido_existente = Pedido.query.filter_by(
            material_id=material.id,
            estado='pendiente'
        ).first()
        
        if pedido_existente:
            logging.info(f"Ya existe un pedido pendiente para {material.nombre}")
            return None
            
        nuevo_pedido = Pedido(
            material_id=material.id,
            proveedor_id=material.proveedor_id,
            cantidad=cantidad_pedido,
            estado='pendiente'
        )
        
        db.session.add(nuevo_pedido)
        db.session.commit()
        
        logging.info(f"Pedido #{nuevo_pedido.id} generado exitosamente")
        
        # Intentar notificar al proveedor, pero no revertir si falla
        mensaje = f"""
        Pedido Automático - {material.nombre}
        Cantidad requerida: {cantidad_pedido}
        Nivel actual: {material.cantidad_actual}
        Nivel mínimo: {material.cantidad_minima}
        Pedido #{nuevo_pedido.id}
        """
        
        email_success = send_email(
            subject=f"Pedido Automático - {material.nombre}",
            body=mensaje,
            to_email=material.proveedor_rel.email
        )
        
        if not email_success:
            logging.warning(f"No se pudo enviar la notificación por email para el pedido #{nuevo_pedido.id}")
        
        return nuevo_pedido
        
    except Exception as e:
        logging.error(f"Error al generar pedido automático: {str(e)}")
        db.session.rollback()
        return None
def revisar_niveles_inventario():
    """Versión mejorada de revisión de inventario con mejor logging"""
    with app.app_context():
        try:
            materiales_bajos = Material.query.filter(
                Material.cantidad_actual < Material.cantidad_minima
            ).all()
            
            logging.info(f"Encontrados {len(materiales_bajos)} materiales bajo el mínimo")
            
            for material in materiales_bajos:
                logging.info(f"Procesando material: {material.nombre}")
                pedido = generar_pedido_automatico(material)
                if pedido:
                    logging.info(f"Pedido generado exitosamente para {material.nombre}")
                    
        except Exception as e:
            logging.error(f"Error al revisar niveles de inventario: {str(e)}")
def revisar_lotes_completos():
    """Revisa los lotes completos y notifica a los clientes asignados"""
    with app.app_context():
        try:
            for producto in Productos.query.all():
                lotes_completos = producto.cantidad // producto.lotes
                if lotes_completos > 0:
                    clientes_asignados = ClienteProducto.query.filter_by(
                        producto_id=producto.id
                    ).all()
                    
                    for asignacion in clientes_asignados:
                        cliente = asignacion.cliente
                        mensaje = f"""
                        Lote(s) Disponible(s) - {producto.nombre}
                        Cantidad de lotes: {lotes_completos}
                        Unidades por lote: {producto.lotes}
                        Total unidades disponibles: {lotes_completos * producto.lotes}
                        """
                        
                        send_notification(
                            subject=f"Lote Disponible - {producto.nombre}",
                            body=mensaje,
                            to_email=cliente.email,
                            to_phone=cliente.telefono
                        )
                        
        except Exception as e:
            logging.error(f"Error al revisar lotes completos: {e}")

def revisar_mantenimiento():
    """Revisa los mantenimientos programados y genera alertas"""
    with app.app_context():
        try:
            fecha_actual = datetime.now()
            
            # Mantenimientos próximos (próximos 7 días)
            proximos = Mantenimiento.query.filter(
                Mantenimiento.fecha_mantenimiento.between(
                    fecha_actual,
                    fecha_actual + timedelta(days=7)
                )
            ).all()
            
            # Mantenimientos vencidos
            vencidos = Mantenimiento.query.filter(
                Mantenimiento.fecha_mantenimiento < fecha_actual
            ).all()
            
            # Procesar próximos mantenimientos
            for mant in proximos:
                # Verificar materiales necesarios
                materiales_necesarios = MaterialMantenimiento.query.filter_by(
                    mantenimiento_id=mant.id
                ).all()
                
                materiales_faltantes = []
                for req in materiales_necesarios:
                    if req.material.cantidad_actual < req.cantidad_requerida:
                        materiales_faltantes.append(req.material)
                
                # Notificar al técnico
                mensaje = f"""
                Mantenimiento Próximo - {mant.equipo}
                Fecha programada: {mant.fecha_mantenimiento}
                Detalles: {mant.detalles}
                """
                
                if materiales_faltantes:
                    mensaje += "\nMateriales faltantes:\n"
                    for mat in materiales_faltantes:
                        mensaje += f"- {mat.nombre}: Disponible {mat.cantidad_actual}\n"
                        generar_pedido_automatico(mat)
                
                if mant.tecnico:
                    send_notification(
                        subject=f"Mantenimiento Próximo - {mant.equipo}",
                        body=mensaje,
                        to_email=mant.tecnico.email,
                        to_phone=mant.tecnico.telefono
                    )
            
            # Procesar mantenimientos vencidos
            for mant in vencidos:
                mensaje = f"""
                ALERTA: Mantenimiento Vencido - {mant.equipo}
                Fecha programada: {mant.fecha_mantenimiento}
                Días de retraso: {(fecha_actual.date() - mant.fecha_mantenimiento).days}
                """
                
                # Notificar al técnico y supervisores
                if mant.tecnico:
                    send_notification(
                        subject=f"URGENTE: Mantenimiento Vencido - {mant.equipo}",
                        body=mensaje,
                        to_email=mant.tecnico.email,
                        to_phone=mant.tecnico.telefono
                    )
                
                # También notificar al administrador
                send_notification(
                    subject=f"URGENTE: Mantenimiento Vencido - {mant.equipo}",
                    body=mensaje,
                    to_email="admin@tuempresa.com"
                )
                
        except Exception as e:
            logging.error(f"Error al revisar mantenimientos: {e}")

def verificar_salud_bot():
    """Verifica el estado de salud del bot"""
    try:
        # Verificar conexión a la base de datos
        with app.app_context():
            db.session.execute('SELECT 1')
        
        # Verificar servicio de email
        send_email(
            subject="Bot Health Check",
            body="Test de salud del bot",
            to_email="empresatroll466@gmail.com"
        )
        
        logging.info("Health check completado exitosamente")
        return True
    except Exception as e:
        logging.error(f"Error en health check: {e}")
        return False

def bot_automatizacion():
    """Versión mejorada del bot principal"""
    logging.info("Iniciando bot de automatización con debugging mejorado")
    
    while True:
        try:
            logging.info("Iniciando ciclo de revisión")
            revisar_niveles_inventario()
            logging.info("Ciclo de revisión completado")
            
            # Aumentar el tiempo entre ciclos para evitar sobrecarga
            time.sleep(30)  # 30 segundos entre ciclos
            
        except Exception as e:
            logging.error(f"Error en ciclo principal del bot: {str(e)}")
            time.sleep(60)  # Esperar más tiempo si hay error

if __name__ == '__main__':
    app = create_app()
    bot_automatizacion()