from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from utils import preproc, predict
from geopy.geocoders import GoogleV3
from datetime import datetime
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"])  # Allows all headers

@app.get("/")
def index():
    return {"greeting": "PreCog Matrix"}

#http://localhost:8000/predict?address=5%20Everson%20Drive%2C%20North%20York
@app.get("/predict")
def predict_query(address, crime_date: Optional[datetime] = Query(None)):
    if crime_date is None:
        crime_date = datetime.now()

    city = 'Toronto'

    year = crime_date.year
    month = crime_date.month
    day = crime_date.day
    hour = crime_date.hour

    def get_lat_lon_google(address):
        geolocator = GoogleV3(api_key='GOOGLE_API_KEY')
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    lat, long = get_lat_lon_google(address + ', ' + city)


    model_path = 'models/crime_prediction_lightgbm_model.joblib'
    onehot_columns = ['Crime_A', 'Crime_B', 'Crime_C', 'Crime_D', 'Crime_E', 'Crime_F']  # Tem que ajustar, pq não sei os nomes
    df = preproc.load_data(lat, long, year, month, day, hour)
    scaler = preproc.load_scaler('models/scaler.joblib')
    df_processed = preproc.preproc(df, scaler)
    prediction =  predict.main(model_path, df_processed, onehot_columns)
    return prediction


predict_query('1000 Jane St', datetime.now())
