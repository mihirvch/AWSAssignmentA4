# AWSAssignmentA4
## AWS Final Project for Team 4, Section A

### Dataset
The dataset contains loan request data and can be found on Kaggle. Credit goes to user Rishi Keshkonapure for uploading the dataset. Additionally, credit is due to users meet25oza and Hendawy, as their public code regarding the model construction was referenced/used in some instances. Below are the sources for this project:

https://www.kaggle.com/datasets/rishikeshkonapure/home-loan-approval

There are two datasets: one for creating the model and another for testing it. The data was used as received, with no edits made prior to loading in Python.

### modeljupyter.ipynb
The model conducts exploratory data analysis, cleans the data, and formats column names to match those used in `Form.html` and `FormPredictandSave.py`. It utilizes a Random Forest model with Grid Search and Stratified k-folds Cross Validation. Stratified k-folds Cross Validation helps address uneven data distributions discovered during EDA by ensuring folds have the same data distribution. The final cells of the notebook save the model to an S3 bucket under the name `model.joblib` for later use. This model was saved using the AWS Sagemaker Jupyter Notebooks feautre.

### Form.html style.css background.jpeg
`Form.html` serves as the front end for the prediction request. It allows users to input the necessary features for their prediction using various input methods. Users can then submit their request to the Amazon Gateway API using the "submit" function. After the prediction is made, the webpage will display the result under the submit button. `Form.html` is linked to the Gateway API. The style.css document and background image allow for a better looking front end.

### Amazon Gateway API
Although there is no specific code for the Gateway API, it's noteworthy that an HTTP API was utilized. This API receives JSON data from `Form.html` and forwards it to `FormPredictandSave.py` running in an AWS Lambda Function. The Gateway API's CORS settings are configured appropriately.

### Amazon Lambda and FormPredictandSave.py
`FormPredictandSave.py` executes within Amazon Lambda. The Lambda function preprocesses data from the Gateway API to align with the `model.joblib` features. Once processed, the data is sent to an EC2 instance for prediction. After the prediction is made, the result is sent back to Lambda, which then forwards the final outcome to the front end. Before concluding, the function saves every prediction to an S3 bucket as a CSV file, exemplified in "Example Form Submission.csv".

For `FormPredictandSave.py` to function correctly, two layers for Joblib, Pandas, and Requests are necessary. These layers are stored in S3.

### FlaskApp.py and EC2 Instance
`FlaskApp.py` contains a simple Flask app running on the EC2 instance. The app uses the previously saved `joblib` file to make predictions on incoming data from Lambda and returns the prediction to Lambda.

## AWS Workflow
Refer to the file `AWSWorkflow.jpg` for the complete workflow diagram.
