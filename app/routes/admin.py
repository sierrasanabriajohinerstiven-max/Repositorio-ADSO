from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_file, abort
from flask_login import login_required, current_user
from app import db, mail
from app.models.product import Product
from app.models.order import Order
from app.models.user import User
from app.models.notification import Notification
from app.utils.timezone import format_datetime
from functools import wraps

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('No tienes permisos para acceder a esta página.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    products_count = Product.query.count()
    orders_count = Order.query.count()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    low_stock_products = Product.query.filter(Product.stock < 10).all()
    
    return render_template('admin/dashboard.html', 
                           products_count=products_count, 
                           orders_count=orders_count,
                           recent_orders=recent_orders,
                           low_stock_count=len(low_stock_products),
                           low_stock_products=low_stock_products)

@admin.route('/products')
@login_required
@admin_required
def products():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@admin.route('/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        
        product = Product(name=name, description=description, price=price, stock=stock)
        db.session.add(product)
        db.session.commit()
        
        flash('Producto agregado exitosamente.', 'success')
        return redirect(url_for('admin.products'))
        
    return render_template('admin/product_form.html', product=None)

@admin.route('/orders')
@login_required
@admin_required
def orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@admin.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.stock = int(request.form.get('stock'))
        
        db.session.commit()
        flash('Producto actualizado exitosamente.', 'success')
        return redirect(url_for('admin.products'))
        
    return render_template('admin/product_form.html', product=product)

@admin.route('/products/delete/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Producto eliminado.', 'success')
    return redirect(url_for('admin.products'))


# ─────────────────────────────────────────────────────────────
# Actualizar estado del pedido (con notificación + correo)
# ─────────────────────────────────────────────────────────────
@admin.route('/orders/update_status/<int:order_id>', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    valid_statuses = [
        'Verificando pedido',
        'Verificando pago',
        'Preparando tu pedido',
        'Pedido en camino',
        'Pedido entregado',
        'Cancelado'
    ]
    
    if new_status in valid_statuses:
        if order.status != new_status:
            old_status = order.status
            order.status = new_status
            
            # Mensajes de notificación personalizados según estado
            notification_messages = {
                'Verificando pedido': f'Tu pedido #{order.id} está siendo verificado. ¡Pronto tendrás novedades!',
                'Verificando pago': f'Tu pedido #{order.id} está en verificación de pago. ¡Pronto confirmaremos!',
                'Preparando tu pedido': f'Tu pedido #{order.id} está en preparación. ¡Pronto estará listo!',
                'Pedido en camino': f'Tu pedido #{order.id} ha sido enviado. ¡Va en camino!',
                'Pedido entregado': f'Tu pedido #{order.id} ha sido entregado. ¡Disfrútalo!',
                'Cancelado': f'Tu pedido #{order.id} ha sido cancelado.'
            }
            
            # Crear notificación para el usuario
            notification = Notification(
                user_id=order.user_id,
                message=notification_messages.get(new_status, f'El estado de tu pedido #{order.id} se actualizó a: {new_status}')
            )
            db.session.add(notification)
            db.session.commit()
            
            # Enviar correo automático al cliente
            try:
                from app.utils.email_service import send_status_email
                customer_email = order.customer_email or order.customer.email
                customer_name = order.customer_name or order.customer.username
                send_status_email(order, new_status, customer_email, customer_name)
            except Exception as e:
                print(f"Error enviando correo de estado: {e}")
            
            flash(f'Estado del pedido #{order.id} actualizado a "{new_status}".', 'success')
        else:
            flash(f'El pedido #{order.id} ya tiene el estado "{new_status}".', 'info')
    else:
        flash('Estado no válido.', 'danger')
    
    return redirect(url_for('admin.orders'))


# ─────────────────────────────────────────────────────────────
# Confirmar pago (enviar correo con PDF adjunto)
# ─────────────────────────────────────────────────────────────
@admin.route('/orders/confirm_payment/<int:order_id>', methods=['POST'])
@login_required
@admin_required
def confirm_payment(order_id):
    order = Order.query.get_or_404(order_id)
    user = User.query.get(order.user_id)
    if not user or not user.email:
        flash('No se encontró correo del cliente.', 'warning')
        return redirect(url_for('admin.orders'))
    
    # Build email
    from flask_mail import Message
    from flask import current_app
    import os
    
    msg = Message(
        subject='Comprobante de pago confirmado',
        sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'marichuyy.m.a@gmail.com'),
        recipients=[user.email]
    )
    msg.body = (
        f"Hola {user.username},\n\n"
        f"Tu pago para el pedido #{order.id} ha sido verificado y confirmado. "
        f"Adjuntamos el comprobante de pago para tu referencia.\n\n"
        f"Gracias por confiar en Marichuy.\n\n"
        f"Saludos,\nEquipo Marichuy"
    )
    
    # Attach PDF receipt if exists
    receipt_path = os.path.join(current_app.instance_path, f'receipts/receipt_{order.id}.pdf')
    if os.path.exists(receipt_path):
        with open(receipt_path, 'rb') as f:
            msg.attach(f'recibo_{order.id}.pdf', 'application/pdf', f.read())
    
    try:
        mail.send(msg)
        flash('Correo de confirmación enviado al cliente.', 'success')
    except Exception as e:
        print(f"Error enviando correo de confirmación: {e}")
        flash('Error al enviar el correo de confirmación.', 'danger')
    
    return redirect(url_for('admin.orders'))


# ─────────────────────────────────────────────────────────────
# Reenviar correo de verificación del comprobante
# ─────────────────────────────────────────────────────────────
@admin.route('/orders/resend_verification/<int:order_id>', methods=['POST'])
@login_required
@admin_required
def resend_verification_email(order_id):
    order = Order.query.get_or_404(order_id)
    user = User.query.get(order.user_id)
    
    if not user or not user.email:
        flash('No se encontró correo del cliente.', 'warning')
        return redirect(url_for('admin.orders'))
    
    if not order.payment_proof:
        flash('Este pedido no tiene comprobante de pago adjunto.', 'warning')
        return redirect(url_for('admin.orders'))
    
    try:
        from app.utils.email_service import send_verification_confirmed_email
        customer_email = order.customer_email or user.email
        customer_name = order.customer_name or user.username
        send_verification_confirmed_email(order, customer_email, customer_name)
        flash(f'Correo de verificación reenviado al cliente para el pedido #{order.id}.', 'success')
    except Exception as e:
        print(f"Error reenviando correo de verificación: {e}")
        flash('Error al enviar el correo de verificación.', 'danger')
    
    return redirect(url_for('admin.orders'))


@admin.route('/orders/delete/<int:order_id>', methods=['POST'])
@login_required
@admin_required
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    # The cascading delete (if configured in models) will delete order_items, 
    # but to be safe we'll delete them manually first just in case
    for item in order.items:
        db.session.delete(item)
    db.session.delete(order)
    db.session.commit()
    flash(f'Pedido #{order.id} eliminado exitosamente.', 'success')
    return redirect(url_for('admin.orders'))

@admin.route('/api/clients')
@login_required
def api_clients():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    users = User.query.filter_by(is_admin=False).order_by(User.created_at.desc()).limit(15).all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'order_count': u.orders.count(),
        'created_at': format_datetime(u.created_at)
    } for u in users])

@admin.route('/clients/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_client(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash('No puedes eliminar a un administrador.', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    # Delete associated orders and order items
    for order in user.orders:
        for item in order.items:
            db.session.delete(item)
        db.session.delete(order)
        
    db.session.delete(user)
    db.session.commit()
    flash('Cliente eliminado exitosamente de la base de datos.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/proof/<int:order_id>')
@login_required
@admin_required
def view_proof(order_id):
    import os
    order = Order.query.get_or_404(order_id)
    if not order.payment_proof or not os.path.exists(order.payment_proof):
        flash('El comprobante no existe o no ha sido cargado.', 'warning')
        return redirect(url_for('admin.dashboard'))
    return send_file(os.path.abspath(order.payment_proof))
