from flask import Flask, jsonify, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from dbConfig import engine, SessionLocal, Utilisateur, Colis, Livraison, HistoriqueStatut
app = Flask(__name__)
# Configuration de la session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.route('/')
def home():
    """Page d'accueil simple"""
    return jsonify({"message": "Bienvenue dans l'API de gestion de colis"})

@app.route('/utilisateurs/get_utilisateurs', methods=['GET'])
def get_utilisateurs():
    """Récupération de tous les utilisateurs dans la base de données"""
    with Session(engine) as db:
        utilisateurs = db.query(Utilisateur).all()
        return jsonify([user.to_dict() for user in utilisateurs])


@app.route('/utilisateur/create_utilisateur', methods=['POST'])
def create_utilisateur():
    """Crée un nouvel utilisateur."""
    data = request.json
    try:
        with Session(engine) as db:
            utilisateur = Utilisateur.from_dict(data)
            db.add(utilisateur)
            db.commit()
            db.refresh(utilisateur)
            return jsonify(utilisateur.to_dict()), 201
    except IntegrityError:
        return jsonify({'error': 'Email ou données dupliquées'}), 400
if __name__ == '__main__':
    app.run(debug=True)
