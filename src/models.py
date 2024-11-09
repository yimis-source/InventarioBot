from config import db
from datetime import datetime

class Oferta(db.Model):
    __tablename__ = 'ofertas'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    lotes_ofrecidos = db.Column(db.Integer, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    cliente = db.relationship('Cliente', backref=db.backref('ofertas', lazy=True))
    producto = db.relationship('Productos', backref=db.backref('ofertas', lazy=True))

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materiales.id'), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='pendiente')
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, onupdate=datetime.utcnow)

    material = db.relationship('Material', backref='pedidos')
    proveedor = db.relationship('Proveedor', backref='pedidos')

class ClienteProducto(db.Model):
    __tablename__ = 'cliente_producto'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad_minima = db.Column(db.Integer, nullable=False, default=1)
    notificar = db.Column(db.Boolean, default=True)

    cliente = db.relationship('Cliente', backref='productos_asignados')
    producto = db.relationship('Productos', backref='clientes_asignados')

class TecnicoMantenimiento(db.Model):
    __tablename__ = 'tecnicos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    especialidad = db.Column(db.String(100))
    mantenimientos = db.relationship('Mantenimiento', backref='tecnico')

class Material(db.Model):
    __tablename__ = 'materiales'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad_actual = db.Column(db.Integer, nullable=False)
    cantidad_minima = db.Column(db.Integer, nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=False)
    productos_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ultima_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class Productos(db.Model):  
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    lotes = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    materiales = db.relationship('Material', backref='producto_rel', lazy=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @property
    def cantidad_lotes(self):
        return self.cantidad // self.lotes if self.lotes > 0 else 0

class Mantenimiento(db.Model):
    __tablename__ = 'mantenimiento'
    id = db.Column(db.Integer, primary_key=True)
    equipo = db.Column(db.String(100), nullable=False)
    fecha_mantenimiento = db.Column(db.Date, nullable=False)
    detalles = db.Column(db.String(200), nullable=False)
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tecnico_id = db.Column(db.Integer, db.ForeignKey('tecnicos.id'))
    estado = db.Column(db.String(20), default='programado')
    ultima_actualizacion = db.Column(db.DateTime, onupdate=datetime.utcnow)

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)

class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    materiales = db.relationship('Material', backref='proveedor_rel', lazy=True)
