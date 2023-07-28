import pandas as pd
import pathlib
import requests

from sklearn.ensemble import RandomForestRegressor

from . import db
from .models import User

# Step 1: Load and preprocess the data
# Load house data and user profile data into pandas DataFrames
house_data = pd.read_excel(
    f"{pathlib.Path().absolute()}/App/datasets/DATA RUMAH TANGSEL.xlsx"
)
# user_profile = User.query.get(1)
datasets_column_title_list = house_data.columns.tolist()
lat = None
lang = None
user_db_objects = None

# Preprocess the data (handle missing values, one-hot encoding, etc.)

# Step 2: Feature engineering (calculate distance_from_workplace)
from geopy.distance import geodesic


def get_user_long_lat_from_address(user_db_object):
    user_address = user_db_object.alamat_tempat_kerja
    API_KEY = "AIzaSyAwqGQ5BbN_hu-bSFX7aHvqMDW2C2tK5Yo"
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={user_address}&key={API_KEY}"

    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    lat = response.json()["results"][0]["geometry"]["location"]["lat"]
    lang = response.json()["results"][0]["geometry"]["location"]["lng"]

    return lat, lang, user_db_object


def calculate_distance(row):
    user_work_address = (lat, lang)
    house_address = (row["latitude"], row["longitude"])
    return geodesic(user_work_address, house_address).kilometers


def train_random_forest(user_db_object):
    global lat
    global lang
    global user_db_objects

    lat, lang, user_db_object = get_user_long_lat_from_address(user_db_object)
    house_data["distance_from_workplace"] = house_data.apply(calculate_distance, axis=1)

    # Step 3: Feature selection (select features to use for prediction)
    selected_features = ["distance_from_workplace", "harga", "fasilitas"]

    # Step 4: Split the data
    X = house_data[selected_features]
    y = house_data["harga"]

    # Step 5: Train the model
    model = RandomForestRegressor()
    model.fit(X, y)

    # Step 6: Predict house prices for the user profile data
    user_data = user_profile[selected_features]
    predicted_prices = model.predict(user_data)

    # Step 7: Rank and recommend houses based on predicted prices and user's affordability
    user_salary = user_profile["monthly_salary"]

    # Filter houses that the user can afford
    affordable_houses = house_data[house_data["price"] <= user_salary]

    # Sort affordable houses by predicted prices in ascending order
    recommended_houses = affordable_houses.loc[
        affordable_houses["price"].argsort(ascending=True)
    ]

    # Display the recommended houses to the user
    print(recommended_houses)
