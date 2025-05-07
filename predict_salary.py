from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

app = Flask(__name__)
CORS(app)

file_path = "C:\\Users\\KIIT\\Desktop\\AD LAB\\PRICE\\Salary_Data.csv"
data = pd.read_csv(file_path)

data = data.dropna(subset=['Salary'])

categorical_features = ['Gender', 'Education Level', 'Job Title']
encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

encoded_categorical = encoder.fit_transform(data[categorical_features])
encoded_df = pd.DataFrame(encoded_categorical, columns=encoder.get_feature_names_out())

num_features = ['Age', 'Years of Experience']
imputer = SimpleImputer(strategy='mean')  # Fill missing values with column mean
num_data = imputer.fit_transform(data[num_features])

X = np.hstack([encoded_categorical, num_data])
y = data['Salary']

# Train the model
model = LinearRegression()
model.fit(X, y)

@app.route('/')
def home():
    return "Flask server is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.json['input']
        input_df = pd.DataFrame([input_data])

        input_df.fillna(value=data.mean(numeric_only=True), inplace=True)

        input_encoded = encoder.transform(input_df[categorical_features])

        num_input = imputer.transform(input_df[num_features])

        final_input = np.hstack([input_encoded, num_input])

        prediction = model.predict(final_input)

        return jsonify({'Salary': prediction[0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

