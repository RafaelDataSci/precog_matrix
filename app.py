import streamlit as st
import folium
from streamlit_folium import folium_static
import requests
from datetime import datetime
import base64
import pandas as pd
import data_visualizations as dv

def coordinates(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': address,
        'format': 'json'
    }
    session = requests.Session()
    session.headers['User-Agent'] = 'Custom user agent'
    response = session.get(url, params=params).json()
    return float(response[0]['lat']), float(response[0]['lon'])

# Streamlit configuration
st.set_page_config(page_title="PreCog Matrix", page_icon="🚨", layout="wide")

# Function to call the prediction API
def predict_crime(address, crime_date):
    lat, lon = coordinates(address)
    url = "http://127.0.0.1:8000/predict"
    params = {"lat": lat, "lon": lon, "crime_date": crime_date.isoformat()}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("prediction"), (lat, lon)
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return None, None

# Function to convert image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Load custom CSS
def load_css():
    base64_image = image_to_base64("toronto.webp")
    st.markdown(
        f"""
        <style>
        body {{
            background-color: #121212;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .stApp {{
            background-color: #121212;
        }}
        .stButton>button {{
            border-radius: 8px;
            background-color: #1db954;
            color: white;
            border: none;
            padding: 0.5em 1em;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s;
        }}
        .stButton>button:hover {{
            background-color: #1ed760;
        }}
        .stTextInput>label, .stDateInput>label, .stTimeInput>label {{
            color: white !important;
        }}
        .stTextInput>div>input {{
            background-color: #1e1e1e;
            color: white;
            border: 1px solid #1db954;
            border-radius: 8px;
            padding: 0.5em;
            font-size: 1em;
        }}
        .stDateInput>div>div>input {{
            background-color: #1e1e1e;
            color: white;
            border: 1px solid #1db954;
            border-radius: 8px;
            padding: 0.5em;
            font-size: 1em;
        }}
        .stTimeInput>div>div>input {{
            background-color: #1e1e1e;
            color: white;
            border: 1px solid #1db954;
            border-radius: 8px;
            padding: 0.5em;
            font-size: 1em;
        }}
        .stMarkdown h1, .stMarkdown h2 {{
            text-align: center;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .stMarkdown h3 {{
            color: white;
        }}
        .footer {{
            text-align: center;
            color: #1db954;
            padding: 10px;
            background-color: #1e1e1e;
            border-top: 2px solid #1db954;
        }}
        .header {{
            background-image: url('data:image/webp;base64,{base64_image}');
            background-size: cover;
            background-position: center;
            height: 300px;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            position: relative;
            width: 100%;
            border-bottom: 4px solid #1db954;
        }}
        .header-content {{
            background-color: rgba(0, 0, 0, 0.8);
            padding: 10px;
            border-radius: 10px;
        }}
        .footer img {{
            width: 50px;
            height: 50px;
            border-radius: 50%;
            margin: 0 10px;
        }}
        .map-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
            width: 100%;
        }}
        .map {{
            width: 100%;
            height: 800px;
            max-width: 1600px;
        }}
        .input-container {{
            display: flex;
            justify-content: center;
            gap: 1em;
            margin-top: 20px;
            width: 100%;
            max-width: 1600px;
        }}
        .center-text {{
            text-align: center;
            width: 100%;
        }}
        .iframe-container {{
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }}

        .p{{

            font-color: #ffffff;

        }}

        .stHorizontalBlock {{
            display: flex;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
            width: 100%;
            max-width: 1600px;
            margin: 0 auto;
        }}
        .folium-map {{
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            max-width: 1600px;
            margin: 20px auto;
        }}

        .selectbox-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
        }}
        .selectbox {{
            width: 300px;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )

# Load the custom CSS
load_css()

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page:", ["Home", "Data Visualization", "Data Analysis"])

# Common Header
def render_header(title):
    st.markdown(
        f"""
        <div class="header">
            <div class="header-content">
                <h2>{title}</h2>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Footer
def render_footer():
    st.markdown(
        """
        <div class="footer">
            <p>A Machine Learning model developed by:</p>
                <p>
                <a href="https://github.com/AVMontanari"><img src="https://avatars.githubusercontent.com/u/82625842?s=400&u=7c9523d90f05fe46a75c2e7924cc46c0443e8daa&v=4" alt="André Valle Montanari"></a> André Valle Montanari
                <a href="https://github.com/mauromsilva"><img src="https://avatars.githubusercontent.com/u/116835043?s=96&v=4" alt="Mauro Moreira Silva"></a> Mauro Moreira Silva
                <a href="https://github.com/RafaelDataSci"><img src="https://avatars.githubusercontent.com/u/155320032?s=400&u=a67e1eb25d7e874654b21957f1cc2294a34939b3&v=4" alt="Rafael Quintanilha Ferreira"></a> Rafael Quintanilha Ferreira
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Home Page
if page == "Home":
    render_header("PreCog Matrix - A Machine Learning Model to Predict Crimes")

    # Streamlit UI
    st.markdown("<h3 style='text-align: center;'>Predicting Crimes in Toronto</h3>", unsafe_allow_html=True)

    # User input
    st.markdown('<div class="input-container stHorizontalBlock">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

    with col1:
        address = st.text_input("Address", "Toronto City Hall 100 Queen St W", help="Enter the address for crime prediction")
    with col2:
        crime_date = st.date_input("Crime Date", datetime.now(), help="Select the date of the crime")
    with col3:
        crime_time = st.time_input("Crime Time", datetime.now().time(), help="Select the time of the crime")
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        predict_button = st.button("Predict Crimes")

    st.markdown('</div>', unsafe_allow_html=True)

    if predict_button:
        combined_datetime = datetime.combine(crime_date, crime_time)
        prediction, coords = predict_crime(address, combined_datetime)

        if prediction:
            st.markdown("<h4 style='color: white; text-align: center;'>Crime Prediction Probabilities:</h4>", unsafe_allow_html=True)
            crime_labels = ["AUTO THEFT", "ASSAULT", "ROBBERY", "THEFT OVER", "BREAK AND ENTER", "HOMICIDE"]
            probabilities = [f"{prob:.2f}%" for prob in prediction[0]]
            df = pd.DataFrame({
                "Crime Type": crime_labels,
                "Probability": probabilities
            })
            st.markdown(
                df.to_html(index=False, justify='center').replace(
                    '<table',
                    '<table style="color: white; width: 50%; margin: auto; border-collapse: collapse;"'
                ).replace(
                    '<th>',
                    '<th style="border: 2px solid #1db954; padding: 8px;">'
                ).replace(
                    '<td>',
                    '<td style="border: 2px solid #1db954; padding: 8px;">'
                ),
                unsafe_allow_html=True
            )
        else:
            st.error("Error fetching prediction. Please try again.")

    # Interactive map
    st.markdown('<div class="center-text"><h4>Click on the Map to Select a Location</h4></div>', unsafe_allow_html=True)
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    map_center = [43.6426, -79.3871]  # CN Tower coordinates
    map_obj = folium.Map(location=map_center, zoom_start=12, control_scale=True)

    # Add click event to map
    if 'map_click' not in st.session_state:
        st.session_state.map_click = None

    def on_map_click(e):
        st.session_state.map_click = e['latlng']

    map_obj.add_child(folium.LatLngPopup())
    map_obj.add_child(folium.ClickForMarker(popup="You clicked here!"))

    # Add marker to the map after prediction
    if predict_button and coords:
        folium.Marker(location=coords, popup="Prediction Location").add_to(map_obj)

    folium_static(map_obj, width=1500, height=500)
    st.markdown('</div>', unsafe_allow_html=True)

    render_footer()

# Data Visualization Page
elif page == "Data Visualization":
    render_header("Data Visualization")
    st.markdown("<h3 style='text-align: center;'>Crimes Data Visualization</h3>", unsafe_allow_html=True)

    # Load your dataframe here
    dfmatrix_tratado = pd.read_csv("https://storage.googleapis.com/wagon-bootcamp-422319_cloudbuild/dfmatrix_tratado.csv")  # Replace with your actual data file

    # List of crime types
    crime_types = ["ASSAULT", "AUTO_THEFT", "BREAK_AND_ENTER", "HOMICIDE", "ROBBERY", "THEFT_OVER"]

     # Select a visualization to display
    st.markdown('<div class="selectbox-container">', unsafe_allow_html=True)
    visualization = st.selectbox(
        "Select a visualization:",
        ["Crimes by Hour", "Crimes by Year", "Crimes by Month", "Crimes by Day of the Week",
         "Crimes by Day of the Year", "Crimes by Day of the Month", "Crimes Correlation",
         "Heatmap for a Specific Crime", "Word Cloud for Day of the Week", "Period of the Day",
         "Period of the Month", "Period of the Week", "Year Categorization", "Crimes per Season",
         "Total Crime Count by Type"],
        key="visualization_selectbox",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Display the selected visualization
    if visualization == "Crimes by Hour":
        dv.plot_crimes_by_hour(dfmatrix_tratado, crime_types)
    elif visualization == "Crimes by Year":
        dv.plot_crimes_by_year(dfmatrix_tratado, crime_types)
    elif visualization == "Crimes by Month":
        dv.plot_crimes_by_month(dfmatrix_tratado, crime_types)
    elif visualization == "Crimes by Day of the Week":
        dv.plot_crimes_by_day_of_week(dfmatrix_tratado, crime_types)
    elif visualization == "Crimes by Day of the Year":
        dv.plot_crimes_by_day_of_year(dfmatrix_tratado, crime_types)
    elif visualization == "Crimes by Day of the Month":
        dv.plot_crimes_by_day_of_month(dfmatrix_tratado, crime_types)
    elif visualization == "Crimes Correlation":
        dv.plot_crimes_correlation(dfmatrix_tratado, crime_types)
    elif visualization == "Heatmap for a Specific Crime":
        crime_type = st.selectbox("Select a crime type:", crime_types)
        north_boundary = st.number_input("North Boundary", value=43.9)
        south_boundary = st.number_input("South Boundary", value=43.6)
        east_boundary = st.number_input("East Boundary", value=-79.2)
        west_boundary = st.number_input("West Boundary", value=-79.6)
        dv.create_heatmap(dfmatrix_tratado, crime_type, north_boundary, south_boundary, east_boundary, west_boundary)
    elif visualization == "Word Cloud for Day of the Week":
        dv.generate_wordcloud(dfmatrix_tratado, "OCC_DOW")
    elif visualization == "Period of the Day":
        dv.plot_period_of_the_day()
    elif visualization == "Period of the Month":
        dv.plot_period_of_the_month()
    elif visualization == "Period of the Week":
        dv.plot_period_of_the_week()
    elif visualization == "Year Categorization":
        dv.plot_year_categorization()
    elif visualization == "Crimes per Season":
        dv.plot_crimes_per_season()
    elif visualization == "Total Crime Count by Type":
        dv.plot_total_crime_count_by_type(dfmatrix_tratado, crime_types)

    render_footer()

# Data Analysis Page
elif page == "Data Analysis":
    render_header("Data Analysis")

    analyses = {
        "Homicide Analysis": "https://app.powerbi.com/view?r=eyJrIjoiNjc0NzFlZTktYjllMy00NmRjLWIyYzUtNDc4ZTE4M2FiYjg2IiwidCI6Ijg1MjljMjI1LWFjNDMtNDc0Yy04ZmI0LTBmNDA5NWFlOGQ1ZCIsImMiOjN9",
        "Assault Analysis": "https://app.powerbi.com/view?r=eyJrIjoiY2EwMTMyOTItMTRmZC00YzU1LTllNGEtZDgxZTRmNWE1MTg4IiwidCI6Ijg1MjljMjI1LWFjNDMtNDc0Yy04ZmI0LTBmNDA5NWFlOGQ1ZCIsImMiOjN9",
        "Auto Theft Analysis": "https://app.powerbi.com/view?r=eyJrIjoiNjA1YWE0ZGYtMTNmYi00ZGRhLTkzMjUtMTE1OTRjNjZmMjhlIiwidCI6Ijg1MjljMjI1LWFjNDMtNDc0Yy04ZmI0LTBmNDA5NWFlOGQ1ZCIsImMiOjN9",
        "Break and Enter Analysis": "https://app.powerbi.com/view?r=eyJrIjoiODBiMDE4ZGEtNTJlNy00OTAyLTlkNDctMWU0MjNjNzQ0MzJiIiwidCI6Ijg1MjljMjI1LWFjNDMtNDc0Yy04ZmI0LTBmNDA5NWFlOGQ1ZCIsImMiOjN9",
        "Robbery Analysis": "https://app.powerbi.com/view?r=eyJrIjoiYTJjY2E0YjMtZDljMi00YzlmLTljODItNzA2MGQ1MzMwYzgxIiwidCI6Ijg1MjljMjI1LWFjNDMtNDc0Yy04ZmI0LTBmNDA5NWFlOGQ1ZCIsImMiOjN9",
        "Theft Over Analysis": "https://app.powerbi.com/view?r=eyJrIjoiZTdkMjAxZTQtYWJjYy00MjhmLTk1MWMtN2ViMmJkZmJiNmM2IiwidCI6Ijg1MjljMjI1LWFjNDMtNDc0Yy04ZmI0LTBmNDA5NWFlOGQ1ZCIsImMiOjN9"
    }

    analysis_options = list(analyses.keys())
    selected_analysis = st.selectbox("Select an analysis to view:", analysis_options)

    st.markdown(f"<h3 style='text-align: center;'>{selected_analysis}</h3>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="iframe-container">
            <iframe title="{selected_analysis}" width="1140" height="541.25" src="{analyses[selected_analysis]}" frameborder="0" allowFullScreen="true"></iframe>
        </div>
        """,
                unsafe_allow_html=True,
    )

    # Add space before the footer
    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

    render_footer()







# import streamlit as st
# import folium
# from streamlit_folium import folium_static
# import requests
# from datetime import datetime
# import base64
# import pandas as pd
# import data_visualizations as dv

# def coordinates(address):
#     url = "https://nominatim.openstreetmap.org/search"
#     params = {
#         'q': address,
#         'format': 'json'
#     }
#     session = requests.Session()
#     session.headers['User-Agent'] = 'Custom user agent'
#     response = session.get(url, params=params).json()
#     return float(response[0]['lat']), float(response[0]['lon'])

# # Streamlit configuration
# st.set_page_config(page_title="PreCog Matrix", page_icon="🚨", layout="wide")

# # Function to call the prediction API
# def predict_crime(address, crime_date):
#     lat, lon = coordinates(address)
#     url = "http://127.0.0.1:8000/predict"
#     params = {"lat": lat, "lon": lon, "crime_date": crime_date.isoformat()}
#     try:
#         response = requests.get(url, params=params)
#         response.raise_for_status()
#         return response.json().get("prediction"), (lat, lon)
#     except requests.exceptions.RequestException as e:
#         st.error(f"API request failed: {e}")
#         return None, None

# # Function to convert image to base64
# def image_to_base64(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode()

# # Load custom CSS
# def load_css():
#     base64_image = image_to_base64("toronto.webp")
#     st.markdown(
#         f"""
#         <style>
#         body {{
#             background-color: #121212;
#             color: white;
#             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#         }}
#         .stApp {{
#             background-color: #121212;
#         }}
#         .stButton>button {{
#             border-radius: 8px;
#             background-color: #1db954;
#             color: white;
#             border: none;
#             padding: 0.5em 1em;
#             font-size: 1em;
#             font-weight: bold;
#             cursor: pointer;
#             transition: background-color 0.3s;
#         }}
#         .stButton>button:hover {{
#             background-color: #1ed760;
#         }}
#         .stTextInput>label, .stDateInput>label, .stTimeInput>label {{
#             color: white !important;
#         }}
#         .stTextInput>div>input {{
#             background-color: #1e1e1e;
#             color: white;
#             border: 1px solid #1db954;
#             border-radius: 8px;
#             padding: 0.5em;
#             font-size: 1em;
#         }}
#         .stDateInput>div>div>input {{
#             background-color: #1e1e1e;
#             color: white;
#             border: 1px solid #1db954;
#             border-radius: 8px;
#             padding: 0.5em;
#             font-size: 1em;
#         }}
#         .stTimeInput>div>div>input {{
#             background-color: #1e1e1e;
#             color: white;
#             border: 1px solid #1db954;
#             border-radius: 8px;
#             padding: 0.5em;
#             font-size: 1em;
#         }}
#         .stMarkdown h1, .stMarkdown h2 {{
#             text-align: center;
#             color: white;
#             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#         }}
#         .stMarkdown h3 {{
#             color: white;
#         }}
#         .footer {{
#             text-align: center;
#             color: #1db954;
#             padding: 10px;
#             background-color: #1e1e1e;
#             border-top: 2px solid #1db954;
#         }}
#         .header {{
#             background-image: url('data:image/webp;base64,{base64_image}');
#             background-size: cover;
#             background-position: center;
#             height: 300px;
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             flex-direction: column;
#             position: relative;
#             width: 100%;
#             border-bottom: 4px solid #1db954;
#         }}
#         .header-content {{
#             background-color: rgba(0, 0, 0, 0.8);
#             padding: 10px;
#             border-radius: 10px;
#         }}
#         .footer img {{
#             width: 50px;
#             height: 50px;
#             border-radius: 50%;
#             margin: 0 10px;
#         }}
#         .map-container {{
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             margin-top: 20px;
#             width: 100%;
#         }}
#         .map {{
#             width: 100%;
#             height: 800px;
#             max-width: 1600px;
#         }}
#         .input-container {{
#             display: flex;
#             justify-content: center;
#             gap: 1em;
#             margin-top: 20px;
#             width: 100%;
#             max-width: 1600px;
#         }}
#         .center-text {{
#             text-align: center;
#             width: 100%;
#         }}
#         .iframe-container {{
#             display: flex;
#             justify-content: center;
#             margin-top: 20px;
#         }}

#         .p{{

#             font-color: #ffffff;

#         }}

#         .stHorizontalBlock {{
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             flex-wrap: wrap;
#             width: 100%;
#             max-width: 1600px;
#             margin: 0 auto;
#         }}
#         .folium-map {{
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             width: 100%;
#             max-width: 1600px;
#             margin: 20px auto;
#         }}

#         .selectbox-container {{
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             margin-top: 20px;
#         }}
#         .selectbox {{
#             width: 300px;
#         }}

#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

# # Load the custom CSS
# load_css()

# # Sidebar for navigation
# st.sidebar.title("Navigation")
# page = st.sidebar.selectbox("Select a page:", ["Home", "Data Visualization", "Data Analysis"])

# # Common Header
# def render_header(title):
#     st.markdown(
#         f"""
#         <div class="header">
#             <div class="header-content">
#                 <h2>{title}</h2>
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

# # Footer
# def render_footer():
#     st.markdown(
#         """
#         <div class="footer">
#             <p>A Machine Learning model developed by:</p>
#                 <p>
#                 <a href="https://github.com/AVMontanari"><img src="https://avatars.githubusercontent.com/u/82625842?s=400&u=7c9523d90f05fe46a75c2e7924cc46c0443e8daa&v=4" alt="André Valle Montanari"></a> André Valle Montanari
#                 <a href="https://github.com/mauromsilva"><img src="https://avatars.githubusercontent.com/u/116835043?s=96&v=4" alt="Mauro Moreira Silva"></a> Mauro Moreira Silva
#                 <a href="https://github.com/RafaelDataSci"><img src="https://avatars.githubusercontent.com/u/155320032?s=400&u=a67e1eb25d7e874654b21957f1cc2294a34939b3&v=4" alt="Rafael Quintanilha Ferreira"></a> Rafael Quintanilha Ferreira
#             </p>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

# # Home Page
# if page == "Home":
#     render_header("PreCog Matrix - A Machine Learning Model to Predict Crimes")

#     # Streamlit UI
#     st.markdown("<h3 style='text-align: center;'>Predicting Crimes in Toronto</h3>", unsafe_allow_html=True)

#     # User input
#     st.markdown('<div class="input-container stHorizontalBlock">', unsafe_allow_html=True)
#     col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

#     with col1:
#         address = st.text_input("Address", "Toronto City Hall 100 Queen St W", help="Enter the address for crime prediction")
#     with col2:
#         crime_date = st.date_input("Crime Date", datetime.now(), help="Select the date of the crime")
#     with col3:
#         crime_time = st.time_input("Crime Time", datetime.now().time(), help="Select the time of the crime")
#     with col4:
#         st.markdown("<br>", unsafe_allow_html=True)
#         predict_button = st.button("Predict Crimes")

#     st.markdown('</div>', unsafe_allow_html=True)

#     if predict_button:
#         combined_datetime = datetime.combine(crime_date, crime_time)
#         prediction, coords = predict_crime(address, combined_datetime)

#         if prediction:
#             st.markdown("<h4 style='color: white; text-align: center;'>Crime Prediction Probabilities:</h4>", unsafe_allow_html=True)
#             crime_labels = ["AUTO THEFT", "ASSAULT", "ROBBERY", "THEFT OVER", "BREAK AND ENTER", "HOMICIDE"]
#             probabilities = [f"{prob:.2f}%" for prob in prediction[0]]
#             df = pd.DataFrame({
#                 "Crime Type": crime_labels,
#                 "Probability": probabilities
#             })
#             st.markdown(
#                 df.to_html(index=False, justify='center').replace(
#                     '<table',
#                     '<table style="color: white; width: 50%; margin: auto; border-collapse: collapse;"'
#                 ).replace(
#                     '<th>',
#                     '<th style="border: 2px solid #1db954; padding: 8px;">'
#                 ).replace(
#                     '<td>',
#                     '<td style="border: 2px solid #1db954; padding: 8px;">'
#                 ),
#                 unsafe_allow_html=True
#             )
#         else:
#             st.error("Error fetching prediction. Please try again.")

#     # Interactive map
#     st.markdown('<div class="center-text"><h3>Click on the Map to Select a Location</h3></div>', unsafe_allow_html=True)
#     st.markdown('<div class="map-container">', unsafe_allow_html=True)
#     map_center = [43.6426, -79.3871]  # CN Tower coordinates
#     map_obj = folium.Map(location=map_center, zoom_start=12, control_scale=True)

#     # Add click event to map
#     if 'map_click' not in st.session_state:
#         st.session_state.map_click = None

#     def on_map_click(e):
#         st.session_state.map_click = e['latlng']

#     map_obj.add_child(folium.LatLngPopup())
#     map_obj.add_child(folium.ClickForMarker(popup="You clicked here!"))

#     # Add marker to the map after prediction
#     if predict_button and coords:
#         folium.Marker(location=coords, popup="Prediction Location").add_to(map_obj)

#     folium_static(map_obj, width=1000, height=500)
#     st.markdown('</div>', unsafe_allow_html=True)

#     render_footer()

# # Data Visualization Page
# elif page == "Data Visualization":
#     render_header("Data Visualization")
#     st.markdown("<h3 style='text-align: center;'>Crimes Data Visualization</h3>", unsafe_allow_html=True)

#     # Load your dataframe here
#     dfmatrix_tratado = pd.read_csv("raw_data/dfmatrix_tratado.csv")  # Replace with your actual data file

#     # List of crime types
#     crime_types = ["ASSAULT", "AUTO THEFT", "BREAK AND ENTER", "HOMICIDE", "ROBBERY", "THEFT OVER"]

#      # Select a visualization to display
#     st.markdown('<div class="selectbox-container">', unsafe_allow_html=True)
#     visualization = st.selectbox(
#         "Select a visualization:",
#         ["Crimes by Hour", "Crimes by Year", "Crimes by Month", "Crimes by Day of the Week",
#          "Crimes by Day of the Year", "Crimes by Day of the Month", "Crimes Correlation",
#          "Heatmap for a Specific Crime", "Word Cloud for Day of the Week", "Period of the Day",
#          "Period of the Month", "Period of the Week", "Year Categorization", "Crimes per Season",
#          "Total Crime Count by Type"],
#         key="visualization_selectbox",
#     )
#     st.markdown('</div>', unsafe_allow_html=True)

#     # Display the selected visualization
#     if visualization == "Crimes by Hour":
#         dv.plot_crimes_by_hour(dfmatrix_tratado, crime_types)
#     elif visualization == "Crimes by Year":
#         dv.plot_crimes_by_year(dfmatrix_tratado, crime_types)
#     elif visualization == "Crimes by Month":
#         dv.plot_crimes_by_month(dfmatrix_tratado, crime_types)
#     elif visualization == "Crimes by Day of the Week":
#         dv.plot_crimes_by_day_of_week(dfmatrix_tratado, crime_types)
#     elif visualization == "Crimes by Day of the Year":
#         dv.plot_crimes_by_day_of_year(dfmatrix_tratado, crime_types)
#     elif visualization == "Crimes by Day of the Month":
#         dv.plot_crimes_by_day_of_month(dfmatrix_tratado, crime_types)
#     elif visualization == "Crimes Correlation":
#         dv.plot_crimes_correlation(dfmatrix_tratado, crime_types)
#     elif visualization == "Heatmap for a Specific Crime":
#         crime_type = st.selectbox("Select a crime type:", crime_types)
#         north_boundary = st.number_input("North Boundary", value=43.9)
#         south_boundary = st.number_input("South Boundary", value=43.6)
#         east_boundary = st.number_input("East Boundary", value=-79.2)
#         west_boundary = st.number_input("West Boundary", value=-79.6)
#         dv.create_heatmap(dfmatrix_tratado, crime_type, north_boundary, south_boundary, east_boundary, west_boundary)
#     elif visualization == "Word Cloud for Day of the Week":
#         dv.generate_wordcloud(dfmatrix_tratado, "OCC_DOW")
#     elif visualization == "Period of the Day":
#         dv.plot_period_of_the_day()
#     elif visualization == "Period of the Month":
#         dv.plot_period_of_the_month()
#     elif visualization == "Period of the Week":
#         dv.plot_period_of_the_week()
#     elif visualization == "Year Categorization":
#         dv.plot_year_categorization()
#     elif visualization == "Crimes per Season":
#         dv.plot_crimes_per_season()
#     elif visualization == "Total Crime Count by Type":
#         dv.plot_total_crime_count_by_type(dfmatrix_tratado, crime_types)

#     render_footer()

# # Data Analysis Page
# elif page == "Data Analysis":
#     render_header("Data Analysis")

#     analyses = {
#         "Homicide Analysis": "https://app.powerbi.com/view?r=eyJrIjoiNjc0NzFlZTktYjllMy00NmRjLWIyYzUtNDc4ZTE4M2FiYjg2IiwidCI6Ijg1MjljMjI1LWFjNDMtNDc0Yy04ZmI0LTBmNDA5NWFlOGQ1ZCIsImMiOjN9",
#         "Assault Analysis": "https://app.powerbi.com/view?r=eyJrIjoiY2EwMTMyOTItMTRmZC00YzU1LTllNGEtZDgxZTRmNWE1MTg4IiwidCI6Ijg1MjljMjI1LWFjNDMtNDc0Yy04ZmI0LTBmNDA5NWFlOGQ1ZCIsImMiOjN9",
#         "Auto Theft Analysis": "https://app.powerbi.com/view?r=eyJrIjoiNjA1YWE0ZGYtMTNmYi00ZGRhLTkzMjUtMTE1OTRjNjZmMjhlIiwidCI6Ijg1MjljMjI1LWFjNDMtNDc0Yy04ZmI0LTBmNDA5NWFlOGQ1ZCIsImMiOjN9",
#         "Break and Enter Analysis": "https://app.powerbi.com/view?r=eyJrIjoiODBiMDE4ZGEtNTJlNy00OTAyLTlkNDctMWU0MjNjNzQ0MzJiIiwidCI6Ijg1MjljMjI1LWFjNDMtNDc0Yy04ZmI0LTBmNDA5NWFlOGQ1ZCIsImMiOjN9",
#         "Robbery Analysis": "https://app.powerbi.com/view?r=eyJrIjoiYTJjY2E0YjMtZDljMi00YzlmLTljODItNzA2MGQ1MzMwYzgxIiwidCI6Ijg1MjljMjI1LWFjNDMtNDc0Yy04ZmI0LTBmNDA5NWFlOGQ1ZCIsImMiOjN9",
#         "Theft Over Analysis": "https://app.powerbi.com/view?r=eyJrIjoiZTdkMjAxZTQtYWJjYy00MjhmLTk1MWMtN2ViMmJkZmJiNmM2IiwidCI6Ijg1MjljMjI1LWFjNDMtNDc0Yy04ZmI0LTBmNDA5NWFlOGQ1ZCIsImMiOjN9"
#     }

#     analysis_options = list(analyses.keys())
#     selected_analysis = st.selectbox("Select an analysis to view:", analysis_options)

#     st.markdown(f"<h3 style='text-align: center;'>{selected_analysis}</h3>", unsafe_allow_html=True)
#     st.markdown(
#         f"""
#         <div class="iframe-container">
#             <iframe title="{selected_analysis}" width="1140" height="541.25" src="{analyses[selected_analysis]}" frameborder="0" allowFullScreen="true"></iframe>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     # Add space before the footer
#     st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

#     render_footer()







# import streamlit as st
# import folium
# from streamlit_folium import folium_static
# import requests
# from datetime import datetime
# import base64
# import pandas as pd
# import data_visualizations as dv

# def coordinates(address):
#     url = "https://nominatim.openstreetmap.org/search"
#     params = {
#         'q': address,
#         'format': 'json'
#     }
#     session = requests.Session()
#     session.headers['User-Agent'] = 'Custom user agent'
#     response = session.get(url, params=params).json()
#     return float(response[0]['lat']), float(response[0]['lon'])

# # Streamlit configuration
# st.set_page_config(page_title="PreCog Matrix", page_icon="🚨", layout="wide")

# # Function to call the prediction API
# def predict_crime(address, crime_date):
#     lat, lon = coordinates(address)
#     url = "http://127.0.0.1:8000/predict"
#     params = {"lat": lat, "lon": lon, "crime_date": crime_date.isoformat()}
#     try:
#         response = requests.get(url, params=params)
#         response.raise_for_status()
#         return response.json().get("prediction"), (lat, lon)
#     except requests.exceptions.RequestException as e:
#         st.error(f"API request failed: {e}")
#         return None, None

# # Function to convert image to base64
# def image_to_base64(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode()

# # Load custom CSS
# def load_css():
#     base64_image = image_to_base64("toronto.webp")
#     st.markdown(
#         f"""
#         <style>
#         body {{
#             background-color: #121212;
#             color: white;
#             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#         }}
#         .stApp {{
#             background-color: #121212;
#         }}
#         .stButton>button {{
#             border-radius: 8px;
#             background-color: #1db954;
#             color: white;
#             border: none;
#             padding: 0.5em 1em;
#             font-size: 1em;
#             font-weight: bold;
#             cursor: pointer;
#             transition: background-color 0.3s;
#         }}
#         .stButton>button:hover {{
#             background-color: #1ed760;
#         }}
#         .stTextInput>label, .stDateInput>label, .stTimeInput>label {{
#             color: white !important;
#         }}
#         .stTextInput>div>input {{
#             background-color: #1e1e1e;
#             color: white;
#             border: 1px solid #1db954;
#             border-radius: 8px;
#             padding: 0.5em;
#             font-size: 1em;
#         }}
#         .stDateInput>div>div>input {{
#             background-color: #1e1e1e;
#             color: white;
#             border: 1px solid #1db954;
#             border-radius: 8px;
#             padding: 0.5em;
#             font-size: 1em;
#         }}
#         .stTimeInput>div>div>input {{
#             background-color: #1e1e1e;
#             color: white;
#             border: 1px solid #1db954;
#             border-radius: 8px;
#             padding: 0.5em;
#             font-size: 1em;
#         }}
#         .stMarkdown h1, .stMarkdown h2 {{
#             text-align: center;
#             color: white;
#             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#         }}
#         .stMarkdown h3 {{
#             color: white;
#         }}
#         .footer {{
#             text-align: center;
#             color: #1db954;
#             padding: 10px;
#             background-color: #1e1e1e;
#             border-top: 2px solid #1db954;
#         }}
#         .header {{
#             background-image: url('data:image/webp;base64,{base64_image}');
#             background-size: cover;
#             background-position: center;
#             height: 300px;
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             flex-direction: column;
#             position: relative;
#             width: 100%;
#             border-bottom: 4px solid #1db954;
#         }}
#         .header-content {{
#             background-color: rgba(0, 0, 0, 0.8);
#             padding: 10px;
#             border-radius: 10px;
#         }}
#         .footer img {{
#             width: 50px;
#             height: 50px;
#             border-radius: 50%;
#             margin: 0 10px;
#         }}
#         .map-container {{
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             margin-top: 20px;
#             width: 100%;
#         }}
#         .map {{
#             width: 100%;
#             height: 800px;
#             max-width: 1600px;
#         }}
#         .input-container {{
#             display: flex;
#             justify-content: center;
#             gap: 1em;
#             margin-top: 20px;
#             width: 100%;
#             max-width: 1600px;
#         }}
#         .center-text {{
#             text-align: center;
#             width: 100%;
#         }}
#         .iframe-container {{
#             display: flex;
#             justify-content: center;
#             margin-top: 20px;
#         }}

#         .p{{

#             font-color: #ffffff;

#         }}

#         .stHorizontalBlock {{
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             flex-wrap: wrap;
#             width: 100%;
#             max-width: 1600px;
#             margin: 0 auto;
#         }}
#         .folium-map {{
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             width: 100%;
#             max-width: 1600px;
#             margin: 20px auto;
#         }}

#         .selectbox-container {{
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             margin-top: 20px;
#         }}
#         .selectbox {{
#             width: 300px;
#         }}


#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

# # Load the custom CSS
# load_css()

# # Sidebar for navigation
# st.sidebar.title("Navigation")
# page = st.sidebar.selectbox("Select a page:", ["Home", "Data Visualization", "Data Analysis"])

# # Common Header
# def render_header(title):
#     st.markdown(
#         f"""
#         <div class="header">
#             <div class="header-content">
#                 <h2>{title}</h2>
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

# # Footer
# def render_footer():
#     st.markdown(
#         """
#         <div class="footer">
#             <p>A Machine Learning model developed by:</p>
#                 <p>
#                 <a href="https://github.com/AVMontanari"><img src="https://avatars.githubusercontent.com/u/82625842?s=400&u=7c9523d90f05fe46a75c2e7924cc46c0443e8daa&v=4" alt="André Valle Montanari"></a> André Valle Montanari
#                 <a href="https://github.com/mauromsilva"><img src="https://avatars.githubusercontent.com/u/116835043?s=96&v=4" alt="Mauro Moreira Silva"></a> Mauro Moreira Silva
#                 <a href="https://github.com/RafaelDataSci"><img src="https://avatars.githubusercontent.com/u/155320032?s=400&u=a67e1eb25d7e874654b21957f1cc2294a34939b3&v=4" alt="Rafael Quintanilha Ferreira"></a> Rafael Quintanilha Ferreira
#             </p>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

# # Home Page
# if page == "Home":
#     render_header("PreCog Matrix - A Machine Learning Model to Predict Crimes")

#     # Streamlit UI
#     st.markdown("<h3 style='text-align: center;'>Predicting Crimes in Toronto</h3>", unsafe_allow_html=True)

#     # User input
#     st.markdown('<div class="input-container stHorizontalBlock">', unsafe_allow_html=True)
#     col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

#     with col1:
#         address = st.text_input("Address", "Toronto City Hall 100 Queen St W", help="Enter the address for crime prediction")
#     with col2:
#         crime_date = st.date_input("Crime Date", datetime.now(), help="Select the date of the crime")
#     with col3:
#         crime_time = st.time_input("Crime Time", datetime.now().time(), help="Select the time of the crime")
#     with col4:
#         st.markdown("<br>", unsafe_allow_html=True)
#         predict_button = st.button("Predict Crimes")

#     st.markdown('</div>', unsafe_allow_html=True)

#     if predict_button:
#         combined_datetime = datetime.combine(crime_date, crime_time)
#         prediction, coords = predict_crime(address, combined_datetime)

#         if prediction:
#             st.markdown("<h4 style='color: white; text-align: center;'>Crime Prediction Probabilities:</h4>", unsafe_allow_html=True)
#             crime_labels = ["AUTO THEFT", "ASSAULT", "ROBBERY", "THEFT OVER", "BREAK AND ENTER", "HOMICIDE"]
#             probabilities = [f"{prob:.2f}%" for prob in prediction[0]]
#             df = pd.DataFrame({
#                 "Crime Type": crime_labels,
#                 "Probability": probabilities
#             })
#             st.markdown(
#                 df.to_html(index=False, justify='center').replace(
#                     '<table',
#                     '<table style="color: white; width: 50%; margin: auto; border-collapse: collapse;"'
#                 ).replace(
#                     '<th>',
#                     '<th style="border: 2px solid #1db954; padding: 8px;">'
#                 ).replace(
#                     '<td>',
#                     '<td style="border: 2px solid #1db954; padding: 8px;">'
#                 ),
#                 unsafe_allow_html=True
#             )
#         else:
#             st.error("Error fetching prediction. Please try again.")

#     # Interactive map
#     st.markdown('<div class="center-text"><h3>Click on the Map to Select a Location</h3></div>', unsafe_allow_html=True)
#     st.markdown('<div class="map-container">', unsafe_allow_html=True)
#     map_center = [43.6426, -79.3871]  # CN Tower coordinates
#     map_obj = folium.Map(location=map_center, zoom_start=12, control_scale=True)

#     # Add click event to map
#     if 'map_click' not in st.session_state:
#         st.session_state.map_click = None

#     def on_map_click(e):
#         st.session_state.map_click = e['latlng']

#     map_obj.add_child(folium.LatLngPopup())
#     map_obj.add_child(folium.ClickForMarker(popup="You clicked here!"))

#     # Add marker to the map after prediction
#     if predict_button and coords:
#         folium.Marker(location=coords, popup="Prediction Location").add_to(map_obj)

#     folium_static(map_obj, width=1000, height=500)
#     st.markdown('</div>', unsafe_allow_html=True)

#     render_footer()

# # Data Visualization Page
# elif page == "Data Visualization":
#     render_header("Data Visualization")
#     st.markdown("<h3 style='text-align: center;'>Crimes Data Visualization</h3>", unsafe_allow_html=True)

#     # Load your dataframe here
#     dfmatrix = pd.read_csv("raw_data/dfmatrix.csv")  # Replace with your actual data file

#     # List of crime types
#     crime_types = ["ASSAULT", "AUTO THEFT", "BREAK AND ENTER", "HOMICIDE", "ROBBERY", "THEFT OVER"]

#      # Select a visualization to display
#     st.markdown('<div class="selectbox-container">', unsafe_allow_html=True)
#     visualization = st.selectbox(
#         "Select a visualization:",
#         ["Crimes by Hour", "Crimes by Year", "Crimes by Month", "Crimes by Day of the Week",
#          "Crimes by Day of the Year", "Crimes by Day of the Month", "Crimes Correlation",
#          "Heatmap for a Specific Crime", "Word Cloud for Day of the Week", "Period of the Day",
#          "Period of the Month", "Period of the Week", "Year Categorization", "Crimes per Season",
#          "Total Crime Count by Type"],
#         key="visualization_selectbox",
#     )
#     st.markdown('</div>', unsafe_allow_html=True)

#     # Display the selected visualization
#     if visualization == "Crimes by Hour":
#         dv.plot_crimes_by_hour(dfmatrix, crime_types)
#     elif visualization == "Crimes by Year":
#         dv.plot_crimes_by_year(dfmatrix, crime_types)
#     elif visualization == "Crimes by Month":
#         dv.plot_crimes_by_month(dfmatrix, crime_types)
#     elif visualization == "Crimes by Day of the Week":
#         dv.plot_crimes_by_day_of_week(dfmatrix, crime_types)
#     elif visualization == "Crimes by Day of the Year":
#         dv.plot_crimes_by_day_of_year(dfmatrix, crime_types)
#     elif visualization == "Crimes by Day of the Month":
#         dv.plot_crimes_by_day_of_month(dfmatrix, crime_types)
#     elif visualization == "Crimes Correlation":
#         dv.plot_crimes_correlation(dfmatrix, crime_types)
#     elif visualization == "Heatmap for a Specific Crime":
#         crime_type = st.selectbox("Select a crime type:", crime_types)
#         north_boundary = st.number_input("North Boundary", value=43.9)
#         south_boundary = st.number_input("South Boundary", value=43.6)
#         east_boundary = st.number_input("East Boundary", value=-79.2)
#         west_boundary = st.number_input("West Boundary", value=-79.6)
#         dv.create_heatmap(dfmatrix, crime_type, north_boundary, south_boundary, east_boundary, west_boundary)
#     elif visualization == "Word Cloud for Day of the Week":
#         dv.generate_wordcloud(dfmatrix, "OCC_DOW")
#     elif visualization == "Period of the Day":
#         dv.plot_period_of_the_day()
#     elif visualization == "Period of the Month":
#         dv.plot_period_of_the_month()
#     elif visualization == "Period of the Week":
#         dv.plot_period_of_the_week()
#     elif visualization == "Year Categorization":
#         dv.plot_year_categorization()
#     elif visualization == "Crimes per Season":
#         dv.plot_crimes_per_season()
#     elif visualization == "Total Crime Count by Type":
#         dv.plot_total_crime_count_by_type(dfmatrix, crime_types)

#     render_footer()

# # Data Analysis Page
# elif page == "Data Analysis":
#     render_header("Data Analysis")

#     analyses = {
#         "Homicide Analysis": "https://app.powerbi.com/view?r=eyJrIjoiNjc0NzFlZTktYjllMy00NmRjLWIyYzUtNDc4ZTE4M2FiYjg2IiwidCI6Ijg1MjljMjI1LWFjNDMtNDc0Yy04ZmI0LTBmNDA5NWFlOGQ1ZCIsImMiOjN9",
#         "Assault Analysis": "https://app.powerbi.com/view?r=eyJrIjoiY2EwMTMyOTItMTRmZC00YzU1LTllNGEtZDgxZTRmNWE1MTg4IiwidCI6Ijg1MjljMjI1LWFjNDMtNDc0Yy04ZmI0LTBmNDA5NWFlOGQ1ZCIsImMiOjN9",
#         "Auto Theft Analysis": "https://app.powerbi.com/view?r=eyJrIjoiNjA1YWE0ZGYtMTNmYi00ZGRhLTkzMjUtMTE1OTRjNjZmMjhlIiwidCI6Ijg1MjljMjI1LWFjNDMtNDc0Yy04ZmI0LTBmNDA5NWFlOGQ1ZCIsImMiOjN9",
#         "Break and Enter Analysis": "https://app.powerbi.com/view?r=eyJrIjoiODBiMDE4ZGEtNTJlNy00OTAyLTlkNDctMWU0MjNjNzQ0MzJiIiwidCI6Ijg1MjljMjI1LWFjNDMtNDc0Yy04ZmI0LTBmNDA5NWFlOGQ1ZCIsImMiOjN9",
#         "Robbery Analysis": "https://app.powerbi.com/view?r=eyJrIjoiYTJjY2E0YjMtZDljMi00YzlmLTljODItNzA2MGQ1MzMwYzgxIiwidCI6Ijg1MjljMjI1LWFjNDMtNDc0Yy04ZmI0LTBmNDA5NWFlOGQ1ZCIsImMiOjN9",
#         "Theft Over Analysis": "https://app.powerbi.com/view?r=eyJrIjoiZTdkMjAxZTQtYWJjYy00MjhmLTk1MWMtN2ViMmJkZmJiNmM2IiwidCI6Ijg1MjljMjI1LWFjNDMtNDc0Yy04ZmI0LTBmNDA5NWFlOGQ1ZCIsImMiOjN9"
#     }

#     analysis_options = list(analyses.keys())
#     selected_analysis = st.selectbox("Select an analysis to view:", analysis_options)

#     st.markdown(f"<h3 style='text-align: center;'>{selected_analysis}</h3>", unsafe_allow_html=True)
#     st.markdown(
#         f"""
#         <div class="iframe-container">
#             <iframe title="{selected_analysis}" width="1140" height="541.25" src="{analyses[selected_analysis]}" frameborder="0" allowFullScreen="true"></iframe>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     # Add space before the footer
#     st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

#     render_footer()















# # import streamlit as st
# # import folium
# # from streamlit_folium import folium_static
# # import requests
# # from datetime import datetime
# # import base64
# # import pandas as pd
# # import data_visualizations as dv


# # def coordinates(address):
# #     url = "https://nominatim.openstreetmap.org/search"
# #     params = {
# #         'q': address,
# #         'format': 'json'
# #     }
# #     session = requests.Session()
# #     session.headers['User-Agent'] = 'Custom user agent'
# #     response = session.get(url, params=params).json()
# #     return float(response[0]['lat']), float(response[0]['lon'])

# # # Streamlit configuration
# # st.set_page_config(page_title="PreCog Matrix", page_icon="🚨", layout="wide")

# # # Function to call the prediction API
# # def predict_crime(address, crime_date):
# #     lat, lon = coordinates(address)
# #     url = "http://127.0.0.1:8000/predict"
# #     params = {"lat": lat, "lon": lon, "crime_date": crime_date.isoformat()}
# #     try:
# #         response = requests.get(url, params=params)
# #         response.raise_for_status()
# #         return response.json().get("prediction"), (lat, lon)
# #     except requests.exceptions.RequestException as e:
# #         st.error(f"API request failed: {e}")
# #         return None, None

# # # Function to convert image to base64
# # def image_to_base64(image_path):
# #     with open(image_path, "rb") as image_file:
# #         return base64.b64encode(image_file.read()).decode()

# # # Load custom CSS
# # def load_css():
# #     base64_image = image_to_base64("toronto.webp")
# #     st.markdown(
# #         f"""
# #         <style>
# #         body {{
# #             background-color: #121212;
# #             color: white;
# #             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
# #         }}
# #         .stApp {{
# #             background-color: #121212;
# #         }}
# #         .stButton>button {{
# #             border-radius: 8px;
# #             background-color: #1db954;
# #             color: white;
# #             border: none;
# #             padding: 0.5em 1em;
# #             font-size: 1em;
# #             font-weight: bold;
# #             cursor: pointer;
# #             transition: background-color 0.3s;
# #         }}
# #         .stButton>button:hover {{
# #             background-color: #1ed760;
# #         }}
# #         .stTextInput>label, .stDateInput>label, .stTimeInput>label {{
# #             color: white !important;
# #         }}
# #         .stTextInput>div>input {{
# #             background-color: #1e1e1e;
# #             color: white;
# #             border: 1px solid #1db954;
# #             border-radius: 8px;
# #             padding: 0.5em;
# #             font-size: 1em;
# #         }}
# #         .stDateInput>div>div>input {{
# #             background-color: #1e1e1e;
# #             color: white;
# #             border: 1px solid #1db954;
# #             border-radius: 8px;
# #             padding: 0.5em;
# #             font-size: 1em;
# #         }}
# #         .stTimeInput>div>div>input {{
# #             background-color: #1e1e1e;
# #             color: white;
# #             border: 1px solid #1db954;
# #             border-radius: 8px;
# #             padding: 0.5em;
# #             font-size: 1em;
# #         }}
# #         .stMarkdown h1, .stMarkdown h2 {{
# #             text-align: center;
# #             color: white;
# #             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
# #         }}
# #         .stMarkdown h3 {{
# #             color: white;
# #         }}
# #         .footer {{
# #             text-align: center;
# #             color: #1db954;
# #             padding: 10px;
# #             background-color: #1e1e1e;
# #             border-top: 2px solid #1db954;
# #         }}
# #         .header {{
# #             background-image: url('data:image/webp;base64,{base64_image}');
# #             background-size: cover;
# #             background-position: center;
# #             height: 300px;
# #             display: flex;
# #             justify-content: center;
# #             align-items: center;
# #             flex-direction: column;
# #             position: relative;
# #             width: 100%;
# #             border-bottom: 4px solid #1db954;
# #         }}
# #         .header-content {{
# #             background-color: rgba(0, 0, 0, 0.8);
# #             padding: 10px;
# #             border-radius: 10px;

# #         }}
# #         .footer img {{
# #             width: 50px;
# #             height: 50px;
# #             border-radius: 50%;
# #             margin: 0 10px;
# #         }}
# #         .map-container {{
# #             display: flex;
# #             justify-content: center;
# #             align-items: center;
# #             margin-top: 20px;
# #             width: 100%;
# #         }}
# #         .map {{
# #             width: 100%;
# #             height: 800px;
# #             max-width: 1600px;
# #         }}
# #         .input-container {{
# #             display: flex;
# #             justify-content: center;
# #             gap: 1em;
# #             margin-top: 20px;
# #             width: 100%;
# #             max-width: 1600px;
# #         }}
# #         .center-text {{
# #             text-align: center;
# #             width: 100%;
# #         }}
# #         .iframe-container {{
# #             display: flex;
# #             justify-content: center;
# #             margin-top: 20px;
# #         }}

# #         .p{{

# #             font-color: #ffffff;

# #         }}

# #         .stHorizontalBlock {{
# #             display: flex;
# #             justify-content: center;
# #             align-items: center;
# #             flex-wrap: wrap;
# #             width: 100%;
# #             max-width: 1600px;
# #             margin: 0 auto;
# #         }}
# #         .folium-map {{
# #             display: flex;
# #             justify-content: center;
# #             align-items: center;
# #             width: 100%;
# #             max-width: 1600px;
# #             margin: 20px auto;
# #         }}

# #         </style>
# #         """,
# #         unsafe_allow_html=True,
# #     )

# # # Load the custom CSS
# # load_css()

# # # Sidebar for navigation
# # st.sidebar.title("Navigation")
# # page = st.sidebar.selectbox("Select a page:", ["Home", "Data Analysis"])

# # # Common Header
# # def render_header(title):
# #     st.markdown(
# #         f"""
# #         <div class="header">
# #             <div class="header-content">
# #                 <h2>{title}</h2>
# #             </div>
# #         </div>
# #         """,
# #         unsafe_allow_html=True,
# #     )

# # # Footer
# # def render_footer():
# #     st.markdown(
# #         """
# #         <div class="footer">
# #             <p>A Machine Learning model developed by:</p>
# #                 <p>
# #                 <a href="https://github.com/AVMontanari"><img src="https://avatars.githubusercontent.com/u/82625842?s=400&u=7c9523d90f05fe46a75c2e7924cc46c0443e8daa&v=4" alt="André Valle Montanari"></a> André Valle Montanari
# #                 <a href="https://github.com/mauromsilva"><img src="https://avatars.githubusercontent.com/u/116835043?s=96&v=4" alt="Mauro Moreira Silva"></a> Mauro Moreira Silva
# #                 <a href="https://github.com/RafaelDataSci"><img src="https://avatars.githubusercontent.com/u/155320032?s=400&u=a67e1eb25d7e874654b21957f1cc2294a34939b3&v=4" alt="Rafael Quintanilha Ferreira"></a> Rafael Quintanilha Ferreira
# #             </p>
# #         </div>
# #         """,
# #         unsafe_allow_html=True,
# #     )

# # # Home Page
# # if page == "Home":
# #     render_header("PreCog Matrix - A Machine Learning Model to Predict Crimes")

# #     # Streamlit UI
# #     st.markdown("<h3 style='text-align: center;'>Predicting Crimes in Toronto</h3>", unsafe_allow_html=True)

# #     # User input
# #     st.markdown('<div class="input-container stHorizontalBlock">', unsafe_allow_html=True)
# #     col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

# #     with col1:
# #         address = st.text_input("Address", "Toronto City Hall 100 Queen St W", help="Enter the address for crime prediction")
# #     with col2:
# #         crime_date = st.date_input("Crime Date", datetime.now(), help="Select the date of the crime")
# #     with col3:
# #         crime_time = st.time_input("Crime Time", datetime.now().time(), help="Select the time of the crime")
# #     with col4:
# #         st.markdown("<br>", unsafe_allow_html=True)
# #         predict_button = st.button("Predict Crimes")

# #     st.markdown('</div>', unsafe_allow_html=True)

# #     if predict_button:
# #         combined_datetime = datetime.combine(crime_date, crime_time)
# #         prediction, coords = predict_crime(address, combined_datetime)
# #         if prediction:
# #             st.markdown("<h4 style='color: white; text-align: center;'>Crime Prediction Probabilities:</h4>", unsafe_allow_html=True)
# #             crime_labels = ["AUTO THEFT", "ASSAULT", "ROBBERY", "THEFT OVER", "BREAK AND ENTER", "HOMICIDE"]
# #             probabilities = [f"{prob:.2f}%" for prob in prediction[0]]
# #             df = pd.DataFrame({
# #                 "Crime Type": crime_labels,
# #                 "Probability": probabilities
# #             })
# #             st.markdown(
# #                 df.to_html(index=False, justify='center').replace(
# #                     '<table',
# #                     '<table style="color: white; width: 50%; margin: auto; border-collapse: collapse;"'
# #                 ).replace(
# #                     '<th>',
# #                     '<th style="border: 2px solid #1db954; padding: 8px;">'
# #                 ).replace(
# #                     '<td>',
# #                     '<td style="border: 2px solid #1db954; padding: 8px;">'
# #                 ),
# #                 unsafe_allow_html=True
# #             )
# #         else:
# #             st.error("Error fetching prediction. Please try again.")

# #     # Interactive map
# #     st.markdown('<div class="center-text"><h3>Click on the Map to Select a Location</h3></div>', unsafe_allow_html=True)
# #     st.markdown('<div class="map-container">', unsafe_allow_html=True)
# #     map_center = [43.6426, -79.3871]  # CN Tower coordinates
# #     map_obj = folium.Map(location=map_center, zoom_start=12, control_scale=True)

# #     # Add click event to map
# #     if 'map_click' not in st.session_state:
# #         st.session_state.map_click = None

# #     def on_map_click(e):
# #         st.session_state.map_click = e['latlng']

# #     map_obj.add_child(folium.LatLngPopup())
# #     map_obj.add_child(folium.ClickForMarker(popup="You clicked here!"))

# #     # Add marker to the map after prediction
# #     if predict_button and coords:
# #         folium.Marker(location=coords, popup="Prediction Location").add_to(map_obj)

# #     folium_static(map_obj, width=1000, height=500)
# #     st.markdown('</div>', unsafe_allow_html=True)

# #     render_footer()

# # # Data Analysis Page
# # elif page == "Data Analysis":
# #     render_header("Data Analysis")
# #     st.markdown("<h3 style='text-align: center;'>Homicide Analysis</h3>", unsafe_allow_html=True)
# #     st.markdown(
# #         """
# #         <div class="iframe-container">
# #             <iframe title="Homicide" width="1140" height="541.25" src="https://app.powerbi.com/view?r=eyJrIjoiNjc0NzFlZTktYjllMy00NmRjLWIyYzUtNDc4ZTE4M2FiYjg2IiwidCI6Ijg1MjljMjI1LWFjNDMtNDc0Yy04ZmI0LTBmNDA5NWFlOGQ1ZCIsImMiOjN9" frameborder="0" allowFullScreen="true"></iframe>
# #         </div>
# #         """,
# #         unsafe_allow_html=True,
# #     )
# #     render_footer()


# # # Data Visualization Page
# # elif page == "Data Visualization":
# #     render_header("Data Visualization")

# #     st.markdown("<h3 style='text-align: center;'>Crimes by Hour</h3>", unsafe_allow_html=True)
# #     dfmatrix = pd.read_csv('/raw_data/dfmatrix.csv')  # Replace with the actual data file
# #     dv.plot_crimes_by_hour(dfmatrix, dv.crime_types)

# #     st.markdown("<h3 style='text-align: center;'>Crimes by Year</h3>", unsafe_allow_html=True)
# #     dv.plot_crimes_by_year(dfmatrix, dv.crime_types)

# #     st.markdown("<h3 style='text-align: center;'>Crimes by Month</h3>", unsafe_allow_html=True)
# #     dv.plot_crimes_by_month(dfmatrix, dv.crime_types)

# #     st.markdown("<h3 style='text-align: center;'>Crimes by Day of the Week</h3>", unsafe_allow_html=True)
# #     dv.plot_crimes_by_day_of_week(dfmatrix, dv.crime_types)

# #     st.markdown("<h3 style='text-align: center;'>Crimes by Day of the Year</h3>", unsafe_allow_html=True)
# #     dv.plot_crimes_by_day_of_year(dfmatrix, dv.crime_types)

# #     st.markdown("<h3 style='text-align: center;'>Crimes by Day of the Month</h3>", unsafe_allow_html=True)
# #     dv.plot_crimes_by_day_of_month(dfmatrix, dv.crime_types)

# #     st.markdown("<h3 style='text-align: center;'>Crimes Correlation</h3>", unsafe_allow_html=True)
# #     dv.plot_crimes_correlation(dfmatrix, dv.crime_types)

# #     st.markdown("<h3 style='text-align: center;'>Heatmap of Crimes</h3>", unsafe_allow_html=True)
# #     dv.create_heatmap(dfmatrix, 'ASSAULT', 43.7, 43.6, -79.4, -79.5)

# #     st.markdown("<h3 style='text-align: center;'>Word Cloud for Day of the Week</h3>", unsafe_allow_html=True)
# #     dv.generate_wordcloud(dfmatrix, 'OCC_DOW')

# #     st.markdown("<h3 style='text-align: center;'>Period of the Day</h3>", unsafe_allow_html=True)
# #     dv.plot_period_of_the_day()

# #     st.markdown("<h3 style='text-align: center;'>Period of the Month</h3>", unsafe_allow_html=True)
# #     dv.plot_period_of_the_month()

# #     st.markdown("<h3 style='text-align: center;'>Period of the Week</h3>", unsafe_allow_html=True)
# #     dv.plot_period_of_the_week()

# #     st.markdown("<h3 style='text-align: center;'>Year Categorization</h3>", unsafe_allow_html=True)
# #     dv.plot_year_categorization()

# #     st.markdown("<h3 style='text-align: center;'>Crimes per Season</h3>", unsafe_allow_html=True)
# #     dv.plot_crimes_per_season()

# #     st.markdown("<h3 style='text-align: center;'>Total Crime Count by Type</h3>", unsafe_allow_html=True)
# #     dv.plot_total_crime_count_by_type(dfmatrix, dv.crime_types)

# #     render_footer()





# # import streamlit as st
# # import folium
# # from streamlit_folium import folium_static
# # import requests
# # from datetime import datetime
# # import base64
# # import pandas as pd


# # def coordinates(address):
# #     url = "https://nominatim.openstreetmap.org/search"
# #     params = {
# #         'q': address,
# #         'format': 'json'
# #     }
# #     session = requests.Session()
# #     session.headers['User-Agent'] = 'Custom user agent'
# #     response = session.get(url, params=params).json()
# #     return (response[0]['lat'], response[0]['lon'])

# # # Streamlit configuration
# # st.set_page_config(page_title="PreCog Matrix", page_icon="🚨", layout="wide")

# # # Function to call the prediction API
# # def predict_crime(address, crime_date):
# #     lat, lon = coordinates(address)
# #     url = "http://127.0.0.1:8000/predict"
# #     params = {"lat": lat, "lon": lon, "crime_date": crime_date.isoformat()}
# #     try:
# #         response = requests.get(url, params=params)
# #         response.raise_for_status()
# #         return response.json().get("prediction")
# #     except requests.exceptions.RequestException as e:
# #         st.error(f"API request failed: {e}")
# #         return None

# # # Function to convert image to base64
# # def image_to_base64(image_path):
# #     with open(image_path, "rb") as image_file:
# #         return base64.b64encode(image_file.read()).decode()

# # # Load custom CSS
# # def load_css():
# #     base64_image = image_to_base64("toronto.webp")
# #     st.markdown(
# #         f"""
# #         <style>
# #         body {{
# #             background-color: #121212;
# #             color: white;
# #             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
# #         }}
# #         .stApp {{
# #             background-color: #121212;
# #         }}
# #         .stButton>button {{
# #             border-radius: 8px;
# #             background-color: #1db954;
# #             color: white;
# #             border: none;
# #             padding: 0.5em 1em;
# #             font-size: 1em;
# #             font-weight: bold;
# #             cursor: pointer;
# #             transition: background-color 0.3s;
# #         }}
# #         .stButton>button:hover {{
# #             background-color: #1ed760;
# #         }}
# #         .stTextInput>label, .stDateInput>label, .stTimeInput>label {{
# #             color: white !important;
# #         }}
# #         .stTextInput>div>input {{
# #             background-color: #1e1e1e;
# #             color: white;
# #             border: 1px solid #1db954;
# #             border-radius: 8px;
# #             padding: 0.5em;
# #             font-size: 1em;
# #         }}
# #         .stDateInput>div>div>input {{
# #             background-color: #1e1e1e;
# #             color: white;
# #             border: 1px solid #1db954;
# #             border-radius: 8px;
# #             padding: 0.5em;
# #             font-size: 1em;
# #         }}
# #         .stTimeInput>div>div>input {{
# #             background-color: #1e1e1e;
# #             color: white;
# #             border: 1px solid #1db954;
# #             border-radius: 8px;
# #             padding: 0.5em;
# #             font-size: 1em;
# #         }}
# #         .stMarkdown h1, .stMarkdown h2 {{
# #             text-align: center;
# #             color: white;
# #             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
# #         }}
# #         .stMarkdown h3 {{
# #             color: white;
# #         }}
# #         .footer {{
# #             text-align: center;
# #             color: #1db954;
# #             padding: 10px;
# #             background-color: #1e1e1e;
# #             border-top: 2px solid #1db954;
# #         }}
# #         .header {{
# #             background-image: url('data:image/webp;base64,{base64_image}');
# #             background-size: cover;
# #             background-position: center;
# #             height: 300px;
# #             display: flex;
# #             justify-content: center;
# #             align-items: center;
# #             flex-direction: column;
# #             position: relative;
# #             width: 100%;
# #             border-bottom: 4px solid #1db954;
# #         }}
# #         .header-content {{
# #             background-color: rgba(0, 0, 0, 0.5);
# #             padding: 10px;
# #             border-radius: 10px;
# #         }}
# #         .footer img {{
# #             width: 50px;
# #             height: 50px;
# #             border-radius: 50%;
# #             margin: 0 10px;
# #         }}
# #         .map-container {{
# #             display: flex;
# #             justify-content: center;
# #             align-items: center;
# #             margin-top: 20px;
# #             width: 100%;
# #         }}
# #         .map {{
# #             width: 100%;
# #             height: 800px;
# #             max-width: 1600px;
# #         }}
# #         .input-container {{
# #             display: flex;
# #             justify-content: center;
# #             gap: 1em;
# #             margin-top: 20px;
# #             width: 100%;
# #             max-width: 1600px;
# #         }}
# #         .center-text {{
# #             text-align: center;
# #             width: 100%;
# #         }}
# #         .iframe-container {{
# #             display: flex;
# #             justify-content: center;
# #             margin-top: 20px;
# #         }}

# #         .p{{

# #             font-color: #ffffff;

# #         }}

# #         .stHorizontalBlock {{
# #             display: flex;
# #             justify-content: center;
# #             align-items: center;
# #             flex-wrap: wrap;
# #             width: 100%;
# #             max-width: 1600px;
# #             margin: 0 auto;
# #         }}
# #         .folium-map {{
# #             display: flex;
# #             justify-content: center;
# #             align-items: center;
# #             width: 100%;
# #             max-width: 1600px;
# #             margin: 20px auto;
# #         }}

# #         </style>
# #         """,
# #         unsafe_allow_html=True,
# #     )

# # # Load the custom CSS
# # load_css()

# # # Sidebar for navigation
# # st.sidebar.title("Navigation")
# # page = st.sidebar.selectbox("Select a page:", ["Home", "Data Analysis"])

# # # Common Header
# # def render_header(title):
# #     st.markdown(
# #         f"""
# #         <div class="header">
# #             <div class="header-content">
# #                 <h2>{title}</h2>
# #             </div>
# #         </div>
# #         """,
# #         unsafe_allow_html=True,
# #     )

# # # Footer
# # def render_footer():
# #     st.markdown(
# #         """
# #         <div class="footer">
# #             <p>A Machine Learning model developed by:</p>
# #                 <p>
# #                 <a href="https://github.com/AVMontanari"><img src="https://avatars.githubusercontent.com/u/82625842?s=400&u=7c9523d90f05fe46a75c2e7924cc46c0443e8daa&v=4" alt="André Valle Montanari"></a> André Valle Montanari
# #                 <a href="https://github.com/mauromsilva"><img src="https://avatars.githubusercontent.com/u/116835043?s=96&v=4" alt="Mauro Moreira Silva"></a> Mauro Moreira Silva
# #                 <a href="https://github.com/RafaelDataSci"><img src="https://avatars.githubusercontent.com/u/155320032?s=400&u=a67e1eb25d7e874654b21957f1cc2294a34939b3&v=4" alt="Rafael Quintanilha Ferreira"></a> Rafael Quintanilha Ferreira
# #             </p>
# #         </div>
# #         """,
# #         unsafe_allow_html=True,
# #     )

# # # Home Page
# # if page == "Home":
# #     render_header("PreCog Matrix - A Machine Learning Model to Predict Crimes")

# #     # Streamlit UI
# #     st.markdown("<h3 style='text-align: center;'>Predicting Crimes in Toronto</h3>", unsafe_allow_html=True)

# #     # User input
# #     st.markdown('<div class="input-container stHorizontalBlock">', unsafe_allow_html=True)
# #     col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

# #     with col1:
# #         address = st.text_input("Address", "Toronto City Hall 100 Queen St W", help="Enter the address for crime prediction")
# #     with col2:
# #         crime_date = st.date_input("Crime Date", datetime.now(), help="Select the date of the crime")
# #     with col3:
# #         crime_time = st.time_input("Crime Time", datetime.now().time(), help="Select the time of the crime")
# #     with col4:
# #         st.markdown("<br>", unsafe_allow_html=True)
# #         predict_button = st.button("Predict Crimes")

# #     st.markdown('</div>', unsafe_allow_html=True)

# #     if predict_button:
# #         combined_datetime = datetime.combine(crime_date, crime_time)
# #         prediction = predict_crime(address, combined_datetime)

# #         # Extract coordinates for the address to place a marker
# #         coords = coordinates(address)

# #         if prediction:
# #             st.markdown("<h4 style='color: white; text-align: center;'>Crime Prediction Probabilities:</h4>", unsafe_allow_html=True)
# #             crime_labels = ["AUTO THEFT", "ASSAULT", "ROBBERY", "THEFT OVER", "BREAK AND ENTER", "HOMICIDE"]
# #             probabilities = [f"{prob:.2f}%" for prob in prediction[0]]
# #             df = pd.DataFrame({
# #                 "Crime Type": crime_labels,
# #                 "Probability": probabilities
# #             })
# #             st.markdown(
# #                 df.to_html(index=False, justify='center').replace(
# #                     '<table',
# #                     '<table style="color: white; width: 50%; margin: auto; border-collapse: collapse;"'
# #                 ).replace(
# #                     '<th>',
# #                     '<th style="border: 2px solid #1db954; padding: 8px;">'
# #                 ).replace(
# #                     '<td>',
# #                     '<td style="border: 2px solid #1db954; padding: 8px;">'
# #                 ),
# #                 unsafe_allow_html=True
# #             )
# #         else:
# #             st.error("Error fetching prediction. Please try again.")

# #     # Interactive map
# #     st.markdown('<div class="center-text"><h3>Click on the Map to Select a Location</h3></div>', unsafe_allow_html=True)
# #     st.markdown('<div class="map-container" style="display: flex; justify-content: center;">', unsafe_allow_html=True)
# #     map_center = [43.6426, -79.3871]  # CN Tower coordinates
# #     map_obj = folium.Map(location=map_center, zoom_start=12, control_scale=True)

# #     # Add click event to map
# #     if 'map_click' not in st.session_state:
# #         st.session_state.map_click = None

# #     def on_map_click(e):
# #         st.session_state.map_click = e['latlng']

# #     map_obj.add_child(folium.LatLngPopup())
# #     map_obj.add_child(folium.ClickForMarker(popup="You clicked here!"))

# #     # Add marker to the map after prediction
# #     if predict_button and coords:
# #         folium.Marker(location=coords, popup="Prediction Location").add_to(map_obj)

# #     folium_static(map_obj, width=1000, height=500)
# #     st.markdown('</div>', unsafe_allow_html=True)



# #     # if predict_button:
# #     #     combined_datetime = datetime.combine(crime_date, crime_time)
# #     #     prediction = predict_crime(address, combined_datetime)
# #     #     if prediction:
# #     #         st.markdown("<h4 style='color: white; text-align: center;'>Crime Prediction Probabilities:</h4>", unsafe_allow_html=True)
# #     #         crime_labels = ["AUTO THEFT", "ASSAULT", "ROBBERY", "THEFT OVER", "BREAK AND ENTER", "HOMICIDE"]
# #     #         probabilities = [f"{prob:.2f}%" for prob in prediction[0]]
# #     #         df = pd.DataFrame({
# #     #             "Crime Type": crime_labels,
# #     #             "Probability": probabilities
# #     #         })
# #     #         st.markdown(
# #     #             df.to_html(index=False, justify='center').replace(
# #     #                 '<table',
# #     #                 '<table style="color: white; width: 50%; margin: auto; border-collapse: collapse;"'
# #     #             ).replace(
# #     #                 '<th>',
# #     #                 '<th style="border: 2px solid #1db954; padding: 8px;">'
# #     #             ).replace(
# #     #                 '<td>',
# #     #                 '<td style="border: 2px solid #1db954; padding: 8px;">'
# #     #             ),
# #     #             unsafe_allow_html=True
# #     #         )
# #     #     else:
# #     #         st.error("Error fetching prediction. Please try again.")

# #     # # Interactive map
# #     # st.markdown('<div class="center-text"><h3>Click on the Map to Select a Location</h3></div>', unsafe_allow_html=True)
# #     # st.markdown('<div class="map-container" style="display: flex; justify-content: center;">', unsafe_allow_html=True)
# #     # map_center = [43.6426, -79.3871]  # CN Tower coordinates
# #     # map_obj = folium.Map(location=map_center, zoom_start=12, control_scale=True)

# #     # # Add click event to map
# #     # if 'map_click' not in st.session_state:
# #     #     st.session_state.map_click = None

# #     # def on_map_click(e):
# #     #     st.session_state.map_click = e['latlng']

# #     # map_obj.add_child(folium.LatLngPopup())
# #     # map_obj.add_child(folium.ClickForMarker(popup="You clicked here!"))

# #     # folium_static(map_obj, width=1000, height=500)
# #     # st.markdown('</div>', unsafe_allow_html=True)


# #     render_footer()

# # # Data Analysis Page
# # elif page == "Data Analysis":
# #     render_header("Data Analysis")
# #     st.markdown("<h3 style='text-align: center;'>Homicide Analysis</h3>", unsafe_allow_html=True)
# #     st.markdown(
# #         """
# #         <div class="iframe-container">
# #             <iframe title="Homicide" width="1140" height="541.25" src="https://app.powerbi.com/view?r=eyJrIjoiNjc0NzFlZTktYjllMy00NmRjLWIyYzUtNDc4ZTE4M2FiYjg2IiwidCI6Ijg1MjljMjI1LWFjNDMtNDc0Yy04ZmI0LTBmNDA5NWFlOGQ1ZCIsImMiOjN9" frameborder="0" allowFullScreen="true"></iframe>
# #         </div>
# #         """,
# #         unsafe_allow_html=True,
# #     )
# #     render_footer()









# # import streamlit as st
# # import folium
# # from streamlit_folium import folium_static
# # import requests
# # from datetime import datetime
# # import base64

# # def coordinates(address):
# #     url = "https://nominatim.openstreetmap.org/search"
# #     params = {
# #         'q': address,
# #         'format': 'json'
# #     }

# #     session = requests.Session()
# #     session.headers['User-Agent'] = 'Custom user agent'
# #     response = session.get(url, params=params).json()
# #     return (response[0]['lat'], response[0]['lon'])

# # # Streamlit configuration
# # st.set_page_config(page_title="PreCog Matrix", page_icon="🚨", layout="wide")

# # # Function to call the prediction API
# # def predict_crime(address, crime_date):
# #     lat, lon = coordinates(address)
# #     url = "http://127.0.0.1:8000/predict"
# #     params = {"lat": lat, "lon": lon, "crime_date": crime_date.isoformat()}
# #     try:
# #         response = requests.get(url, params=params)
# #         response.raise_for_status()
# #         return response.json().get("prediction")
# #     except requests.exceptions.RequestException as e:
# #         st.error(f"API request failed: {e}")
# #         return None

# # # Function to convert image to base64
# # def image_to_base64(image_path):
# #     with open(image_path, "rb") as image_file:
# #         return base64.b64encode(image_file.read()).decode()

# # # Load custom CSS
# # def load_css():
# #     base64_image = image_to_base64("toronto.webp")
# #     st.markdown(
# #         f"""
# #         <style>
# #         body {{
# #             background-color: #121212;
# #             color: white;
# #             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
# #         }}
# #         .stApp {{
# #             background-color: #121212;
# #         }}
# #         .stButton>button {{
# #             border-radius: 8px;
# #             background-color: #1db954;
# #             color: white;
# #             border: none;
# #             padding: 0.5em 1em;
# #             font-size: 1em;
# #             font-weight: bold;
# #             cursor: pointer;
# #             transition: background-color 0.3s;
# #         }}
# #         .stButton>button:hover {{
# #             background-color: #1ed760;
# #         }}
# #         .stTextInput>label, .stDateInput>label, .stTimeInput>label {{
# #             color: white !important;
# #         }}
# #         .stTextInput>div>input {{
# #             background-color: #1e1e1e;
# #             color: white;
# #             border: 1px solid #1db954;
# #             border-radius: 8px;
# #             padding: 0.5em;
# #             font-size: 1em;
# #         }}
# #         .stDateInput>div>div>input {{
# #             background-color: #1e1e1e;
# #             color: white;
# #             border: 1px solid #1db954;
# #             border-radius: 8px;
# #             padding: 0.5em;
# #             font-size: 1em;
# #         }}
# #         .stTimeInput>div>div>input {{
# #             background-color: #1e1e1e;
# #             color: white;
# #             border: 1px solid #1db954;
# #             border-radius: 8px;
# #             padding: 0.5em;
# #             font-size: 1em;
# #         }}
# #         .stMarkdown h1, .stMarkdown h2 {{
# #             text-align: center;
# #             color: white;
# #             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
# #         }}
# #         .stMarkdown h3 {{
# #             color: white;
# #         }}
# #         .footer {{
# #             text-align: center;
# #             color: #1db954;
# #             padding: 10px;
# #             background-color: #1e1e1e;
# #             border-top: 2px solid #1db954;
# #         }}
# #         .header {{
# #             background-image: url('data:image/webp;base64,{base64_image}');
# #             background-size: cover;
# #             background-position: center;
# #             height: 300px;
# #             display: flex;
# #             justify-content: center;
# #             align-items: center;
# #             flex-direction: column;
# #             position: relative;
# #             width: 100%;
# #             border-bottom: 4px solid #1db954;
# #         }}
# #         .header-content {{
# #             background-color: rgba(0, 0, 0, 0.5);
# #             padding: 10px;
# #             border-radius: 10px;
# #         }}
# #         .footer img {{
# #             width: 50px;
# #             height: 50px;
# #             border-radius: 50%;
# #             margin: 0 10px;
# #         }}
# #         .map-container {{
# #             display: flex;
# #             justify-content: center;
# #             align-items: center;
# #             margin-top: 20px;
# #             width: 100%;
# #         }}
# #         .map {{
# #             width: 100%;
# #             height: 800px;
# #             max-width: 1200px;
# #         }}
# #         .input-container {{
# #             display: flex;
# #             justify-content: center;
# #             gap: 1em;
# #             margin-top: 20px;
# #             width: 100%;
# #         }}
# #         .center-text {{
# #             text-align: center;
# #             width: 100%;
# #         }}
# #         .iframe-container {{
# #             display: flex;
# #             justify-content: center;
# #             margin-top: 20px;
# #         }}

# #         .p{{

# #             font-color: #ffffff;

# #         }}



# #         </style>
# #         """,
# #         unsafe_allow_html=True,
# #     )

# # # Load the custom CSS
# # load_css()

# # # Sidebar for navigation
# # st.sidebar.title("Navigation")
# # page = st.sidebar.selectbox("Select a page:", ["Home", "Data Analytics"])

# # # Home Page
# # if page == "Home":
# #     # Header
# #     st.markdown(
# #         """
# #         <div class="header">
# #             <div class="header-content">
# #                 <h2>PreCog Matrix - A Machine Learning Model to Predict Crimes</h2>
# #             </div>
# #         </div>
# #         """,
# #         unsafe_allow_html=True,
# #     )

# #     # Streamlit UI
# #     st.markdown("## Predicting Crimes in Toronto")

# #     # User input
# #     st.markdown('<div class="input-container">', unsafe_allow_html=True)
# #     address = st.text_input("Address", "Toronto City Hall 100 Queen St W", help="Enter the address for crime prediction")
# #     crime_date = st.date_input("Crime Date", datetime.now(), help="Select the date of the crime")
# #     crime_time = st.time_input("Crime Time", datetime.now().time(), help="Select the time of the crime")
# #     st.markdown('</div>', unsafe_allow_html=True)

# #     # Centralize the "Predict Crime" button
# #     st.markdown('<div class="center-text">', unsafe_allow_html=True)
# #     if st.button("Predict Crimes", key="predict_button"):
# #         combined_datetime = datetime.combine(crime_date, crime_time)
# #         prediction = predict_crime(address, combined_datetime)
# #         if prediction:
# #             st.markdown("### Crime Prediction Probabilities:")
# #             crime_labels = ["AUTO THEFT", "ASSAULT", "ROBBERY", "THEFT OVER", "BREAK AND ENTER", "HOMICIDE"]
# #             for crime, prob in zip(crime_labels, prediction[0]):
# #                 st.markdown(f"**{crime}:** {prob:.2f}")
# #         else:
# #             st.error("Error fetching prediction. Please try again.")
# #     st.markdown('</div>', unsafe_allow_html=True)

# #     # Interactive map
# #     st.markdown('<div class="center-text"><h3>Click on the Map to Select a Location</h3></div>', unsafe_allow_html=True)
# #     st.markdown('<div class="map-container">', unsafe_allow_html=True)
# #     map_center = [43.6426, -79.3871]  # CN Tower coordinates
# #     map_obj = folium.Map(location=map_center, zoom_start=12, control_scale=True, width='100%', height='100%')

# #     # Add click event to map
# #     if 'map_click' not in st.session_state:
# #         st.session_state.map_click = None

# #     def on_map_click(e):
# #         st.session_state.map_click = e['latlng']

# #     map_obj.add_child(folium.LatLngPopup())
# #     map_obj.add_child(folium.ClickForMarker(popup="You clicked here!"))

# #     folium_static(map_obj, width=1250, height=500)
# #     st.markdown('</div>', unsafe_allow_html=True)

# # # Data Analytics Page
# # elif page == "Data Analytics":
# #     st.markdown("## Data Analytics")
# #     st.markdown("<h3 style='text-align: center;'>Homicide Analysis</h3>", unsafe_allow_html=True)
# #     st.markdown(
# #         """
# #         <div class="iframe-container">
# #             <iframe title="Homicide" width="1140" height="541.25" src="https://app.powerbi.com/view?r=eyJrIjoiNjc0NzFlZTktYjllMy00NmRjLWIyYzUtNDc4ZTE4M2FiYjg2IiwidCI6Ijg1MjljMjI1LWFjNDMtNDc0Yy04ZmI0LTBmNDA5NWFlOGQ1ZCIsImMiOjN9" frameborder="0" allowFullScreen="true"></iframe>
# #         </div>
# #         """,
# #         unsafe_allow_html=True,
# #     )

# # # Footer
# # st.markdown(
# #     """
# #     <div class="footer">
# #         <p>A Machine Learning model developed by:</p>
# #             <p>
# #             <a href="https://github.com/AVMontanari"><img src="https://avatars.githubusercontent.com/u/82625842?s=400&u=7c9523d90f05fe46a75c2e7924cc46c0443e8daa&v=4" alt="André Valle Montanari"></a> André Valle Montanari
# #             <a href="https://github.com/mauromsilva"><img src="https://avatars.githubusercontent.com/u/116835043?s=96&v=4" alt="Mauro Moreira Silva"></a> Mauro Moreira Silva
# #             <a href="https://github.com/RafaelDataSci"><img src="https://avatars.githubusercontent.com/u/155320032?s=400&u=a67e1eb25d7e874654b21957f1cc2294a34939b3&v=4" alt="Rafael Quintanilha Ferreira"></a> Rafael Quintanilha Ferreira
# #         </p>
# #     </div>
# #     """,
# #     unsafe_allow_html=True,
# # )
