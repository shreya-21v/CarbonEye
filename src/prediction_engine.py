import pandas as pd
import joblib
from geopy.geocoders import Nominatim
import pandas as pd

# Loading trained models
vehicle_model = joblib.load('models/vehicle_model.pkl')
industry_model = joblib.load('models/industry_model.pkl')


VEHICLE_THRESHOLD = 120
INDUSTRY_THRESHOLD = 500

from sklearn.preprocessing import LabelEncoder

def process_vehicle_data():
    df = pd.read_csv('data/new_vehicle_data.csv')

    # Encode categorical columns SAME WAY as training
    le_fuel = LabelEncoder()
    le_type = LabelEncoder()

    df['fuel_type'] = le_fuel.fit_transform(df['fuel_type'])
    df['vehicle_type'] = le_type.fit_transform(df['vehicle_type'])
    df[['lat','lon']] = df['City'].apply(lambda x: pd.Series(get_lat_lon(x)))

    features = df.drop(columns=['vehicle_no'])
    predictions = vehicle_model.predict(features)

    df['Predicted_CO2'] = predictions
    df['Status'] = df['Predicted_CO2'].apply(lambda x: "HIGH" if x > VEHICLE_THRESHOLD else "SAFE")

    df.to_csv('data/vehicle_results.csv', index=False)
    print("Vehicle prediction complete")


def process_industry_data():
    df = pd.read_csv('data/new_industry_data.csv')

    le_type = LabelEncoder()
    le_fuel = LabelEncoder()

    df['Industry_Type'] = le_type.fit_transform(df['Industry_Type'])
    df['Fuel_Used'] = le_fuel.fit_transform(df['Fuel_Used'])
    df['Pollution_Control'] = df['Pollution_Control'].map({'Yes':1,'No':0})
    df[['lat','lon']] = df['City'].apply(lambda x: pd.Series(get_lat_lon(x)))

    features = df.drop(columns=['Industry_Name'])
    predictions = industry_model.predict(features)

    df['Predicted_CO2'] = predictions
    df['Status'] = df['Predicted_CO2'].apply(lambda x: "HIGH" if x > INDUSTRY_THRESHOLD else "SAFE")

    df.to_csv('data/industry_results.csv', index=False)
    print("Industry prediction complete")

geolocator = Nominatim(user_agent="emission_app")

