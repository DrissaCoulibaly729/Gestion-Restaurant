from flask import Blueprint, jsonify, request,  render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, current_user, logout_user
from .models import db, User, MenuItem, Order

bp = Blueprint('routes', __name__)
@bp.route('/')
def home():
    return render_template('home.html')
@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/services')
def services():
    return render_template('services.html')

@bp.route('/menu')
def menu():
    plats = MenuItem.query.all()
    return render_template('menu.html', plats=plats)
@bp.route('/menu/<int:plat_id>', methods=['GET', 'POST'])
@login_required
def plat_detail(plat_id):
    plat = MenuItem.query.get_or_404(plat_id)
    if request.method == 'POST':
        # Créer une nouvelle commande avec le plat sélectionné
        new_order = Order(
            user_id=current_user.id,
            items=plat_id,  # Utiliser une liste contenant le plat sélectionné
            status='en cours',
            special_requests=request.form.get('special_requests', '')
        )
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for('routes.menu'))
    return render_template('plat_detail.html', plat=plat)
@bp.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')
@bp.route('/cart-content')
@login_required
def cart_content():
    orders = db.session.query(Order, MenuItem).join(MenuItem, Order.items == MenuItem.id).filter(Order.user_id == current_user.id).all()

    cart_items = []
    for order, item in orders:
        cart_items.append({
            'name': item.name,
            'price': item.price,
            'image': item.photo,
            'quantity': 1,  # Vous pouvez ajuster en fonction des détails de votre modèle Order
        })

    return jsonify(cart_items)
@bp.route('/cart_count')
@login_required
def cart_count():
    user_id = current_user.id
    count = Order.query.filter_by(user_id=user_id, status='en cours').count()
    return jsonify(count=count)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and password: 
            login_user(user)
            return redirect(url_for('routes.home'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password'] 
        
        # Vérifiez si l'utilisateur existe déjà
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Ce nom d\'utilisateur est déjà utilisé. Veuillez choisir un autre nom.', 'danger')
            return redirect(url_for('routes.register'))
        
        # Créez un nouvel utilisateur avec les données du formulaire
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # Utilisez la méthode set_password pour hasher le mot de passe
        
        # Ajoutez le nouvel utilisateur à la session et committez les changements
        db.session.add(new_user)
        db.session.commit()
        
        flash('Inscription réussie ! Veuillez vous connecter.', 'success')
        return redirect(url_for('routes.login'))
    
    return render_template('register.html')



@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.home'))


@bp.route('/users', methods=['GET'])
@login_required
def get_users():
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized access'}), 403

    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@bp.route('/users', methods=['POST'])
@login_required
def create_user():
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized access'}), 403

    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=generate_password_hash(data['password'])
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@bp.route('/menu_items', methods=['GET'])
def get_menu_items():
    menu_items = MenuItem.query.all()
    return jsonify([item.serialize() for item in menu_items]), 200

@bp.route('/menu_items', methods=['POST'])
@login_required
def create_menu_item():
    if not current_user.is_authenticated or not current_user.admin:
        return jsonify({'message': 'Unauthorized access'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'message': 'Invalid JSON data'}), 400

    new_item = MenuItem(
        name=data.get('name'),
        ingredients=data.get('ingredients'),
        price=data.get('price'),
        available=data.get('available', True),
        photo=data.get('photo'),
        description=data.get('description')
    )

    db.session.add(new_item)
    db.session.commit()

    return jsonify({'message': 'Menu item created successfully'}), 201

@bp.route('/orders', methods=['POST'])
@login_required
def place_order():
    data = request.get_json()
    item_ids = data.get('item_ids', [])
    items = MenuItem.query.filter(MenuItem.id.in_(item_ids)).all()

    new_order = Order(
        user_id=current_user.id,
        items=', '.join([item.name for item in items]),
        special_requests=data.get('special_requests', '')
    )
    db.session.add(new_order)
    db.session.commit()

    return jsonify({'message': 'Order placed successfully'}), 201

@bp.route('/orders', methods=['GET'])
@login_required
def get_orders():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return jsonify([order.serialize() for order in orders]), 200

@bp.route('/admin/orders', methods=['GET'])
@login_required
def get_all_orders():
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized access'}), 403

    orders = Order.query.all()
    return jsonify([order.serialize() for order in orders]), 200

@bp.route('/admin/orders', methods=['POST'])
@login_required
def create_order():
    if not current_user.admin:
        return jsonify({'message': 'Unauthorized access'}), 403

    data = request.get_json()
    user_id = data.get('user_id')
    items = data.get('items', [])
    special_requests = data.get('special_requests', '')

    new_order = Order(
        user_id=user_id,
        items=', '.join(items),
        special_requests=special_requests
    )
    db.session.add(new_order)
    db.session.commit()

    return jsonify({'message': 'Order created successfully'}), 201

@bp.route('/commandes', methods=['GET'])
@login_required
def get_commandes():
    commandes = Commande.query.filter_by(user_id=current_user.id).all()
    return jsonify([commande.serialize() for commande in commandes]), 200

@bp.route('/commandes', methods=['POST'])
@login_required
def create_commande():
    data = request.get_json()
    item_ids = data.get('item_ids', [])
    items = MenuItem.query.filter(MenuItem.id.in_(item_ids)).all()

    new_commande = Commande(
        user_id=current_user.id,
        items=items,
        status=data.get('status', 'En attente'),
        special_requests=data.get('special_requests', '')
    )
    db.session.add(new_commande)
    db.session.commit()

    return jsonify({'message': 'Commande created successfully'}), 201

@bp.route('/commandes/<int:commande_id>', methods=['PUT'])
@login_required
def update_commande(commande_id):
    commande = Commande.query.get(commande_id)
    if not commande:
        return jsonify({'message': 'Commande not found'}), 404

    data = request.get_json()
    if 'status' in data:
        commande.status = data['status']
    if 'special_requests' in data:
        commande.special_requests = data['special_requests']

    db.session.commit()
    return jsonify({'message': 'Commande updated successfully'}), 200

@bp.route('/commandes/<int:commande_id>', methods=['DELETE'])
@login_required
def delete_commande(commande_id):
    commande = Commande.query.get(commande_id)
    if not commande:
        return jsonify({'message': 'Commande not found'}), 404

    db.session.delete(commande)
    db.session.commit()
    return jsonify({'message': 'Commande deleted successfully'}), 200
