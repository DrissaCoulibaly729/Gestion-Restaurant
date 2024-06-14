from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Utilisateur, Menu, Commande

bp_main = Blueprint('main', __name__)


@bp_main.route('/')
def index():
    return render_template('index.html')


@bp_main.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom_utilisateur = request.form['nom_utilisateur']
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']

        existing_user = Utilisateur.query.filter_by(email=email).first()
        if existing_user:
            flash('Cette adresse email est déjà associée à un compte.', 'danger')
            return redirect(url_for('main.inscription'))

        utilisateur = Utilisateur(nom_utilisateur=nom_utilisateur, email=email)
        utilisateur.set_password(mot_de_passe)

        db.session.add(utilisateur)
        db.session.commit()

        flash('Inscription réussie! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('main.connexion'))

    return render_template('inscription.html')


@bp_main.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        utilisateur = Utilisateur.query.filter_by(email=email).first()
        if utilisateur and utilisateur.check_password(mot_de_passe):
            login_user(utilisateur)
            flash('Connexion réussie!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Échec de la connexion. Veuillez vérifier vos informations.', 'danger')
    return render_template('connexion.html')


@bp_main.route('/deconnexion')
@login_required
def deconnexion():
    logout_user()
    flash('Vous êtes maintenant déconnecté.', 'success')
    return redirect(url_for('main.index'))


@bp_main.route('/menu')
def afficher_menu():
    menus = Menu.query.all()
    return render_template('menu.html', menus=menus)


@bp_main.route('/commande', methods=['GET', 'POST'])
@login_required
def passer_commande():
    if request.method == 'POST':
        menu_id = request.form['menu_id']
        quantite = request.form['quantite']
        demandes_speciales = request.form['demandes_speciales']
        commande = Commande(utilisateur_id=current_user.id, menu_id=menu_id,
                            quantite=quantite, demandes_speciales=demandes_speciales)
        db.session.add(commande)
        db.session.commit()
        flash('Commande passée avec succès!', 'success')
        return redirect(url_for('main.index'))
    menus = Menu.query.all()
    return render_template('commande.html', menus=menus)


@bp_main.route('/mes_commandes')
@login_required
def mes_commandes():
    commandes = Commande.query.filter_by(utilisateur_id=current_user.id).all()
    return render_template('mes_commandes.html', commandes=commandes)
