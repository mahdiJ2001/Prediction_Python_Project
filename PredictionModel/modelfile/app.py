from flask import Flask, render_template, jsonify, request
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__, static_folder='../client/static', template_folder='../client/templates')


def load_models():
    file_name = "models/model_file.p"
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form.to_dict()
    print(data)
    input_data = pd.DataFrame(data,columns=['age', 'sex', 'cp', 'rbp', 'chol', 'fbs', 'maxhr', 'exang'], index=[0])
    model = load_models()
    print(input_data)
    prediction = model.predict_proba(input_data)[:, 1][0]
    return jsonify({'response': prediction})
@app.route('/Recommendations')
def recommendations():
    return render_template('Recommendations.html')

@app.route('/Risk_Factors')
def risk_factors():
    return render_template('Risk_Factors.html')

@app.route('/Data_Set')
def dataset():
    return render_template('Data_Set.html')

if __name__ == '__main__':
    app.run(debug=True)