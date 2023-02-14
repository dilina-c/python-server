from flask import Flask
from flask import request, jsonify
import random, time, json, datetime
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score  
import joblib
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

@app.route('/predict',methods=  ['POST'])
def makePrediction():

   predictValue = [[]]

   json_data = request.get_json()
   predictData= json_data.to_dict()

   day_of_week = datetime.fromtimestamp(predictData["time"]).weekday()
   time_of_day = datetime.fromtimestamp(predictData["time"]).strftime("%I") 

   predictValue = [[day_of_week,time_of_day]]

   #make predictions using the model
   model = joblib.load('Prediction-Model.joblib')
   prediction = model.predict(predictValue)
   return jsonify({"response":prediction.tolist(),"requested_value":predictValue})
  

@app.route('/train')
def trainPredictionModel():
   data = pd.read_csv('device_data.csv')

   X = data[['time_of_day', 'day_of_week']]
   y = data['isOn']

   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

   model = RandomForestClassifier()
   model.fit(X_train.values, y_train.values)

   score = model.score(X_test.values, y_test.values)
   print(f'Accuracy: {score:.2f}')

   joblib.dump(model,'Prediction-Model.joblib')

   return ['prediction model trained',score]


@app.route('/genarate')
def genarateDataSet():

   cred = credentials.Certificate(
    "smart-adapter-test1-firebase-adminsdk-9nc3j-31f034dae2.json")
   firebase_admin.initialize_app(cred)

   db = firestore.client()

   data = []
   now = datetime.now()
   three_months_ago = now - timedelta(days=30)

   devices_col_ref = db.collection(u'devices')

   for device_doc_snap in devices_col_ref.stream():
      device_id = device_doc_snap.id
      
      readings_col_ref = device_doc_snap.reference.collection(u'readings')
      for reading_doc_snap in readings_col_ref.where(u"time", u">=", three_months_ago.timestamp()).stream():
         # print(reading_doc_snap.to_dict())
         datum = reading_doc_snap.to_dict()

         datum["isOn"] = True if datum["i"] > 0.4 else False
         datum["day_of_week"] = datetime.fromtimestamp(datum["time"]).weekday()
         datum["time_of_day"] = datetime.fromtimestamp(
         datum["time"]).strftime("%I")

         data.append(datum)
         # print(data)
         df = pd.DataFrame.from_dict(data)
         df.to_csv(device_id + ".csv")
         print(df)
   return 'Data Set Generated'

if __name__ == '__main__':
   app.run(port=8080, debug=False)

