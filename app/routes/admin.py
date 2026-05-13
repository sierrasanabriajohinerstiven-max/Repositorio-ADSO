from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_file, abort
from flask_login import login_required, current_user
from app import db
from app.models.product import Product
from app.models.order import Order
from app.models.user import User
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

@admin.route('/orders/update_status/<int:order_id>', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    if new_status in ['Pendiente', 'Completado', 'Cancelado']:
        order.status = new_status
        db.session.commit()
        flash(f'Estado del pedido #{order.id} actualizado a {new_status}.', 'success')
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
        'created_at': u.created_at.strftime('%Y-%m-%d %H:%M')
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
