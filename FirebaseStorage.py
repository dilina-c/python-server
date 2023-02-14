
import firebase_admin
from firebase_admin import credentials ,storage

cred = credentials.Certificate("./firebase_storage/key.json")
app = firebase_admin.initialize_app(cred,{'storageBucket' : "smart-power-adapter-3a443.appspot.com"})

source_blob_name = 'Prediction-Model.joblib'

#The path to which the file should be downloaded
destination_file_name = "./firebase_storage/Prediction-Model.joblib"

bucket = storage.bucket()

Dilinablob = bucket.blob(source_blob_name)
Dilinablob.download_to_filename(destination_file_name)


fileName = "./firebase_storage/kariyawasam.jpg"
blob = bucket.blob("kariyawasam.jpg")
blob.upload_from_filename(fileName)