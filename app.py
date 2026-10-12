from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Konfiguration der SQLite-Datenbank im Projektordner
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'vereinsplaner.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Erweitertes User-Modell mit Passwort-Hash
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='player') # 'player' oder 'captain'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route("/")
def hello():
    return "Tischtennis Vereinsplaner Backend mit Benutzerverwaltung läuft!"

# Einfache Registrierungs-Route als Test
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Benutzername und Passwort erforderlich"}), 400

    # Prüfen, ob der User bereits existiert
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({"error": "Benutzer existiert bereits"}), 400

    new_user = User(
        username=data['username'],
        role=data.get('role', 'player')
    )
    new_user.set_password(data['password'])
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"Benutzer {new_user.username} erfolgreich registriert!"}), 201

if __name__ == "__main__":
    # Datenbanktabellen beim Start automatisch erstellen falls nicht vorhanden
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)