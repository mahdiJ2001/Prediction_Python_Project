from flask import Blueprint, render_template, redirect, url_for,flash
from routes.forms import RegistrationForm, LoginForm
from models.models import User,StandardUser,Doctor,Admin,db
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash
from flask_login import login_manager, login_user , logout_user
from flask_login import login_required
from flask import flash


bcrypt = Bcrypt()
auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        user_type = form.user_type.data

        if password != confirm_password:
            flash("Les mots de passe ne correspondent pas", "error")
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash("L'email est déjà utilisé", "error")
            return redirect(url_for('auth.register'))

        if user_type == 'admin':
            if Admin.query.first() is not None:
                flash("Il ne peut y avoir qu'un seul admin", "error")
                return redirect(url_for('auth.register'))
            else:   
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                new_user = User(name=name, email=email, password=hashed_password, user_type=user_type)
                admin = Admin(name=form.name.data, email=form.email.data, password=hashed_password)
                db.session.add(admin)
                db.session.commit()
                new_user.admin = admin
                db.session.add(new_user)
                db.session.commit()
        elif user_type == 'doctor':
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(name=name, email=email, password=hashed_password, user_type=user_type)
            doctor = Doctor(name=name, email=email, password=hashed_password)
            db.session.add(doctor)
            db.session.commit()
            new_user.doctor = doctor
            db.session.add(new_user)
            db.session.commit()
        elif user_type == 'standard':
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(name=name, email=email, password=hashed_password, user_type=user_type)
            standard_user = StandardUser(name=name, email=email, password=hashed_password)
            db.session.add(standard_user)
            db.session.commit()
            new_user.standard_user = standard_user
            db.session.add(new_user)
            db.session.commit()
        
        flash("Inscription réussie!", "success")
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user:
            if user.user_type == form.user_type.data:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    if user.user_type == 'standard':
                        return redirect(url_for('standard_user.effectuer_test'))
                    elif user.user_type == 'doctor':
                        return redirect(url_for('docteur.effectuer_test_doc'))
                    elif user.user_type == 'admin':
                        return redirect(url_for('admin.consulter_utilisateurs'))
                else:
                    flash('Invalid username or password', 'danger')
            else:
                flash('Invalid user type', 'danger')
        else:
            flash('User not found', 'danger')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))