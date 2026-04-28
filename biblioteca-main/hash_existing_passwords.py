import sys
import os

# Add the project root to sys.path so we can import the app
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.users import User
from werkzeug.security import generate_password_hash

app = create_app()

def hash_passwords():
    with app.app_context():
        users = User.query.all()
        count = 0
        for user in users:
            # Check if the password is already hashed (hashes usually start with pbkdf2:sha256: or scrypt:)
            if not user.passwordUser.startswith(('pbkdf2:sha256:', 'scrypt:', 'argon2:')):
                print(f"Hashing password for user: {user.nameUser}")
                user.set_password(user.passwordUser)
                count += 1
        
        if count > 0:
            db.session.commit()
            print(f"Successfully hashed {count} passwords.")
        else:
            print("No plain-text passwords found.")

if __name__ == "__main__":
    hash_passwords()
