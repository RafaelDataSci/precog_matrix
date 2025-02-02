from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from app.predict import main as predict_main
from app.preproc import preproc, load_data, load_scaler
from geopy.geocoders import GoogleV3
from datetime import datetime
import os
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

# Simple in-memory cache for geocoding results
geocode_cache = {}

def geocode_address(address):
    if address in geocode_cache:
        return geocode_cache[address]

    google_api_key = os.getenv("GOOGLE_API_KEY")
    logger.debug(f"Google API Key: {GOOGLE_API_KEY}")

    if not google_api_key:
        raise ValueError("Google API Key is not set.")

    geolocator = GoogleV3(api_key=GOOGLE_API_KEY)
    logger.debug(f"Geolocator: {geolocator}")

    try:
        location = geolocator.geocode(address)
        logger.debug(f"Geocode result: {location}")

        if location:
            geocode_cache[address] = (location.latitude, location.longitude)
            return location.latitude, location.longitude
        else:
            raise ValueError("Could not geocode the provided address.")
    except Exception as e:
        logger.error(f"Error during geocoding: {e}")
        raise ValueError(f"Error during geocoding: {e}")

@app.get("/")
def index():
    return {"greeting": "PreCog Matrix"}

@app.get("/predict")
def predict_query(address: str, crime_date: str):
    try:
        if not address:
            return {"error": "You must inform one address to predict"}

        crime_date = datetime.fromisoformat(crime_date)
        year, month, day, hour = crime_date.year, crime_date.month, crime_date.day, crime_date.hour

        lat, lon = geocode_address(address + ', Toronto')

        model_path = 'models/crime_prediction_lightgbm_model.joblib'
        df = load_data(lat, lon, year, month, day, hour)
        scaler = load_scaler('models/scaler.joblib')
        df_processed = preproc(df, scaler)
        prediction = predict_main(model_path, df_processed, ["AUTO THEFT", "ASSAULT", "ROBBERY", "THEFT OVER", "BREAK AND ENTER", "HOMICIDE"])

        return {"prediction": prediction.tolist()}
    except ValueError as e:
        logger.error(f"Error occurred: {e}")
        return {"error": str(e)}
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return {"error": str(e)}
