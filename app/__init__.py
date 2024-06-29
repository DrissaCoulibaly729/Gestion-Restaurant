from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from .models import User  # Assurez-vous d'importer votre modèle User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    with app.app_context():
        db.create_all()

    return app
