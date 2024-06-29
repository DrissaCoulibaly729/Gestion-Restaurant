from app import create_app, db
from app.models import MenuItem

# Créer l'application Flask
app = create_app()

# Liste des plats à ajouter
plats = [
    {
        'nom': 'Stracciatella',
        'ingredients': 'Bouillon de volaille, œufs, parmesan, persil',
        'prix': 2000,
        'photo': 'images/menu1.jpg',
        'description': 'Soupe italienne traditionnelle à base de bouillon de volaille, d\'œufs battus, de parmesan et de persil.'
    },
    {
        'nom': 'Chevrefrit au miel',
        'ingredients': 'Chèvre frais, miel, noix, feuilles de brick',
        'prix': 1500,
        'photo': 'images/menu2.jpg',
        'description': 'Fromage de chèvre frais enveloppé dans des feuilles de brick croustillantes, garni de miel et de noix.'
    },
    {
        'nom': 'Saumon Gravlax',
        'ingredients': 'Saumon frais, sel, sucre, aneth',
        'prix': 1500,
        'photo': 'images/menu3.jpg',
        'description': 'Saumon mariné dans un mélange de sel, de sucre et d\'aneth, servi en fines tranches.'
    },
    {
        'nom': 'Croustillant de poisson',
        'ingredients': 'Filet de poisson blanc, chapelure, œufs, épices',
        'prix': 1500,
        'photo': 'images/menu4.jpg',
        'description': 'Filet de poisson blanc enrobé d\'une croûte croustillante, accompagné d\'épices.'
    },
    {
        'nom': 'Carpaccio de daurade',
        'ingredients': 'Filet de daurade, huile d\'olive, citron, câpres',
        'prix': 2000,
        'photo': 'images/menu5.jpg',
        'description': 'Filet de daurade frais, tranché finement et assaisonné avec de l\'huile d\'olive, du citron et des câpres.'
    },
]


# Ajouter les plats à la base de données
with app.app_context():
    for plat in plats:
        new_item = MenuItem(
            name=plat['nom'],
            ingredients=plat['ingredients'],
            price=plat['prix'],
            available=True,
            photo=plat['photo'],
            description=plat['description']
        )
        db.session.add(new_item)

    db.session.commit()

print('Plats ajoutés avec succès à la base de données.')
