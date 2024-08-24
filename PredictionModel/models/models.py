from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone


db = SQLAlchemy()

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(255), nullable=False)

class Admin(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def ajouterUtil(self):
        pass
    def consulterUtil(self):
        pass
    def modifierUtil(self):
        pass
    def supprimerUtil(self):
        pass
    def consulterStat(self):
        pass

class StandardUser(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def effectuerTest(self):
        pass
    def consulterRecom(self):
        pass
    def consulterFacteurs(self):
        pass

class Doctor(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def ajouterPatient(self):
        pass
    def consulterPatient(self):
        pass
    def supprimerPatient(self):
        pass
    def effectuerTest(self):
        pass
    def mettreCommentaire(self):
        pass

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    prenom = db.Column(db.String(255), nullable=False)
    sexe = db.Column(db.String(10), nullable=False)
    numtel = db.Column(db.String(20), nullable=False)
    datenaiss = db.Column(db.Date, nullable=False)
    commentaire = db.Column(db.Text)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    doctor = db.relationship("Doctor", backref="assigned_patients")
    age = db.Column(db.Integer)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    sexe = db.Column(db.String(10), nullable=False)
    typedouleurthor = db.Column(db.String(255), nullable=False)
    parepos = db.Column(db.Integer, nullable=False)
    fcmax = db.Column(db.Integer, nullable=False)
    cholest = db.Column(db.Integer, nullable=False)
    ang = db.Column(db.Boolean, nullable=False)
    pajeun = db.Column(db.Integer, nullable=False)
    resultat = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref="tests")

def create_tables():
    db.create_all()
