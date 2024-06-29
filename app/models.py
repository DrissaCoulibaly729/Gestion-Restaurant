from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    # Retourne l'instance de l'utilisateur basée sur user_id
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # Changer de password à password_hash
    orders = db.relationship('Order', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    available = db.Column(db.Boolean, default=True)
    photo = db.Column(db.String(200)) 
    description = db.Column(db.String(500))  

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)  # Clé étrangère pour MenuItem.id
    status = db.Column(db.String(50), default='en cours')
    special_requests = db.Column(db.String(200))
