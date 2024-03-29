import json
import boto3
import pandas as pd
from io import StringIO
import requests
import uuid
import csv

# Initialize the S3 client
s3 = boto3.client('s3')

def preprocess_input_data(form_data, model_features):
    """
    Preprocess the incoming form data to match the training data format.
    """
    input_df = pd.DataFrame([form_data])
    input_df.fillna({'gender': 'Missing', 'married': 'Missing', 'dependents': 'Missing',
                     'education': 'Missing', 'selfEmployed': 'Missing', 'applicantIncome': 0,
                     'coapplicantIncome': 0, 'loanAmount': 0, 'loanAmountTerm': 0,
                     'creditHistory': 0, 'propertyArea': 'Missing'}, inplace=True)

    categorical_cols = ['gender', 'married', 'dependents', 'education', 'selfEmployed', 'propertyArea']
    input_df = pd.get_dummies(input_df, columns=categorical_cols, drop_first=True)

    # Adding missing dummy variables
    all_possible_categorical_values = {
        'gender_Female', 'gender_Male', 'married_No', 'married_Yes', 'dependents_0', 'dependents_1',
        'dependents_2', 'dependents_3+', 'education_Graduate', 'education_Not Graduate',
        'selfEmployed_No', 'selfEmployed_Yes', 'propertyArea_Rural', 'propertyArea_Semiurban',
        'propertyArea_Urban'
    }
    missing_cols = all_possible_categorical_values - set(input_df.columns)
    for col in missing_cols:
        input_df[col] = 0  # Add missing columns as zeros

    # Ensure the input DataFrame has columns in the exact order of model_features
    input_df = input_df.reindex(columns=model_features, fill_value=0)

    return input_df

def lambda_handler(event, context):
    model_features = ['applicantIncome', 'coapplicantIncome', 'loanAmount', 'loanAmountTerm',
                      'creditHistory', 'loanAmount_log', 'gender_Female', 'gender_Male',
                      'married_No', 'married_Yes', 'dependents_0', 'dependents_1', 'dependents_2',
                      'dependents_3+', 'education_Graduate', 'education_Not Graduate',
                      'selfEmployed_No', 'selfEmployed_Yes', 'propertyArea_Rural',
                      'propertyArea_Semiurban', 'propertyArea_Urban']
    
    form_data = json.loads(event['body'])
    processed_input = preprocess_input_data(form_data, model_features)
    
    ec2_api_url = 'http://54.172.71.23:5000/predict'
    response = requests.post(ec2_api_url, json=processed_input.to_dict(orient='records'))
    
    if response.status_code == 200:
        prediction = response.json()['prediction']
    else:
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to get prediction from EC2 instance.')
        }
    
    unique_id = str(uuid.uuid4())
    filename = f'submissions/form_submission_{unique_id}.csv'
    
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    headers = list(form_data.keys()) + ['prediction']
    csv_writer.writerow(headers)
    csv_writer.writerow(list(form_data.values()) + [prediction[0]])
    
    bucket_name = 'csvloan-bucket'
    s3.put_object(Bucket=bucket_name, Key=filename, Body=csv_buffer.getvalue())
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Form submission processed and saved successfully.',
            'filename': filename,
            'prediction': prediction  # Adjust according to the format EC2 returns
        }),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
