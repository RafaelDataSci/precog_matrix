import urllib.parse
import urllib.request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from geopy.geocoders import GoogleV3
import urllib
#from model import predict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# http://127.0.0.1:8000/predict?...
@app.get("/predict")
def predict(address, crime_date):
    '''
        Make a single prediction
    '''
    city = 'Toronto'

    def get_lat_lon_google(address):
        geolocator = GoogleV3(api_key=GOOGLE_API_KEY)
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None

    latitude, longitude = get_lat_lon_google(address + ', ' + city)

    print(f'Lat : {latitude}, Long: {longitude}.')


#predict('5 Everson Drive, North York)
search = 'address=5 Everson Drive, North York&crime_date=2024-06-09%2006:19:08.378587'
search = urllib.parse.quote(search)
print(search)
