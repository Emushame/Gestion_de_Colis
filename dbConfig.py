from sqlalchemy import create_engine, Column, Integer, DateTime, ForeignKey, Enum, String
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
from datetime import datetime

from config import DATABASE_URL

# Connexion à la base de données PostgreSQL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()

# Modèle pour les utilisateurs
class Utilisateur(Base):
    __tablename__ = 'utilisateurs'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    mot_de_passe = Column(String, nullable=False)
    role = Column(Enum('Client', 'Livreur', 'Administrateur', name='role_enum'), nullable=False)
    date_creation = Column(DateTime, default=datetime.utcnow)
    colis = relationship('Colis', back_populates='client', foreign_keys="Colis.client_id")
    livraisons = relationship('Livraison', back_populates='livreur')

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "email": self.email,
            "role": self.role,
            "date_creation": self.date_creation.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            nom=data["nom"],
            email=data["email"],
            mot_de_passe=data["mot_de_passe"],
            role=data["role"],
        )
# Modèle pour les colis
class Colis(Base):
    __tablename__ = 'colis'
    id = Column(Integer, primary_key=True)
    identifiant_unique = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    etat = Column(Enum('A traiter', 'En cours', 'Livré', name='etat_enum'), nullable=False)
    date_creation = Column(DateTime, default=datetime.utcnow)
    client_id = Column(Integer, ForeignKey('utilisateurs.id'))
    livreur_id = Column(Integer, ForeignKey('utilisateurs.id'))
    client = relationship("Utilisateur", back_populates='colis', foreign_keys=[client_id])
    livreur = relationship("Utilisateur", foreign_keys=[livreur_id])
    historique = relationship("HistoriqueStatut", back_populates='colis')

# Modèle pour les livraisons
class Livraison(Base):
    __tablename__ = 'livraisons'
    id = Column(Integer, primary_key=True)
    colis_id = Column(Integer, ForeignKey('colis.id'))
    livreur_id = Column(Integer, ForeignKey('utilisateurs.id'))
    date_livraison = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum('Prevue', 'En cours', 'Terminée', name='status_enum'), nullable=False)
    livreur = relationship("Utilisateur", back_populates='livraisons', foreign_keys=[livreur_id])
    colis = relationship('Colis')

# Modèle pour l'historique des statuts
class HistoriqueStatut(Base):
    __tablename__ = 'historique_statuts'
    id = Column(Integer, primary_key=True)
    colis_id = Column(Integer, ForeignKey('colis.id'))
    etat = Column(Enum('A traiter', 'En cours', 'Livré', name='etat_enum'), nullable=False)
    date_modification = Column(DateTime, default=datetime.utcnow)
    colis = relationship("Colis", back_populates='historique')

# Création des tables dans la base de données
if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    print("Les tables ont été créées avec succès")
