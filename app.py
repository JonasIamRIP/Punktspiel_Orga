from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Konfiguration der SQLite-Datenbank im Projektordner
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'vereinsplaner.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Beispiel-Modell für Benutzer (Spieler & Kapitäne)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default='player') # 'player' oder 'captain'

    def __repr__(self):
        return f'<User {self.username}>'

@app.route("/")
def hello():
    return "Tischtennis Vereinsplaner Backend mit SQLite läuft!"

if __name__ == "__main__":
    # Datenbanktabellen beim Start automatisch erstellen falls nicht vorhanden
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)