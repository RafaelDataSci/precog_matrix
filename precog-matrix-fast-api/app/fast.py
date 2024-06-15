from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from predict import main
from preproc import preproc, load_data, load_scaler
from geopy.geocoders import GoogleV3
from datetime import datetime
import logging

app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"]  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "PreCog Matrix"}

@app.get("/predict")
def predict_query(address: str, crime_date: str):
    try:
        city = 'Toronto'

        if not address:
            return {"error": "You must inform one address to predict"}

        crime_date = datetime.fromisoformat(crime_date)

        year = crime_date.year
        month = crime_date.month
        day = crime_date.day
        hour = crime_date.hour

        geolocator = GoogleV3(api_key="GOOGLE_API_KEY")
        location = geolocator.geocode(address + ', ' + city)
        if not location:
            return {"error": "Could not geocode address"}

        lat, long = location.latitude, location.longitude

        model_path = 'models/crime_prediction_lightgbm_model.joblib'
        df = load_data(lat, long, year, month, day, hour)
        scaler = load_scaler('models/scaler.joblib')
        df_processed = preproc(df, scaler)
        prediction = main(model_path, df_processed, ["AUTO THEFT", "ASSAULT", "ROBBERY", "THEFT OVER", "BREAK AND ENTER", "HOMICIDE"])

        return {"prediction": prediction.tolist()}
    except ValueError as e:
        logger.error(f"Error occurred: {e}")
        return {"error": "Invalid date format. Please use ISO 8601 format (YYYY-MM-DDTHH:MM:SS)."}
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return {"error": str(e)}
