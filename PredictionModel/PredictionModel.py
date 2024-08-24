import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# Load the cleaned CSV file into a DataFrame
df = pd.read_csv(r'C:\Users\ASUS\Downloads\cleaned.csv')

# Define features (X) and target variable (y)
X = df.drop(columns=['target'])
y = df['target']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the classifier
rf_classifier.fit(X_train, y_train)

# Make predictions
y_pred = rf_classifier.predict(X_test)

# Evaluate the classifier
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Print classification report
#print(classification_report(y_test, y_pred))

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

#Resultat avec ces valeurs : 83%

# Create a DataFrame from the dictionary
df_preferred_values = pd.DataFrame(preferred_values)

# Make predictions using the trained classifier
predictions = rf_classifier.predict(df_preferred_values)

# Print the predictions
print("Predictions:", predictions)

probability_of_disease = rf_classifier.predict_proba(df_preferred_values)

# The second column represents the probability of class 1 (heart disease)
probability_of_disease = probability_of_disease[:, 1]

# Print the probability of having heart disease
print("Probability of having heart disease:", probability_of_disease)


pickl = {'model': rf_classifier }
pickle.dump( pickl, open( 'model_file' + ".p", "wb" ) )

file_name = "model_file.p"
with open(file_name, 'rb') as pickled:
    data = pickle.load(pickled)
    model = data['model']

model.predict_proba(df_preferred_values)[:, 1]






