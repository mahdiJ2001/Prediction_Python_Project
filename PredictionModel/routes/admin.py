from flask import Blueprint, render_template, redirect, url_for, abort
from models.models import db, User , Doctor, StandardUser , Admin , Test
from .forms import AddUserForm, UpdateUserForm , DeleteUserForm
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash
from sqlalchemy import text
from flask_login import login_required

bcrypt = Bcrypt()

admin_routes = Blueprint('admin', __name__)

@admin_routes.route('/ajouter_utilisateur', methods=['GET', 'POST'])
@login_required
def ajouter_utilisateur():
    form = AddUserForm()
    if form.validate_on_submit():
        name = form.nom.data
        email = form.email.data
        password = form.mot_de_passe.data
        user_type = form.type.data

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(name=name, email=email, password=hashed_password, user_type=user_type)
        db.session.add(new_user)
        db.session.commit()

        if user_type == 'standard':
            standard_user = StandardUser(name=name, email=email, password=hashed_password)
            new_user.standard_user = standard_user
            db.session.add(standard_user)
            db.session.commit()
        elif user_type == 'doctor':
            doctor = Doctor(name=name, email=email, password=hashed_password)
            new_user.doctor = doctor
            db.session.add(doctor)
            db.session.commit()

        return redirect(url_for('admin.consulter_utilisateurs'))
    return render_template('admin/ajouter_utilisateur.html', form=form)

@admin_routes.route('/consulter_utilisateurs')
@login_required
def consulter_utilisateurs():
    form = DeleteUserForm() 
    users = User.query.all()
    return render_template('admin/consulter_utilisateurs.html', users=users , form=form)

@admin_routes.route('/modifier_utilisateur/<int:user_id>', methods=['GET', 'POST'])
@login_required
def modifier_utilisateur(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)
    form = UpdateUserForm(obj=user)
    print("les champs : " , form.email.data , form.nom.data , form.type.data , user.name , user.user_type)
    print(form.errors)
    if form.validate_on_submit():
        old_email = user.email  # Stocker l'ancien email avant la modification
        if user.user_type != form.type.data:
            if user.user_type == 'standard':
                db.session.execute(text("DELETE FROM standard_user WHERE email = :email"), {'email': old_email})
            elif user.user_type == 'doctor':
                db.session.execute(text("DELETE FROM doctor WHERE email = :email"), {'email': old_email})
                
            if form.type.data == 'standard':
                new_standard_user = StandardUser(email=form.email.data, name=form.nom.data, password=user.password)
                db.session.add(new_standard_user)
            elif form.type.data == 'doctor':
                new_doctor = Doctor(email=form.email.data, name=form.nom.data, password=user.password)
                db.session.add(new_doctor)
                
            user.user_type = form.type.data       
        user.name = form.nom.data
        user.email = form.email.data  # Mettre à jour l'email avec le nouvel email
        db.session.commit()
        return redirect(url_for('admin.consulter_utilisateurs')) 
    return render_template('admin/modifier_utilisateur.html', form=form, user=user)

@admin_routes.route('/supprimer_utilisateur/<int:user_id>', methods=['POST'])
@login_required
def supprimer_utilisateur(user_id):
    form = DeleteUserForm()  # Crée une instance du formulaire
    if form.validate_on_submit():  # Vérifie si le formulaire a été soumis et est valide
        user = User.query.get(user_id)
        if user:
            if user.user_type == 'doctor':
                doctor = Doctor.query.filter_by(email=user.email).first()
                if doctor:
                    db.session.delete(doctor)
            elif user.user_type == 'admin':
                admin = Admin.query.filter_by(email=user.email).first()
                if admin:
                    db.session.delete(admin)
            elif user.user_type == 'standard':
                standard_user = StandardUser.query.filter_by(email=user.email).first()
                if standard_user:
                    db.session.delete(standard_user)
            # Supprimer l'utilisateur de la table User
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('admin.consulter_utilisateurs'))
    return render_template('admin/consulter_utilisateurs', form=form)

def get_statistics():
    total_users = User.query.count()
    total_tests = Test.query.count()
    total_standard_users = StandardUser.query.count()
    total_doctors = Doctor.query.count()
    return {
        'total_users': total_users,
        'total_tests': total_tests,
        'total_standard_users': total_standard_users,
        'total_doctors': total_doctors
    }


@admin_routes.route('/consulter_stat')
@login_required
def consulter_stat():
    statistics = get_statistics()
    return render_template('admin/consulter_stat.html', statistics=statistics)