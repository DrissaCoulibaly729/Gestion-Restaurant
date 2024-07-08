from flask_mail import Message
from app import mail  # Assurez-vous d'importer votre instance de mail

def send_order_confirmation(email, order):
    msg = Message('Confirmation de commande', recipients=[email])
    msg.body = f'Votre commande {order.id} a été confirmée avec succès!'
    mail.send(msg)
