# Importations nécessaires
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_login import UserMixin

# Configuration de l'application Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialisation des extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Modèles de données
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    available = db.Column(db.Boolean, default=True)
    photo = db.Column(db.String(200))  # Chemin vers l'image du plat
    description = db.Column(db.String(500))  # Description du plat

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('MenuItem', secondary='order_items', backref='orders', lazy=True)
    status = db.Column(db.String(50), default='Pending')
    special_requests = db.Column(db.String(200))

# Table d'association pour la relation many-to-many entre Order et MenuItem
order_items = db.Table('order_items',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('menu_item.id'), primary_key=True)
)

# Routes pour l'administration
@app.route('/admin/template', methods=['GET', 'POST'])
@login_required
def admin_template():
    if request.method == 'POST':
        # Logique pour ajouter un nouveau plat ou gérer les commandes
        pass  # À compléter selon vos besoins
    return render_template('admin_template.html')

# Configuration du LoginManager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Point d'entrée de l'application
if __name__ == '__main__':
    app.run(debug=True)
