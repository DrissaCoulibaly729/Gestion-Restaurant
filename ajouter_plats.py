from app import create_app, db
from app.models import Menu

app = create_app()

with app.app_context():
    plats = [
        {'nom': 'Thiebou dieune', 'ingredients': 'Riz, Poisson, Légumes', 'prix': 2000},
        {'nom': 'Mafe', 'ingredients': 'Riz, Viande, Sauce arachide', 'prix': 1500},
        {'nom': 'Domoda', 'ingredients': 'Riz, Viande, Sauce tomate', 'prix': 1500},
        {'nom': 'Soupou Kandia', 'ingredients': 'Riz, Viande, Sauce gombo', 'prix': 1500},
        {'nom': 'Thiere', 'ingredients': 'Couscous, Viande, Légumes', 'prix': 2000},
        {'nom': 'Soloukhou', 'ingredients': 'Riz, Viande, Sauce arachide', 'prix': 1500},
        {'nom': 'Mbakhal', 'ingredients': 'Riz, Haricots, Viande', 'prix': 2000},
        {'nom': 'Yassa', 'ingredients': 'Riz, Poulet, Oignons', 'prix': 1500},
        {'nom': 'Thiebou Ndiebe', 'ingredients': 'Riz, Poisson sec, Légumes', 'prix': 2000},
        {'nom': 'Vermicelle', 'ingredients': 'Vermicelle, Viande, Sauce tomate', 'prix': 1500},
        {'nom': 'Couss Couss', 'ingredients': 'Couscous, Viande, Légumes', 'prix': 1500},
        {'nom': 'Lathiry ak sow', 'ingredients': 'Mil, Lait', 'prix': 1000},
        {'nom': 'Lakh', 'ingredients': 'Mil, Lait', 'prix': 1000}
    ]

    for plat in plats:
        menu_item = Menu(
            nom=plat['nom'], ingredients=plat['ingredients'], prix=plat['prix'])
        db.session.add(menu_item)

    db.session.commit()
    print("Plats ajoutés avec succès!")
