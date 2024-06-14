from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from app.predict import main
from app.preproc import preproc, load_data, load_scaler
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
    allow_headers=["*"])  # Allows all headers

@app.get("/")
def index():
    return {"greeting": "PreCog Matrix"}

#http://localhost:8000/predict?address=Toronto%20City%20Hall%20100%20Queen%20St%20W&crime_date=2024-06-09T10%3A04%3A57.047990
@app.get("/predict")
#def predict_query(address, crime_date: Optional[datetime] = datetime.now()):
def predict_query(address, crime_date):
    try:
        city = 'Toronto'

        if not address:
            return  {"error": "You must inform one address to predict"}

        if crime_date is None:
            crime_date = datetime.now()
        elif isinstance(crime_date, str):
            # Parse the crime_date string into a datetime object
            crime_date = datetime.fromisoformat(crime_date)

        year = crime_date.year
        month = crime_date.month
        day = crime_date.day
        hour = crime_date.hour

        def get_lat_lon_google(address):
            geolocator = GoogleV3(api_key=GOOGLE_API_KEY)
            location = geolocator.geocode(address)
            if location:
                return location.latitude, location.longitude
            else:
                return None, None
        lat, long = get_lat_lon_google(address + ', ' + city)
        if lat is None or long is None:
            return {"error": "Could not geocode address"}

        model_path = 'models/crime_prediction_lightgbm_model.joblib'
        onehot_columns = ['Crime_A', 'Crime_B', 'Crime_C', 'Crime_D', 'Crime_E', 'Crime_F']  # Tem que ajustar, pq não sei os nomes
        #print(lat, long, year, month, day, hour)
        df = load_data(lat, long, year, month, day, hour)
        scaler = load_scaler('models/scaler.joblib')
        df_processed = preproc(df, scaler)
        prediction =  main(model_path, df_processed, onehot_columns)
        return dict(prediction=prediction.tolist())
    except ValueError as e:
        logger.error(f"Error occurred: {e}")
        return {"error": "Invalid date format. Please use ISO 8601 format (YYYY-MM-DDTHH:MM:SS)."}
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return {"error": str(e)}
