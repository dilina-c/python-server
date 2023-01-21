from flask import Flask
from flask import Flask, url_for

import random
import time
import json
import datetime

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score  
import joblib



app = Flask(__name__)

@app.route('/predict/')
def makeAnomalyPrediction(predictValue):
   model = joblib.load('Prediction-Model.joblib')
   prediction = model.predict(predictValue)
   return prediction
  

@app.route('/train')
def trainPredictionModel():
   data = pd.read_csv('device_data.csv')

   X = data[['time_of_day', 'day_of_week']]
   y = data['isOn']

   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

   model = RandomForestClassifier()
   model.fit(X_train, y_train)

   score = model.score(X_test, y_test)
   print(f'Accuracy: {score:.2f}')

   joblib.dump(model,'Prediction-Model.joblib')

   return 'prediction model trained'

@app.route('/genarate')
def genarateDataSet():
   data = []
   for i in range(0, 100):
      datum = {
         "voltage": random.random(),
         "current": random.random(),
         "timestamp": time.time() + random.random()*10000000
      }
      datum["isOn"] = True if datum["current"] > 0.5 else False
      datum["day_of_week"] = datetime.datetime.fromtimestamp(datum["timestamp"]).weekday()
      datum["time_of_day"] = datetime.datetime.fromtimestamp(datum["timestamp"]).strftime("%I")
      data.append(datum)
      
      df = pd.DataFrame.from_dict(data)
      df.to_csv("device_data.csv")
   return 'Data Set Generated'

with app.test_request_context():
  print(url_for('makeAnomalyPrediction', predictValue = 0))

   
if __name__ == '__main__':
   app.run()