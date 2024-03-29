# AWSAssignmentA4
## AWS Final Project for Team 4 Section A



### Dataset
The dataset used contains loan request data. The data can be found on Kaggle and credit should go to user Rishi Keshkonapure for the dataset upload. Furthermore, users meet25oza and Hendawy should be credited, as their public code regarding how the model should be made was referenced/used in some cases. These are the sources for this project.

https://www.kaggle.com/datasets/rishikeshkonapure/home-loan-approval

There are two datasets, one for creating the model, and for for testing it. The data was used as it came and no edits were made prior to loading in Python.

### modeljupyter.py
The model used conducts exploratory data analysis, cleans the data, and formats column names to match the names used in Form.html and FormPredictandSave.py. It uses a Random Forest model with Grid Search and Stratified k-folds Cross Validation. Startified k-folds Cross Validation allows us to confront the uneven data discovered in EDA by forcing folds to have the same distribution of data. The final cells of the notebook save the model to a S3 bucket under the name model.joblib to be used later.

### Form.html
Form.html is the front end of the prediction request. The file allows the user to input the features needed to request their prediction using various input methods. The user can then use the "submit" function to call the Amazon Gateway API. After the prediction is made, the webpage will display the prediction for the user under the submit button. Form.html is linked to the Gateway API.

### Amazon Gateway API
There is no code for using Gateway, however it should be noted that a http API was used. This API recieves JSON data from Form.html, and passes it on to FormPredictandSave.py running in a AWS Lambda Function. The Gateway API CORS settings are set appropraitely. 

### Amazon Lambda and FormPredictandSave.py
FormPredictandSave.py runs on Amazon Lambda. The Lambda function first preprocesses data from the Gateway API to match the _model.joblib features. After the data has been processed, it gets sent to an EC2 instance for the prediction to be made. After the prediciton has been made, the result is returned to Lambda, which in turn sends the final result to the front end. Before the function ends, it saves every prediction to a S3 bucket as a CSV. An example is shown in "Example Form Subbmission.csv".

For FormPredictandSave.py to run correctly, there must be two layers for Joblib, Pandas, and Requests. These layers were stored in S3.

### FlaskApp.py and EC2 Instance 



