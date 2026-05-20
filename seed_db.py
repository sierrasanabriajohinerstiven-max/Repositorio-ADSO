from app import create_app, db
from app.models.user import User
from app.models.product import Product

app = create_app()

with app.app_context():
    # Crear Admin
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(username='admin', email='admin@marichuy.com', is_admin=True)
        admin_user.set_password('admin123')
        db.session.add(admin_user)
    
    # Crear producto
    chocolate = Product.query.filter_by(name='Chocolate Marichuy 100% Cacao (Sin Azúcar)').first()
    if not chocolate:
        chocolate = Product(
            # pyrefly: ignore [unexpected-keyword]
            name='Chocolate Marichuy 100% Cacao (Sin Azúcar)',
            # pyrefly: ignore [unexpected-keyword]
            description='Presentación de 125 gramos. 100% Natural, puro cacao sin azúcar. Una pastilla de cacao por cada taza de agua o leche, panela al gusto. *Nota: El precio está sujeto a cambios dependiendo del comportamiento del mercado del cacao.*',
            # pyrefly: ignore [unexpected-keyword]
            price=12000.0,
            # pyrefly: ignore [unexpected-keyword]
            stock=100,
            # pyrefly: ignore [unexpected-keyword]
            image_file='cacao_125g.png'
        )
        db.session.add(chocolate)
    
    db.session.commit()
    print("Database seeded successfully!")
