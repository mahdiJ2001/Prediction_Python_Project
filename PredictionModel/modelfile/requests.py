# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 10:36:10 2024

@author: ASUS
"""

import requests
import pandas as pd

preferred_values = {
    'age': [45],
    'sex': [0],  # Assuming 1 for male, 0 for female
    'cp': [3],
    'rbp': [112],
    'chol': [149],
    'fbs': [0],  # Assuming 0 for false, 1 for true
    'maxhr': [125],
    'exang': [0]  # Assuming 0 for false, 1 for true
}
df_preferred_values = pd.DataFrame(preferred_values)
input_data = df_preferred_values.to_dict(orient='records')




URL = "http://127.0.0.1:5000/predict"
headers = {"Content-Type" : "application/json"}
data = {"input" : input_data }
r = requests.get(URL,headers=headers, json=data)
r.json()