# InventarioBot

Sistema de gestión de inventario con bot de automatización para control de materiales, proveedores, clientes, productos y mantenimiento de equipos.

## Características

- **Gestión de Inventario**: Control de materiales con alertas de stock mínimo
- **Gestión de Proveedores**: Administración de proveedores y pedidos automáticos
- **Gestión de Clientes**: Registro de clientes y ofertas personalizadas
- **Gestión de Productos**: Control de productos, lotes y precios
- **Mantenimiento de Equipos**: Programación y seguimiento de mantenimientos
- **Bot de Automatización**: Notificaciones automáticas por email
- **Pedidos Automáticos**: Creación automática de pedidos cuando el stock es bajo

## Requisitos

- Python 3.8+
- Flask 3.0+
- SQLAlchemy 2.0+
- Cuenta de Gmail para notificaciones (con contraseña de aplicación)

## Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/yimis-source/InventarioBot.git
cd InventarioBot
```

2. **Crear entorno virtual**
```bash
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

Variables requeridas en `.env`:
```env
SECRET_KEY=tu-secret-key-aqui
EMAIL_USER=tu-email@gmail.com
EMAIL_PASSWORD=tu-password-de-aplicacion
FLASK_ENV=development
```

## Uso

### Iniciar la aplicación web

```bash
cd src
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

### Iniciar el bot de automatización

```bash
cd src
python bot.py
```

El bot se ejecutará continuamente y:
- Revisará el inventario cada minuto
- Creará pedidos automáticos para materiales bajo stock mínimo
- Enviará notificaciones por email a proveedores y clientes
- Gestionará recordatorios de mantenimiento

## Estructura del Proyecto

```
InventarioBot/
├── src/
│   ├── app.py              # Aplicación Flask principal
│   ├── bot.py              # Bot de automatización
│   ├── config.py           # Configuración de la aplicación
│   ├── models.py           # Modelos de base de datos
│   ├── database.py         # Configuración de base de datos
│   ├── validators.py       # Validadores de entrada
│   ├── templates/          # Plantillas HTML
│   └── static/             # Archivos estáticos (CSS, JS)
├── requirements.txt        # Dependencias del proyecto
├── .env.example           # Ejemplo de variables de entorno
├── .gitignore             # Archivos ignorados por git
├── README.md              # Este archivo
└── MEJORAS.md             # Documentación de mejoras implementadas
```

## Funcionalidades Principales

### 1. Gestión de Materiales
- Agregar, editar y listar materiales
- Control de cantidades actuales y mínimas
- Alertas automáticas de stock bajo
- Relación con proveedores y productos

### 2. Gestión de Proveedores
- Registro de proveedores con datos de contacto
- Validación de emails y teléfonos
- Asociación con materiales

### 3. Gestión de Clientes
- Registro de clientes
- Asignación de productos con cantidades mínimas
- Sistema de ofertas personalizadas

### 4. Gestión de Productos
- Control de productos, precios y lotes
- Cálculo automático de lotes disponibles
- Relación con materiales

### 5. Mantenimiento de Equipos
- Programación de mantenimientos
- Asignación de técnicos
- Seguimiento de estados (programado, en proceso, completado)

### 6. Sistema de Pedidos
- Creación manual de pedidos
- Generación automática cuando stock < mínimo
- Historial de pedidos
- Estados: pendiente, en proceso, completado

## Seguridad

El proyecto implementa múltiples medidas de seguridad:

- ✅ **Validación de entrada**: Sanitización de todos los datos de formularios
- ✅ **Protección de credenciales**: Variables de entorno para información sensible
- ✅ **Cookies seguras**: HttpOnly, Secure, SameSite
- ✅ **SQL Injection**: Protección mediante ORM de SQLAlchemy
- ✅ **Logging**: Registro de operaciones para auditoría

Ver `MEJORAS.md` para detalles completos.

## Notas Importantes

1. **Gmail**: Para usar notificaciones por email, configura una [contraseña de aplicación](https://support.google.com/accounts/answer/185833) de Google

2. **Secret Key**: Genera una clave segura:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

3. **Base de Datos**: Por defecto usa SQLite. Para producción, considera PostgreSQL o MySQL

4. **Logs**: Revisa `app.log` y `bot_automatization.log` para seguimiento de operaciones

## Desarrollo

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Realiza tus cambios siguiendo las prácticas de seguridad establecidas
4. Commit tus cambios (`git commit -m 'Añade nueva funcionalidad'`)
5. Push a la rama (`git push origin feature/nueva-funcionalidad`)
6. Abre un Pull Request

## Solución de Problemas

### El bot no envía emails
- Verifica que `EMAIL_USER` y `EMAIL_PASSWORD` estén configurados
- Usa una contraseña de aplicación de Gmail, no tu contraseña normal
- Revisa `bot_automatization.log` para errores específicos

### Errores de base de datos
- Elimina `src/inventario.db` y reinicia la aplicación para crear una nueva
- Verifica que tienes permisos de escritura en el directorio

### Errores de validación
- Verifica que los datos de entrada cumplan con los formatos requeridos
- Revisa `app.log` para ver qué validación falló

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Contacto

Para preguntas o sugerencias, abre un issue en GitHub.
