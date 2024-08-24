from datetime import datetime , timezone
from flask import Blueprint, render_template, jsonify, request , session
from flask_login import login_required
from routes.forms import PredictionForm
import pickle
import pandas as pd
from flask_login import login_required , current_user
from models.models import Test, db


standard_user = Blueprint('standard_user', __name__)

@standard_user.route('/effectuer_test')
@login_required
def effectuer_test():
    form = PredictionForm()
    return render_template('user/effectuer_test.html', form=form)

@standard_user.route('/facteurs')
@login_required
def facteurs():
    return render_template('user/facteurs.html')

@standard_user.route('/recommandations')
@login_required
def recommandations():
    return render_template('user/recommandations.html')

@standard_user.route('/data_set')
@login_required
def data_set():
    return render_template('user/data_set.html')

def load_models():
    file_name = "modelfile/models/model_file.p"
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model

@standard_user.route('/predict', methods=['POST'])
@login_required
def predict():
    data = request.form.to_dict()
    input_data = pd.DataFrame(data, columns=['age', 'sex', 'cp', 'rbp', 'chol', 'fbs', 'maxhr', 'exang'], index=[0])
    model = load_models()
    prediction = model.predict_proba(input_data)[:, 1][0]

    test = Test(
            age=int(data['age']),
            sexe=data['sex'],
            typedouleurthor=data['cp'],
            parepos=int(data['rbp']),
            cholest=int(data['chol']),
            ang=data['fbs'] == '1',
            fcmax=int(data['maxhr']),
            pajeun=data['exang'] == '1',
            resultat=prediction * 100,
            user_id=current_user.id,
            date = datetime.now(timezone.utc)
        )
    db.session.add(test)
    db.session.commit()
    return jsonify({'response': prediction})

@standard_user.route('/consulter_tests', methods=['GET'])
@login_required
def consulter_tests():
    tests = Test.query.all()
    return render_template('user/consulter_tests.html', tests=tests)