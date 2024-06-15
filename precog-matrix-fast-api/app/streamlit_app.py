import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.geocoders import GoogleV3
import requests
from datetime import datetime

# Streamlit configuration
st.set_page_config(page_title="Crime Prediction", page_icon="🔍", layout="wide")

# Function to geocode address
def geocode_address(address):
    geolocator = GoogleV3(api_key="GOOGLE_API_KEY")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# Function to call the prediction API
def predict_crime(address, crime_date):
    url = "http://localhost:8000/predict"
    params = {"address": address, "crime_date": crime_date.isoformat()}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("prediction")
    else:
        return None

# Streamlit UI
st.title("Crime Prediction")

# User input
address = st.text_input("Address", "Toronto City Hall 100 Queen St W")
crime_date = st.date_input("Crime Date", datetime.now())
crime_time = st.time_input("Crime Time", datetime.now().time())

# Prediction button
if st.button("Predict Crime"):
    lat, lon = geocode_address(address)
    if lat is not None and lon is not None:
        combined_datetime = datetime.combine(crime_date, crime_time)
        prediction = predict_crime(address, combined_datetime)
        if prediction:
            st.write("Crime Prediction Probabilities:")
            crime_labels = ["AUTO THEFT", "ASSAULT", "ROBBERY", "THEFT OVER", "BREAK AND ENTER", "HOMICIDE"]
            for crime, prob in zip(crime_labels, prediction[0]):
                st.write(f"{crime}: {prob:.2f}")
        else:
            st.error("Error fetching prediction. Please try again.")
    else:
        st.error("Could not geocode the provided address.")

# Interactive map
st.subheader("Click on the map to select a location")
map_center = [43.651070, -79.347015]  # Toronto center
map_obj = folium.Map(location=map_center, zoom_start=12)

# Add click event to map
map_obj.add_child(folium.LatLngPopup())

# Function to handle map click
if 'map_click' not in st.session_state:
    st.session_state.map_click = None

def on_map_click(e):
    st.session_state.map_click = e['latlng']

map_obj.add_child(folium.ClickForMarker(popup="You clicked here!"))

if st.session_state.map_click:
    st.write(f"You clicked at: {st.session_state.map_click}")

folium_static(map_obj)
