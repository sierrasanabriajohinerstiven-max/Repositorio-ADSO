from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    u = User.query.filter_by(email='admin@marichuy.com').first()
    if not u:
        u = User(username='admin', email='admin@marichuy.com', is_admin=True)
        print("Creating new admin user...")
    else:
        print("Updating existing admin user...")
        u.is_admin = True
    
    u.set_password('admin123')
    db.session.add(u)
    db.session.commit()
    print("Admin user ensured: admin@marichuy.com / admin123")
