# from flask import Flask, render_template, redirect, url_for, request, flash
# from flask_login import LoginManager, login_user, logout_user, login_required, current_user
# from models import db, User  # Assurez-vous que le modèle User est correctement importé

# app = Flask(__name__)
# app.config.from_object('config.Config')

# # Configuration de Flask-Login
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'  # Nom de votre route de connexion

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# @app.context_processor
# def inject_user():
#     return dict(current_user=current_user)

# @app.route('/')
# def home():
#     return render_template('home.html')

# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/services')
# def services():
#     return render_template('services.html')

# @app.route('/menu')
# def menu():
#     return render_template('menu.html')

# @app.route('/testimonials')
# def testimonials():
#     return render_template('testimonials.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         user = User.query.filter_by(email=email).first()
#         if user and user.check_password(password):  # Assurez-vous que check_password est défini dans User
#             login_user(user)
#             return redirect(url_for('home'))
#         else:
#             flash('Invalid credentials')
#     return render_template('login.html')
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         username = request.form.get('username')

#         user = User.query.filter_by(email=email).first()
#         if user:
#             flash('Email address already exists')
#             return redirect(url_for('register'))

#         new_user = User(email=email, username=username)
#         new_user.set_password(password)
#         db.session.add(new_user)
#         db.session.commit()

#         login_user(new_user)
#         return redirect(url_for('home'))

#     return render_template('register.html')


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('home'))

# @app.route('/admin/template', methods=['GET', 'POST'])
# @login_required
# def admin_template():
#     if request.method == 'POST':
#         # Logique pour ajouter un nouveau plat ou gérer les commandes
#         pass  # À compléter selon vos besoins
#     return render_template('admin_template.html')

# if __name__ == '__main__':
#     app.run(debug=True)

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
