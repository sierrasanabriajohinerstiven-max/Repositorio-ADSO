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
    truffles = Product.query.filter_by(name='Trufas Artesanales Premium').first()
    if not truffles:
        truffles = Product(
            name='Trufas Artesanales Premium',
            description='Una exquisita selección de trufas rellenas de ganache oscuro, elaboradas con el mejor cacao y un toque de licor, espolvoreadas con polvo de oro comestible. Perfecto para regalar.',
            price=25000.0,
            stock=50,
            image_file='truffles.png'
        )
        db.session.add(truffles)
    
    db.session.commit()
    print("Database seeded successfully!")
