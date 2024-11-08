# app.py
from flask import render_template, request, redirect, url_for, flash
from config import create_app, db
from models import ClienteProducto, Material, Cliente, Mantenimiento, Proveedor, Productos, TecnicoMantenimiento,Pedido, Oferta
from datetime import datetime

app = create_app()

@app.route('/')
def index():
    return render_template('index.html')

#funnciones de los materiales
@app.route('/agregar_material', methods=['GET', 'POST'])
def agregar_material():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            cantidad_actual = int(request.form['cantidad_actual'])
            cantidad_minima = int(request.form['cantidad_minima'])
            proveedor_id = int(request.form['proveedor_id'])
            productos_id = request.form.get('productos_id')
            
            if productos_id:
                productos_id = int(productos_id)
            
            nuevo_material = Material(
                nombre=nombre,
                cantidad_actual=cantidad_actual,
                cantidad_minima=cantidad_minima,
                proveedor_id=proveedor_id,
                productos_id=productos_id
            )
            db.session.add(nuevo_material)
            db.session.commit()
            flash('Material agregado exitosamente.', 'success')
        except ValueError:
            flash('Error: Los valores numéricos no son válidos.', 'error')
            return redirect(url_for('agregar_material'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar material: {str(e)}', 'error')
            return redirect(url_for('agregar_material'))
        
        return redirect(url_for('listar_materiales'))
    
    proveedores = Proveedor.query.all()
    productos = Productos.query.all()
    return render_template('agregar_material.html', proveedores=proveedores, productos=productos)

@app.route('/listar_materiales')
def listar_materiales():
    try:
        materiales = Material.query.join(Proveedor).all()
        return render_template('listar_materiales.html', materiales=materiales)
    except Exception as e:
        flash(f'Error al listar materiales: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/editar_material/<int:id>', methods=['GET', 'POST'])
def editar_material(id):
    material = Material.query.get_or_404(id)
    if request.method == 'POST':
        try:
            material.cantidad_actual = int(request.form['cantidad_actual'])
            material.cantidad_minima = int(request.form['cantidad_minima'])
            material.ultima_actualizacion = datetime.now(datetime.timezone.utc)
            db.session.commit()
            flash('Material actualizado exitosamente.', 'success')
        except ValueError:
            flash('Error: Los valores ingresados no son válidos.', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar material: {str(e)}', 'error')
        return redirect(url_for('listar_materiales'))
    
    return render_template('editar_material.html', material=material)



#funciones de los proveedores
@app.route('/agregar_proveedor', methods=['GET', 'POST'])
def agregar_proveedor():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            telefono = request.form['telefono']
            email = request.form['email']
            
            nuevo_proveedor = Proveedor(
                nombre=nombre,
                telefono=telefono,
                email=email
            )
            db.session.add(nuevo_proveedor)
            db.session.commit()
            flash('Proveedor agregado exitosamente.', 'success')
            return redirect(url_for('listar_proveedores'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar proveedor: {str(e)}', 'error')
            return redirect(url_for('agregar_proveedor'))
    
    return render_template('agregar_proveedor.html')

@app.route('/listar_proveedores')
def listar_proveedores():
    proveedores = Proveedor.query.all()
    return render_template('listar_proveedores.html', proveedores=proveedores)

@app.route('/editar_proveedor/<int:id>', methods=['GET', 'POST'])
def editar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    if request.method == 'POST':
        try:
            proveedor.nombre = request.form['nombre']
            proveedor.telefono = request.form['telefono']
            proveedor.email = request.form['email']
            db.session.commit()
            flash('Proveedor actualizado exitosamente.', 'success')
            return redirect(url_for('listar_proveedores'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar proveedor: {str(e)}', 'error')
            return redirect(url_for('editar_proveedor', id=id))
    return render_template('editar_proveedor.html', proveedor=proveedor)


#funciones de los clientes
@app.route('/agregar_cliente', methods=['GET', 'POST'])
def agregar_cliente():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            email = request.form['email']
            telefono = request.form['telefono']
            
            nuevo_cliente = Cliente(
                nombre=nombre,
                email=email,
                telefono=telefono
            )
            db.session.add(nuevo_cliente)
            db.session.commit()
            flash('Cliente agregado exitosamente.', 'success')
            return redirect(url_for('listar_clientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar cliente: {str(e)}', 'error')
            return redirect(url_for('agregar_cliente'))
    
    return render_template('agregar_cliente.html')

@app.route('/listar_clientes')
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('listar_clientes.html', clientes=clientes)

@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id: int):
    cliente = Cliente.query.get_or_404(id)
    if request.method == 'POST':
        try:
            cliente.nombre = request.form['nombre']
            cliente.email = request.form['email']
            cliente.telefono = request.form['telefono']
            db.session.commit()
            flash('El cliente fue actualizado exitosamente.', 'success')
            return redirect(url_for('listar_clientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al editar cliente: {str(e)}', 'error')
            return redirect(url_for('editar_cliente', id=id))
    return render_template('editar_cliente.html', cliente=cliente)

@app.route('/asignar_cliente_producto', methods=['GET', 'POST'])
def asignar_cliente_producto():
    if request.method == 'POST':
        try:
            cliente_id = int(request.form['cliente_id'])
            producto_id = int(request.form['producto_id'])
            cantidad_minima = int(request.form['cantidad_minima'])
            
            asignacion = ClienteProducto(
                cliente_id=cliente_id,
                producto_id=producto_id,
                cantidad_minima=cantidad_minima
            )
            db.session.add(asignacion)
            db.session.commit()
            flash('Asignación realizada exitosamente.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error en la asignación: {str(e)}', 'error')
        return redirect(url_for('listar_clientes'))
    
    clientes = Cliente.query.all()
    productos = Productos.query.all()
    return render_template('asignar_cliente_producto.html', clientes=clientes, productos=productos)



#funciones de los productos
@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            precio = float(request.form['precio'])
            lotes = int(request.form['lotes'])
            cantidad = int(request.form['cantidad'])
            
            nuevo_producto = Productos(
                nombre=nombre,
                precio=precio,
                lotes=lotes,
                cantidad=cantidad
            )
            db.session.add(nuevo_producto)
            db.session.commit()
            flash('Producto agregado exitosamente.', 'success')
            return redirect(url_for('listar_productos'))
        except ValueError:
            flash('Error: Los valores numéricos no son válidos.', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar producto: {str(e)}', 'error')
        return redirect(url_for('agregar_producto'))
    
    return render_template('agregar_productos.html')

@app.route('/listar_productos')
def listar_productos():
    productos = Productos.query.all()
    return render_template('listar_productos.html', productos=productos)

@app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Productos.query.get_or_404(id)
    
    if request.method == 'POST':
        # Actualizar los valores del producto desde el formulario
        producto.nombre = request.form['nombre']
        producto.precio = float(request.form['precio'])
        producto.lotes = int(request.form['lotes'])
        producto.cantidad = int(request.form['cantidad'])
        
        try:
            db.session.commit()
            flash('Producto actualizado con éxito.', 'success')
            return redirect(url_for('listar_productos'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar el producto.', 'error')
            print(e)
            return redirect(url_for('editar_producto', id=id))
    
    return render_template('editar_producto.html', producto=producto)

#funciones de tecnicos
@app.route('/agregar_tecnico', methods=['GET', 'POST'])
def agregar_tecnico():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            email = request.form['email']
            telefono = request.form['telefono']
            especialidad = request.form['especialidad']
            
            nuevo_tecnico = TecnicoMantenimiento(
                nombre=nombre,
                email=email,
                telefono=telefono,
                especialidad=especialidad
            )
            db.session.add(nuevo_tecnico)
            db.session.commit()
            flash('Técnico agregado exitosamente.', 'success')
            return redirect(url_for('listar_tecnicos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar técnico: {str(e)}', 'error')
            return redirect(url_for('agregar_tecnico'))
    
    return render_template('agregar_tecnico.html')

@app.route('/listar_tecnicos')
def listar_tecnicos():
    tecnicos = TecnicoMantenimiento.query.all()
    return render_template('listar_tecnicos.html', tecnicos=tecnicos)

@app.route('/editar_tecnico/<int:id>', methods=['GET', 'POST'])
def editar_tecnico(id):
    tecnico = TecnicoMantenimiento.query.get_or_404(id)
    if request.method == 'POST':
        try:
            tecnico.nombre = request.form['nombre']
            tecnico.email = request.form['email']
            tecnico.telefono = request.form['telefono']
            tecnico.especialidad = request.form['especialidad']
            db.session.commit()
            flash('Información del técnico actualizada.', 'success')
            return redirect(url_for('listar_tecnicos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar técnico: {str(e)}', 'error')
            return redirect(url_for('editar_tecnico', id=id))
    return render_template('editar_tecnico.html', tecnico=tecnico)

@app.route('/asignar_tecnico_mantenimiento/<int:mantenimiento_id>', methods=['GET', 'POST'])
def asignar_tecnico_mantenimiento(mantenimiento_id):
    if request.method == 'POST':
        try:
            tecnico_id = int(request.form['tecnico_id'])
            mantenimiento = Mantenimiento.query.get_or_404(mantenimiento_id)
            mantenimiento.tecnico_id = tecnico_id
            db.session.commit()
            flash('Técnico asignado exitosamente.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al asignar técnico: {str(e)}', 'error')
        return redirect(url_for('mantenimiento'))
    
    mantenimiento = Mantenimiento.query.get_or_404(mantenimiento_id)
    tecnicos = TecnicoMantenimiento.query.all()
    return render_template('asignar_tecnico.html', mantenimiento=mantenimiento, tecnicos=tecnicos)

#funciones de mantenimiento
@app.route('/mantenimiento', methods=['GET', 'POST'])
def mantenimiento():
    if request.method == 'POST':
        try:
            equipo = request.form['equipo']
            fecha_mantenimiento = datetime.strptime(request.form['fecha_mantenimiento'], '%Y-%m-%d').date()
            detalles = request.form['detalles']
            
            nuevo_mantenimiento = Mantenimiento(
                equipo=equipo,
                fecha_mantenimiento=fecha_mantenimiento,
                detalles=detalles
            )
            db.session.add(nuevo_mantenimiento)
            db.session.commit()
            flash('Registro de mantenimiento agregado exitosamente.', 'success')
        except ValueError:
            flash('Error: Formato de fecha inválido. Use YYYY-MM-DD', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar mantenimiento: {str(e)}', 'error')
        return redirect(url_for('mantenimiento'))
            
    mantenimientos = Mantenimiento.query.order_by(Mantenimiento.fecha_mantenimiento.desc()).all()
    return render_template('mantenimiento_equipos.html', mantenimientos=mantenimientos)

@app.route('/editar_mantenimiento/<int:id>', methods=['GET', 'POST'])
def editar_mantenimiento(id):
    mantenimiento = Mantenimiento.query.get_or_404(id)
    if request.method == 'POST':
        try:
            mantenimiento.equipo = request.form['equipo']
            mantenimiento.fecha_mantenimiento = datetime.strptime(request.form['fecha_mantenimiento'], '%Y-%m-%d').date()
            mantenimiento.detalles = request.form['detalles']
            mantenimiento.estado = request.form['estado']
            db.session.commit()
            flash('Registro de mantenimiento actualizado exitosamente.', 'success')
            return redirect(url_for('mantenimiento'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar mantenimiento: {str(e)}', 'error')
            return redirect(url_for('editar_mantenimiento', id=id))
    return render_template('editar_mantenimiento.html', mantenimiento=mantenimiento)


#funciones de pedidos
@app.route('/crear_pedido', methods=['GET', 'POST'])
def crear_pedido():
    if request.method == 'POST':
        material_id = request.form['material_id']
        proveedor_id = request.form['proveedor_id']
        cantidad = request.form['cantidad']
        nuevo_pedido = Pedido(
            material_id=material_id,
            proveedor_id=proveedor_id,
            cantidad=cantidad,
            estado='pendiente'
        )
        db.session.add(nuevo_pedido)
        db.session.commit()
        flash('Pedido creado exitosamente.')
        return redirect(url_for('listar_pedidos'))
    materiales = Material.query.all()
    proveedores = Proveedor.query.all()
    return render_template('agregar_pedido.html', materiales=materiales, proveedores=proveedores)

@app.route('/listar_pedidos')
def listar_pedidos():
    pedidos = Pedido.query.all()
    return render_template('listar_pedidos.html', pedidos=pedidos)


@app.route('/editar_pedidos/<int:id>', methods=['GET', 'POST'])
def editar_pedido(id):
    pedido = Pedido.query.get(id)
    if request.method == 'POST':
        pedido.estado = request.form['estado']
        db.session.commit()
        flash('Estado del pedido actualizado.')
        return redirect(url_for('listar_pedidos'))
    return render_template('editar_pedido.html', pedido=pedido)

@app.route('/historial_pedidos')
def historial_pedidos():
    pedidos = Pedido.query.order_by(Pedido.fecha_creacion.desc()).all()
    return render_template('historial_pedidos.html', pedidos=pedidos)

#funciones de ofertas 
@app.route('/listar_ofertas')
def listar_ofertas():
    ofertas = Oferta.query.all()
    return render_template('listar_ofertas.html', ofertas=ofertas)

@app.route('/agregar_oferta', methods=['GET', 'POST'])
def agregar_oferta():
    clientes = Cliente.query.all()
    productos = Productos.query.all()
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        producto_id = request.form['producto_id']
        lotes_ofrecidos = int(request.form['lotes_ofrecidos'])
        oferta = Oferta(cliente_id=cliente_id, producto_id=producto_id, lotes_ofrecidos=lotes_ofrecidos)
        db.session.add(oferta)
        db.session.commit()
        flash('Oferta creada con éxito')
        return redirect(url_for('listar_ofertas'))
    return render_template('agregar_oferta.html', clientes=clientes, productos=productos)

@app.route('/editar_oferta/<int:id>', methods=['GET', 'POST'])
def editar_oferta(id):
    oferta = Oferta.query.get_or_404(id)
    clientes = Cliente.query.all()
    productos = Productos.query.all()
    if request.method == 'POST':
        oferta.cliente_id = request.form['cliente_id']
        oferta.producto_id = request.form['producto_id']
        oferta.lotes_ofrecidos = int(request.form['lotes_ofrecidos'])
        db.session.commit()
        flash('Oferta actualizada con éxito')
        return redirect(url_for('listar_ofertas'))
    return render_template('editar_oferta.html', oferta=oferta, clientes=clientes, productos=productos)

#funciones de alertas
@app.route('/alertas')
def alertas():
    materiales_bajos = Material.query.filter(Material.cantidad_actual < Material.cantidad_minima).all()
    return render_template('alertas.html', materiales_bajos=materiales_bajos)
#funciones de ofertas
@app.route('/ofertas')
def ofertas():
    return render_template('ofertas.html')
#funciones de 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#funcion main 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)