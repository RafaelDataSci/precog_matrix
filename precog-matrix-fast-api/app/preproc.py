import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib

# Definir os limites aproximados de Toronto
LAT_BOUNDS = [43.5810, 43.8554]  # Limites aproximados de latitude para Toronto
LONG_BOUNDS = [-79.639, -79.115]  # Limites aproximados de longitude para Toronto

def load_data(lat, long, year, month, day, hour):
    """Create a DataFrame from input data and check if within Toronto bounds."""
    if not (LAT_BOUNDS[0] <= lat <= LAT_BOUNDS[1]):
        raise ValueError(f"Latitude {lat} is out of bounds for Toronto.")
    if not (LONG_BOUNDS[0] <= long <= LONG_BOUNDS[1]):
        raise ValueError(f"Longitude {long} is out of bounds for Toronto.")

    data = {
        'LAT_WGS84': [lat],
        'LONG_WGS84': [long],
        'OCC_YEAR': [year],
        'MONTH': [month],
        'OCC_DAY': [day],
        'HOUR': [hour]
    }
    df = pd.DataFrame(data)

    # Rename columns temporarily to create OCC_DATE
    temp_df = df.rename(columns={'OCC_YEAR': 'year', 'MONTH': 'month', 'OCC_DAY': 'day'})
    df['OCC_DATE'] = pd.to_datetime(temp_df[['year', 'month', 'day']])

    # Calculate DOW (day of the week) and DOY (day of the year)
    df['OCC_DOW'] = df['OCC_DATE'].dt.dayofweek + 2  # Adjusting to Sunday=1, Saturday=7
    df['OCC_DOY'] = df['OCC_DATE'].dt.dayofyear  # Day of year

    # Map the days to correct values (Sunday=1, Saturday=7)
    df['OCC_DOW'] = df['OCC_DOW'].apply(lambda x: 1 if x == 8 else x)

    df.drop(columns=['OCC_DATE'], inplace=True)

    return df

def add_trigonometric_features(df, columns):
    """Add sine and cosine transformations for cyclic features."""
    for column in columns:
        if column == 'OCC_DOW':
            max_value = 7
        elif column == 'HOUR':
            max_value = 24
        elif column == 'MONTH':
            max_value = 12
        elif column == 'OCC_DAY':
            max_value = 31
        elif column == 'OCC_DOY':
            max_value = 365
        else:
            raise ValueError(f"Unexpected column name: {column}")

        df[f'{column}_SIN'] = np.sin(2 * np.pi * df[column] / max_value)
        df[f'{column}_COS'] = np.cos(2 * np.pi * df[column] / max_value)
    return df

# def normalize_features(df, feature_columns):
#     """Normalize the features and return the scaled features along with the scaler."""
#     scaler = StandardScaler()
#     df[feature_columns] = scaler.fit_transform(df[feature_columns])
#     return df, scaler

def preproc(df, scaler):
    """Preprocess the data."""
    # Add trigonometric features
    df = add_trigonometric_features(df, ['HOUR', 'OCC_DAY', 'MONTH', 'OCC_DOW', 'OCC_DOY'])

    # Drop original columns that are not needed for the model
    df.drop(columns=['MONTH', 'OCC_DAY', 'HOUR', 'OCC_DOW', 'OCC_DOY'], inplace=True)

    # Normalize features
    feature_columns = ['LAT_WGS84', 'LONG_WGS84', 'OCC_YEAR', 'MONTH_SIN', 'MONTH_COS',
                       'HOUR_SIN', 'HOUR_COS', 'OCC_DAY_SIN', 'OCC_DAY_COS',
                       'OCC_DOY_SIN', 'OCC_DOY_COS', 'OCC_DOW_SIN', 'OCC_DOW_COS']
    df[feature_columns] = scaler.transform(df[feature_columns])

    return df

def load_scaler(filepath):
    """Load the scaler from a file using joblib."""
    return joblib.load(filepath)
