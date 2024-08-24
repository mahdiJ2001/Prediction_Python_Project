from flask_wtf import FlaskForm
from wtforms import IntegerField, RadioField,StringField, PasswordField, SelectField, SubmitField,HiddenField , TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo , Length
from wtforms.fields import DateField

class RegistrationForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('Type d\'utilisateur', choices=[('standard', 'Utilisateur Standard'), ('admin', 'Admin'), ('doctor', 'Docteur')], validators=[DataRequired()])
    submit = SubmitField('S\'inscrire')

class LoginForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    user_type = SelectField('Type d\'utilisateur', choices=[('standard', 'Utilisateur Standard'), ('admin', 'Admin'), ('doctor', 'Docteur')], validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class AddUserForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    type = SelectField('Type', choices=[('docteur', 'Docteur'), ('utilisateur', 'Utilisateur')], validators=[DataRequired()])
    

class UpdateUserForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    type = SelectField('Type', choices=[('doctor', 'Docteur'), ('standard', 'Utilisateur Standard')], validators=[DataRequired()])
    submit = SubmitField('Enregistrer')

class AddPatientForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prénom', validators=[DataRequired()])
    sexe = SelectField('Sexe', choices=[('M', 'Masculin'), ('F', 'Féminin')], validators=[DataRequired()])
    numtel = StringField('Numéro de téléphone', validators=[DataRequired()])
    datenaiss = DateField('Date de naissance', format='%Y-%m-%d', validators=[DataRequired()])

class CommentForm(FlaskForm):
    comment = TextAreaField('Commentaire', validators=[DataRequired()])

class PredictionForm(FlaskForm):
    age = IntegerField('Âge', validators=[DataRequired()])
    sex = RadioField('Sexe', choices=[('1', 'Homme'), ('0', 'Femme')], validators=[DataRequired()])
    cp = IntegerField('Type de douleur thoracique', validators=[DataRequired()])
    rbp = IntegerField('Pression artérielle au repos en mm Hg', validators=[DataRequired()])
    chol = IntegerField('Cholestérol en mg/dL', validators=[DataRequired()])
    fbs = RadioField('Glycémie à jeun supérieure à 120 mg/dL', choices=[('1', 'Oui'), ('0', 'Non')], validators=[DataRequired()])
    maxhr = IntegerField('Fréquence cardiaque maximale', validators=[DataRequired()])
    exang = RadioField('Angine de poitrine induite par l\'exercice', choices=[('1', 'Oui'), ('0', 'Non')], validators=[DataRequired()])
    submit = SubmitField('Prédire')

class DeleteUserForm(FlaskForm):
    csrf = HiddenField('CSRF Token')

class DeletePatientForm(FlaskForm):
    submit = SubmitField('Confirmer la suppression')