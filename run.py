import os
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'NOT SET')
        print(f"=== DATABASE URI: {db_uri}")
        
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri[len('sqlite:///'):]
            db_dir = os.path.dirname(db_path)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
        
        db.create_all()

        # === LIMPIEZA ÚNICA DE BASE DE DATOS ===
        from app.models.user import User
        from app.models.order import Order, OrderItem
        from app.models.product import Product

        OrderItem.query.delete()
        Order.query.delete()
        User.query.delete()

        admin = User(username='admin', email='marichuyy.m.a@gmail.com', is_admin=True)
        admin.set_password('12872sierra')
        db.session.add(admin)
        db.session.commit()

        print(f"=== DB limpia. Admin: {admin.email}, Productos: {Product.query.count()}")
        # === FIN LIMPIEZA ===
    
    host = os.environ.get('FLASK_RUN_HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    
    app.run(host=host, debug=debug)
