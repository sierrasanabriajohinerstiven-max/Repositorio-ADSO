"""
Script de limpieza de base de datos.
- Borra todos los pedidos (OrderItem + Order)
- Borra todos los usuarios excepto el admin principal
- Crea/actualiza el admin con el correo de marichuy y contraseña encriptada
- Conserva todos los productos
"""
from app import create_app, db
from app.models.user import User
from app.models.order import Order, OrderItem

app = create_app()

ADMIN_EMAIL = 'marichuyy.m.a@gmail.com'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = '12872sierra'

with app.app_context():
    print("=== Iniciando limpieza de base de datos ===")
    
    # 1. Borrar todos los items de pedidos
    items_deleted = OrderItem.query.delete()
    print(f"  - OrderItems eliminados: {items_deleted}")
    
    # 2. Borrar todos los pedidos
    orders_deleted = Order.query.delete()
    print(f"  - Orders eliminados: {orders_deleted}")
    
    # 3. Borrar TODOS los usuarios
    users_deleted = User.query.delete()
    print(f"  - Usuarios eliminados: {users_deleted}")
    
    # 4. Crear el único admin
    admin = User(
        username=ADMIN_USERNAME,
        email=ADMIN_EMAIL,
        is_admin=True
    )
    admin.set_password(ADMIN_PASSWORD)
    db.session.add(admin)
    
    db.session.commit()
    
    # Verificar
    admin_check = User.query.filter_by(email=ADMIN_EMAIL).first()
    print(f"  - Admin creado: {admin_check.username} ({admin_check.email}), is_admin={admin_check.is_admin}")
    print(f"  - Password válido: {admin_check.check_password(ADMIN_PASSWORD)}")
    
    from app.models.product import Product
    products_count = Product.query.count()
    print(f"  - Productos conservados: {products_count}")
    
    print("=== Limpieza completada ===")
