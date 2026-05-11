from app import create_app, mail
from flask_mail import Message
import traceback

app = create_app()
with app.app_context():
    try:
        msg = Message("Test", recipients=["stivenrodriguezperez99@gmail.com"], body="Test email")
        mail.send(msg)
        print("Success")
    except Exception as e:
        print("ERROR:")
        traceback.print_exc()
