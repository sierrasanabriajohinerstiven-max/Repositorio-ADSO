from app import create_app, db
from app.utils.email_service import send_nequi_confirmation
import os

app = create_app()
with app.app_context():
    # Creamos un PDF dummy para probar
    os.makedirs('instance/receipts', exist_ok=True)
    dummy_pdf_path = 'instance/receipts/test_recibo.pdf'
    with open(dummy_pdf_path, 'wb') as f:
        f.write(b'%PDF-1.4 dummy pdf content')

    try:
        products = [{'name': 'Cacao', 'quantity': 1, 'price': 12000.00}]
        success = send_nequi_confirmation(
            email='stivenrodriguezperez99@gmail.com',
            name='Test',
            total=12000.00,
            products=products,
            pdf_path=dummy_pdf_path
        )
        print("Success:", success)
    except Exception as e:
        print("ERROR:", e)
