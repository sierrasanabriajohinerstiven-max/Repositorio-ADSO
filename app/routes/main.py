from flask import Blueprint, render_template, redirect, url_for, flash, session, request, send_file
from werkzeug.utils import secure_filename
import os
import io
from app.utils.pdf_generator import generate_receipt
from app.utils.email_service import send_nequi_confirmation
from flask_login import current_user, login_required
from app import db
from app.models.product import Product
from app.models.order import Order, OrderItem

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    products = Product.query.all()
    return render_template('main/index.html', products=products)

@main.route('/product/<int:product_id>')
@login_required
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('main/product_detail.html', product=product)

@main.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    if quantity <= 0:
        flash('La cantidad debe ser mayor a 0 para añadir al carrito.', 'warning')
        return redirect(request.referrer or url_for('main.index'))
    
    if 'cart' not in session:
        session['cart'] = {}
        
    cart = session['cart']
    
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += quantity
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': product.price,
            'quantity': quantity,
            'image': product.image_file
        }
        
    session.modified = True
    flash(f'{product.name} añadido al carrito.', 'success')
    return redirect(request.referrer or url_for('main.index'))

@main.route('/cart')
@login_required
def cart():
    cart_items = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart_items.values())
    return render_template('main/cart.html', cart_items=cart_items, total=total)

@main.route('/remove_from_cart/<product_id>')
@login_required
def remove_from_cart(product_id):
    if 'cart' in session and product_id in session['cart']:
        del session['cart'][product_id]
        session.modified = True
        flash('Producto eliminado del carrito.', 'info')
    return redirect(url_for('main.cart'))

@main.route('/update_cart/<product_id>', methods=['POST'])
@login_required
def update_cart(product_id):
    if 'cart' in session and product_id in session['cart']:
        quantity = int(request.form.get('quantity', 1))
        if quantity > 0:
            session['cart'][product_id]['quantity'] = quantity
            session.modified = True
        elif quantity == 0:
            del session['cart'][product_id]
            session.modified = True
            flash('Producto eliminado del carrito.', 'info')
    return redirect(url_for('main.cart'))

@main.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = session.get('cart', {})
    if not cart_items:
        flash('Tu carrito está vacío.', 'warning')
        return redirect(url_for('main.index'))
        
    total = sum(item['price'] * item['quantity'] for item in cart_items.values())
    
    if request.method == 'POST':
        payment_method = request.form.get('payment_method')
        address = request.form.get('address')
        address_desc = request.form.get('address_description', '').strip()
        if address_desc:
            address = f"{address} | Info: {address_desc}"
        
        phone = request.form.get('phone')
        customer_name = request.form.get('customer_name')
        customer_email = request.form.get('customer_email')
        
        order = Order(
            user_id=current_user.id,
            total_amount=total,
            payment_method=payment_method,
            shipping_address=address,
            phone_number=phone,
            customer_name=customer_name,
            customer_email=customer_email
        )
        db.session.add(order)
        db.session.flush() # Para obtener el ID de la orden
        
        for p_id, item in cart_items.items():
            order_item = OrderItem(
                order_id=order.id,
                product_id=int(p_id),
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)
            
        db.session.commit()
        
        if payment_method == 'nequi':
            session.pop('cart', None)
            return redirect(url_for('main.nequi_payment', order_id=order.id))
            
        session.pop('cart', None)
        return redirect(url_for('main.order_success', payment_method=payment_method))
        
    return render_template('main/checkout.html', total=total)

@main.route('/order_success')
@login_required
def order_success():
    payment_method = request.args.get('payment_method', 'efectivo')
    return render_template('main/order_success.html', payment_method=payment_method)

@main.route('/nequi_payment/<int:order_id>', methods=['GET', 'POST'])
@login_required
def nequi_payment(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        if 'proof' not in request.files:
            flash('No se subió ningún archivo.', 'danger')
            return redirect(request.url)
            
        file = request.files['proof']
        if file.filename == '':
            flash('No seleccionaste ningún archivo.', 'danger')
            return redirect(request.url)
            
        if file:
            filename = secure_filename(file.filename)
            proofs_dir = os.path.join('instance', 'proofs')
            os.makedirs(proofs_dir, exist_ok=True)
            file_path = os.path.join(proofs_dir, f'proof_{order.id}_{filename}')
            file.save(file_path)
            
            order.payment_proof = file_path
            order.status = 'Verificando pago'
            db.session.commit()
            
            # Generar el PDF reconstruyendo los cart_items
            cart_items = {str(item.product_id): {'name': item.product.name, 'quantity': item.quantity, 'price': item.price} for item in order.items}
            pdf_bytes, pdf_path = generate_receipt(order, cart_items)
            
            # Enviar el correo de confirmación con el PDF adjunto
            products_list = list(cart_items.values())
            send_nequi_confirmation(order.customer_email or order.customer.email, order.customer_name or order.customer.username, order.total_amount, products_list, pdf_path)
            
            flash('Comprobante enviado con éxito. Hemos enviado tu recibo por correo.', 'success')
            return redirect(url_for('main.order_success', payment_method='nequi'))
            
    return render_template('main/nequi_payment.html', order=order)

@main.route('/download_receipt/<int:order_id>.pdf')
@login_required
def download_receipt(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('main.index'))
        
    # Generar el PDF dinámicamente para que siempre tenga el estado actualizado
    cart_items = {str(item.product_id): {'name': item.product.name, 'quantity': item.quantity, 'price': item.price} for item in order.items}
    pdf_bytes, _ = generate_receipt(order, cart_items)
    
    return send_file(
        io.BytesIO(pdf_bytes), 
        as_attachment=True, 
        download_name=f'Recibo_Marichuy_Pedido_{order.id}.pdf', 
        mimetype='application/pdf'
    )

from app.models.notification import Notification

@main.route('/profile')
@login_required
def profile():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template('main/profile.html', orders=user_orders, notifications=notifications)

@main.route('/clear_notifications', methods=['POST'])
@login_required
def clear_notifications():
    from app.models.notification import Notification
    from app import db
    Notification.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('Notificaciones limpiadas.', 'success')
    return redirect(url_for('main.profile'))

@main.route('/download_qr')
def download_qr():
    from flask import current_app
    qr_path = os.path.join(current_app.static_folder, 'img', 'qr_nequi.png')
    if os.path.exists(qr_path):
        return send_file(qr_path, as_attachment=True, download_name='QR_Nequi_Marichuy.png', mimetype='image/png')
    else:
        flash('El código QR no está disponible en este momento.', 'warning')
        return redirect(request.referrer or url_for('main.index'))
