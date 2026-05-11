from app import create_app, db
from app.models.order import Order
from app.utils.pdf_generator import generate_receipt

app = create_app()
with app.app_context():
    order = Order.query.get(9)
    if order:
        cart_items = {}
        for item in order.items:
            cart_items[str(item.product.id)] = {
                'name': item.product.name, 
                'quantity': item.quantity, 
                'price': item.price
            }
        generate_receipt(order, cart_items)
        print("Recibo 9 regenerado exitosamente.")
    else:
        print("Order 9 not found")
