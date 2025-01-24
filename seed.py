from dbConfig import engine, SessionLocal, Utilisateur, Colis, Livraison, HistoriqueStatut
from datetime import datetime


# Données de test
def seed_data():
    with SessionLocal() as session:
        # Création de quelques utilisateurs
        utilisateur1 = Utilisateur(
            nom="Esther",
            email="esther@gmail.com",
            mot_de_passe="1234",
            role="Client"
        )
        utilisateur2 = Utilisateur(
            nom="Prince",
            email="prince@umk.com",
            mot_de_passe="345",
            role="Livreur"
        )

        session.add_all([utilisateur1, utilisateur2])
        session.commit()

        # Création d'un colis pour Esther
        colis = Colis(
            identifiant_unique="COLIS12345",
            description="Ordinateur portable",
            etat="A traiter",
            client_id=utilisateur1.id
        )
        session.add(colis)
        session.commit()

        # Historique du colis
        historique = HistoriqueStatut(
            colis_id=colis.id,
            etat="A traiter",
            date_modification=datetime.utcnow()
        )
        session.add(historique)
        session.commit()


if __name__ == '__main__':
    seed_data()
    print("Données de test insérées avec succès")
