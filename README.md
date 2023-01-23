# python-server
This python server is a web server built using the Flask framework. Flask is a micro web framework written in Python that allows developers to build web applications quickly and easily.

This server has three routes:

1. /predict: It accepts a JSON data containing 'to_predict' field, loads a pre-trained model using joblib, makes a prediction using the model and returns the prediction and the requested value in a JSON format.
2. /train: It loads a csv file 'device_data.csv', trains a RandomForestClassifier model, saves the model to a file 'Prediction-Model.joblib' and returns a list containing the message 'prediction model trained' and the score.
3. /genarate: It generates a dataset and saves it to a csv file 'device_data.csv'.

This server can accept JSON data via a POST request at the /predict route and respond with a JSON data containing the prediction and requested value. It can also train a prediction model using a provided csv file and generate a dataset.
