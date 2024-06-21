import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import folium
from folium.plugins import HeatMap
from branca.colormap import linear
from streamlit_folium import st_folium

# Load the DataFrame
dfmatrix_tratado = pd.read_csv('https://storage.googleapis.com/wagon-bootcamp-422319_cloudbuild/dfmatrix_tratado.csv')

# Updated crime types list
crime_types = ["ASSAULT", "AUTO_THEFT", "BREAK_AND_ENTER", "HOMICIDE", "ROBBERY", "THEFT_OVER"]

# Function for plotting crimes by hour
def plot_crimes_by_hour(dfmatrix_tratado, crime_types):
    plt.figure(figsize=(12, 6))
    for crime in crime_types:
        if crime in dfmatrix_tratado.columns:
            sns.lineplot(data=dfmatrix_tratado, x="OCC_HOUR", y=crime, label=crime)
        else:
            st.warning(f"Column '{crime}' not found in DataFrame.")
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Incidents')
    plt.title('Incidents by Hour of the Day')
    plt.xlim(0, 24.5)
    plt.xticks(range(0, 25))
    plt.legend(title='Crime Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt)

# Function for plotting crimes by year
def plot_crimes_by_year(dfmatrix_tratado, crime_types):
    plt.figure(figsize=(12, 6))
    for crime in crime_types:
        if crime in dfmatrix_tratado.columns:
            sns.lineplot(data=dfmatrix_tratado, x="OCC_YEAR", y=crime, label=crime)
        else:
            st.warning(f"Column '{crime}' not found in DataFrame.")
    plt.xlabel('Year')
    plt.ylabel('Number of Incidents')
    plt.title('Incidents by Year')
    plt.legend(title='Crime Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt)

# Function for plotting crimes by month
def plot_crimes_by_month(dfmatrix_tratado, crime_types):
    plt.figure(figsize=(12, 6))
    for crime in crime_types:
        if crime in dfmatrix_tratado.columns:
            sns.lineplot(data=dfmatrix_tratado, x="OCC_MONTH_NUM", y=crime, label=crime)
        else:
            st.warning(f"Column '{crime}' not found in DataFrame.")
    plt.xlabel('Month')
    plt.ylabel('Number of Incidents')
    plt.title('Incidents by Month')
    plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.legend(title='Crime Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt)

# Function for plotting crimes by day of the week
def plot_crimes_by_day_of_week(dfmatrix_tratado, crime_types):
    dfmatrix_tratado['OCC_DOW_NUM'] = dfmatrix_tratado['OCC_DOW_NUM'] % 7
    plt.figure(figsize=(12, 6))
    for crime in crime_types:
        if crime in dfmatrix_tratado.columns:
            sns.lineplot(data=dfmatrix_tratado, x="OCC_DOW_NUM", y=crime, label=crime)
        else:
            st.warning(f"Column '{crime}' not found in DataFrame.")
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Incidents')
    plt.title('Incidents by Day of the Week')
    plt.xticks(range(7), ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    plt.legend(title='Crime Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt)

# Function for plotting crimes by day of the year
def plot_crimes_by_day_of_year(dfmatrix_tratado, crime_types):
    plt.figure(figsize=(12, 6))
    for crime in crime_types:
        if crime in dfmatrix_tratado.columns:
            sns.lineplot(data=dfmatrix_tratado, x="OCC_DOY", y=crime, label=crime)
        else:
            st.warning(f"Column '{crime}' not found in DataFrame.")
    plt.xlabel('Day of the Year')
    plt.ylabel('Number of Incidents')
    plt.title('Incidents by Day of the Year')
    plt.legend(title='Crime Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt)

# Function for plotting crimes by day of the month
def plot_crimes_by_day_of_month(dfmatrix_tratado, crime_types):
    plt.figure(figsize=(12, 6))
    for crime in crime_types:
        if crime in dfmatrix_tratado.columns:
            sns.lineplot(data=dfmatrix_tratado, x="OCC_DAY", y=crime, label=crime)
        else:
            st.warning(f"Column '{crime}' not found in DataFrame.")
    plt.xlabel('Day of the Month')
    plt.ylabel('Number of Incidents')
    plt.title('Incidents by Day of the Month')
    plt.legend(title='Crime Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt)

# Function for plotting crimes correlation
def plot_crimes_correlation(dfmatrix_tratado, crime_columns):
    corr = dfmatrix_tratado[crime_columns].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    st.pyplot(plt)

# Function for creating heatmaps for specific crimes
def create_heatmap(dfmatrix_tratado, crime_type, north_boundary, south_boundary, east_boundary, west_boundary):
    sampled_df = dfmatrix_tratado.sample(frac=0.3, random_state=42)
    crime_df = sampled_df.query(f"`{crime_type}` == 1 and LAT_WGS84 >= @south_boundary and LAT_WGS84 <= @north_boundary and LONG_WGS84 >= @west_boundary and LONG_WGS84 <= @east_boundary")
    locations = crime_df[["LAT_WGS84", "LONG_WGS84"]].values.tolist()
    colormap = linear.YlOrRd_09.scale(0, crime_df.shape[0])
    colormap.caption = crime_type.replace("_", " ").title()
    heatmap = HeatMap(data=locations, gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'yellow', 1: 'red'}, radius=15, blur=20)
    m = folium.Map(location=[(north_boundary + south_boundary) / 2, (east_boundary + west_boundary) / 2], zoom_start=10)
    heatmap.add_to(m)
    colormap.add_to(m)
    return m

# Function to create heatmaps for all crime types
def create_heatmaps_for_all_crimes(dfmatrix_tratado, north_boundary, south_boundary, east_boundary, west_boundary):
    for crime in crime_types:
        heatmap = create_heatmap(dfmatrix_tratado, crime, north_boundary, south_boundary, east_boundary, west_boundary)
        st.write(f"Heatmap for {crime}")
        st_folium(heatmap)

# Function for generating a word cloud for day of the week
def generate_wordcloud(dfmatrix_tratado, column_name):
    dfmatrix_tratado[column_name] = dfmatrix_tratado[column_name].str.strip().fillna('')
    text_data = dfmatrix_tratado[column_name].tolist()
    word_freq = Counter(text_data)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(column_name.replace("_", " ").title())
    st.pyplot(plt)

# Function for plotting period of the day
def plot_period_of_the_day():
    data = {
        'PERIOD_OF_THE_DAY': ['Night (12am - 5am)', 'Morning (5am - 12pm)', 'Afternoon (12pm - 6pm)', 'Night (6pm - 12am)'],
        'Count': [201146, 71721, 105223, 201146]
    }
    df_period_of_the_day = pd.DataFrame(data)
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    barplot = sns.barplot(x='PERIOD_OF_THE_DAY', y='Count', hue='PERIOD_OF_THE_DAY', data=df_period_of_the_day, palette='viridis', dodge=False)
    plt.title('Counts for Each Period of the Day', fontsize=16)
    plt.xlabel('Period of the Day', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.xticks(rotation=45)
    legend_text = ['Night (12am - 5am)', 'Morning (5am - 12pm)', 'Afternoon (12pm - 6pm)', 'Night (6pm - 12am)']
    plt.legend(legend_text, title='Hour Range', title_fontsize='14', loc='upper left', bbox_to_anchor=(1, 0.8))
    plt.tight_layout()
    st.pyplot(plt)

# Function for plotting period of the month
def plot_period_of_the_month():
    data = {
        'PERIOD_OF_THE_MONTH': ['Beginning of the Month', 'End of the Month', 'Middle of the Month'],
        'Count': [127758, 126699, 123633]
    }
    df_period_of_the_month = pd.DataFrame(data)
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(x='PERIOD_OF_THE_MONTH', y='Count', hue='PERIOD_OF_THE_MONTH', data=df_period_of_the_month, palette='viridis', dodge=False)
    plt.title('Counts for Each Period of the Month', fontsize=16)
    plt.xlabel('Period of the Month', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.xticks(rotation=45)
    legend_text = ['Beginning of the Month (1st - 10th)', 'Middle of the Month (11th - 20th)', 'End of the Month (21st - 31st)']
    plt.legend(legend_text, title='Day Range', title_fontsize='14', loc='upper left', bbox_to_anchor=(1, 0.8))
    plt.tight_layout()
    st.pyplot(plt)

# Function for plotting period of the week
def plot_period_of_the_week():
    data = {
        'PERIOD_OF_THE_WEEK': ['Weekday', 'Weekend'],
        'Count': [200000, 80000]
    }
    df_period_of_the_week = pd.DataFrame(data)
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(x='PERIOD_OF_THE_WEEK', y='Count', hue='PERIOD_OF_THE_WEEK', data=df_period_of_the_week, palette='viridis', dodge=False)
    plt.title('Counts for Each Period of the Week', fontsize=16)
    plt.xlabel('Period of the Week', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    legend_text = ['Weekday: Monday - Friday', 'Weekend: Saturday - Sunday']
    plt.legend(legend_text, title='Day Period', title_fontsize='14')
    plt.tight_layout()
    st.pyplot(plt)

# Function for plotting year categorization
def plot_year_categorization():
    data = {
        'YEAR_CATEGORY': ['Early 2010s (2014-2016)', 'Late 2010s (2017-2019)', 'Early 2020s (2020-2022)', '2023 and 2024'],
        'Count': [97946, 111368, 109871, 58905]
    }
    df_year_category = pd.DataFrame(data)
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(x='YEAR_CATEGORY', y='Count', hue='YEAR_CATEGORY', data=df_year_category, palette='viridis', dodge=False)
    plt.title('Counts for Each Year Category', fontsize=18)
    plt.xlabel('Year Category', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.xticks(rotation=45)
    for index, row in df_year_category.iterrows():
        barplot.text(index, row.Count + 1000, f'{row.Count:,}', color='black', ha="center", fontsize=12)
    legend_text = ['Early 2010s (2014-2016)', 'Late 2010s (2017-2019)', 'Early 2020s (2020-2022)', '2023 and 2024']
    plt.legend(legend_text, title='Year Category', title_fontsize='14', loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(plt)

# Function for plotting crimes visualization per season
def plot_crimes_per_season():
    monthly_counts = {
        'January': 32820,
        'February': 29567,
        'March': 32382,
        'April': 28742,
        'May': 31593,
        'June': 31628,
        'July': 32523,
        'August': 32406,
        'September': 31678,
        'October': 32740,
        'November': 31661,
        'December': 30350
    }
    seasons = {
        'Winter': ['December', 'January', 'February'],
        'Spring': ['March', 'April', 'May'],
        'Summer': ['June', 'July', 'August'],
        'Fall': ['September', 'October', 'November']
    }
    season_counts = {season: sum(monthly_counts[month] for month in months) for season, months in seasons.items()}
    df_seasons = pd.DataFrame(list(season_counts.items()), columns=['Season', 'Count'])
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(x='Season', y='Count', hue='Season', data=df_seasons, palette='viridis', dodge=False)
    plt.title('Counts for Each Season', fontsize=16)
    plt.xlabel('Season', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    legend_text = ['Winter: Dec - Feb', 'Spring: Mar - May', 'Summer: Jun - Aug', 'Fall: Sep - Nov']
    plt.legend(legend_text, title='Season', title_fontsize='14', loc='upper left', bbox_to_anchor=(1, 0.8))
    plt.tight_layout()
    st.pyplot(plt)

# Function for plotting total crime count by type
def plot_total_crime_count_by_type(dfmatrix_tratado, crime_columns):
    total_counts = dfmatrix_tratado[crime_columns].sum().reset_index()
    total_counts.columns = ['Crime Type', 'Total Count']
    total_counts = total_counts.sort_values(by='Total Count', ascending=False)
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(x='Total Count', y='Crime Type', data=total_counts, orient='h', palette='viridis')
    plt.title('Total Crime Count by Type', fontsize=18)
    plt.xlabel('Total Count', fontsize=14)
    plt.ylabel('Crime Type', fontsize=14)
    plt.tight_layout()
    st.pyplot(plt)

# Streamlit app interface
st.title("Crime Data Visualization")

option = st.selectbox(
    'Select a visualization to display:',
    ('Crimes by Hour', 'Crimes by Year', 'Crimes by Month', 'Crimes by Day of Week',
     'Crimes by Day of Year', 'Crimes by Day of Month', 'Crimes Correlation',
     'Word Cloud', 'Period of the Day', 'Period of the Month', 'Period of the Week',
     'Year Categorization', 'Crimes per Season', 'Total Crime Count by Type', 'Create Heatmap')
)

if option == 'Crimes by Hour':
    plot_crimes_by_hour(dfmatrix_tratado, crime_types)
elif option == 'Crimes by Year':
    plot_crimes_by_year(dfmatrix_tratado, crime_types)
elif option == 'Crimes by Month':
    plot_crimes_by_month(dfmatrix_tratado, crime_types)
elif option == 'Crimes by Day of Week':
    plot_crimes_by_day_of_week(dfmatrix_tratado, crime_types)
elif option == 'Crimes by Day of Year':
    plot_crimes_by_day_of_year(dfmatrix_tratado, crime_types)
elif option == 'Crimes by Day of Month':
    plot_crimes_by_day_of_month(dfmatrix_tratado, crime_types)
elif option == 'Crimes Correlation':
    plot_crimes_correlation(dfmatrix_tratado, crime_types)
elif option == 'Word Cloud':
    column_name = st.selectbox('Select column for Word Cloud:', dfmatrix_tratado.columns)
    generate_wordcloud(dfmatrix_tratado, column_name)
elif option == 'Period of the Day':
    plot_period_of_the_day()
elif option == 'Period of the Month':
    plot_period_of_the_month()
elif option == 'Period of the Week':
    plot_period_of_the_week()
elif option == 'Year Categorization':
    plot_year_categorization()
elif option == 'Crimes per Season':
    plot_crimes_per_season()
elif option == 'Total Crime Count by Type':
    plot_total_crime_count_by_type(dfmatrix_tratado, crime_types)
elif option == 'Create Heatmap':
    st.header("Create Heatmap")
    north_boundary = 43.8555
    south_boundary = 43.5810
    east_boundary = -79.1150
    west_boundary = -79.6393
    create_heatmaps_for_all_crimes(dfmatrix_tratado, north_boundary, south_boundary, east_boundary, west_boundary)

