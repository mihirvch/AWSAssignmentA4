from flask import Flask, request, jsonify
import pandas as pd
import joblib
import boto3
from io import BytesIO


app = Flask(__name__)

# Function to load model from S3
def load_model_from_s3(bucket_name, model_key):
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=model_key)
    model_file = response['Body'].read()
    model = joblib.load(BytesIO(model_file))
    return model

# Replace 'your_bucket_name' and 'your_model_key' with your S3 bucket name and model file key
MODEL_BUCKET = 'model-bucket-mihir'
MODEL_KEY = '_model.joblib'

# Load your model
model = load_model_from_s3(MODEL_BUCKET, MODEL_KEY)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    df = pd.DataFrame(data)
    prediction = model.predict(df)
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
