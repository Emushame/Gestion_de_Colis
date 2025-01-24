from dbConfig import Utilisateur, Colis, Livraison, HistoriqueStatut, engine, SessionLocal
from flask import Flask, jsonify, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

app = Flask(__name__)
#configuration de la session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Creation de nos differentes APIs
@app.route('/utilisateurs', methods=['GET'])
def get_utilisateurs():
    """Recuperation des tous les utilisateurs dans la bdd"""
    with Session(engine) as db:
        utilisateurs = db.query(Utilisateur).all()
        return jsonify([user.to_dict() for user in utilisateurs])



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
    app.run(debug = True)