from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():

    app = Flask(__name__)    
    app.config.from_object('config.Config')
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(idUser):
        from .models.users import User
        return User.query.get(int(idUser))

    # Import all models so they are registered with SQLAlchemy
    from .models.users import User
    from .models.authors import Author
    from .models.rooms import Room
    from .models.perfil import Perfil
    from .models.posts import Post
    from .models.tags import Tag
    from .models.audit import Auditoria

    # Register Audit Listeners
    from app.utils.audit_handler import register_audit_listeners
    for model in [User, Author, Room, Post, Tag, Perfil]:
        register_audit_listeners(model)

    # Register blueprints
    from app.routes import (
        auth, author_routes, users_route, 
        room_routes, users_route_async, perfil_route,
        posts_route, tags_route, buscador_route, audit_routes
    )
    app.register_blueprint(auth.bp)
    app.register_blueprint(author_routes.bp)
    app.register_blueprint(users_route.bp)
    app.register_blueprint(room_routes.bp)
    app.register_blueprint(users_route_async.bp)
    app.register_blueprint(perfil_route.bp)
    app.register_blueprint(posts_route.bp)
    app.register_blueprint(tags_route.bp)
    app.register_blueprint(buscador_route.bp)
    app.register_blueprint(audit_routes.bp)

    @app.after_request
    def add_header(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    return app