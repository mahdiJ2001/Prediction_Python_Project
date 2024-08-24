from flask import Blueprint, render_template, redirect, url_for , abort , request
from models.models import db, Patient  
from .forms import AddPatientForm, CommentForm, PredictionForm  , DeletePatientForm # Assurez-vous d'utiliser .forms pour les imports
from flask_login import login_required
from datetime import datetime

docteur_routes = Blueprint('docteur', __name__)

@docteur_routes.route('/effectuer_test_doc')
@login_required
def effectuer_test_doc():
    form = PredictionForm()
    return render_template('doctor/effectuer_test_doc.html', form=form)

@docteur_routes.route('/ajouter_patient', methods=['GET', 'POST'])
@login_required
def ajouter_patient():
    form = AddPatientForm()
    if form.validate_on_submit():
        datenaiss = form.datenaiss.data
        if datenaiss is not None:
            aujourdhui = datetime.now()
            age = aujourdhui.year - datenaiss.year - ((aujourdhui.month, aujourdhui.day) < (datenaiss.month, datenaiss.day))
            new_patient = Patient(nom=form.nom.data, prenom=form.prenom.data, sexe=form.sexe.data, numtel=form.numtel.data, datenaiss=datenaiss, age=age)
            db.session.add(new_patient)
            db.session.commit()
            return redirect(url_for('docteur.consulter_patients'))
        else:
            flash('Veuillez entrer une date de naissance valide', 'danger')
    return render_template('doctor/ajouter_patient.html', form=form)

@docteur_routes.route('/consulter_patients')
@login_required
def consulter_patients():
    patients = Patient.query.all()
    form = DeletePatientForm()
    return render_template('doctor/consulter_patients.html', patients=patients , form=form)

@docteur_routes.route('/mettre_commentaire/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def mettre_commentaire(patient_id):
    patient = Patient.query.get(patient_id)
    form = CommentForm()
    if form.validate_on_submit():
        patient.commentaire = form.comment.data
        db.session.commit()
        return redirect(url_for('docteur.consulter_patients'))
    elif request.method == 'GET':
        form.comment.data = patient.commentaire  # Remplir le champ avec l'ancien commentaire
    return render_template('doctor/mettre_commentaire.html', patient=patient, form=form)

    
@docteur_routes.route('/supprimer_patient/<int:patient_id>', methods=['POST'])
@login_required
def supprimer_patient(patient_id):
    patient = Patient.query.get(patient_id)
    form = DeletePatientForm()
    
    if not patient:
        abort(404)
    
    if form.validate_on_submit():
        db.session.delete(patient)
        db.session.commit()
        return redirect(url_for('docteur.consulter_patients'))
    return render_template('doctor/consulter_patients.html', form=form)

