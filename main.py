
import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Load Model
model = joblib.load("price_prediction_app.pkl")

# Page Configuration
st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="centered"
)

# Heading
st.title("🏠 House Price Prediction")
st.write("Enter house details to predict the estimated price.")

st.divider()

# Input Fields - Two Columns
col1, col2 = st.columns(2)

with col1:
    area_sqft = st.number_input(
        "Area (Square Feet)",
        min_value=100,
        max_value=10000,
        value=1000,
        key="area"
    )

    bedrooms = st.number_input(
        "Bedrooms",
        min_value=1,
        max_value=10,
        value=2,
        key="bedrooms"
    )

    bathrooms = st.number_input(
        "Bathrooms",
        min_value=1,
        max_value=10,
        value=2,
        key="bathrooms"
    )

    age_years = st.number_input(
        "Age (Years)",
        min_value=0,
        max_value=100,
        value=5,
        key="age"
    )

with col2:
    floor_number = st.number_input(
        "Floor Number",
        min_value=0,
        max_value=100,
        value=1,
        key="floor"
    )

    parking_spaces = st.number_input(
        "Parking Spaces",
        min_value=0,
        max_value=10,
        value=1,
        key="parking"
    )

    distance_metro_km = st.number_input(
        "Distance from Metro (KM)",
        min_value=0.0,
        max_value=100.0,
        value=2.0,
        key="metro"
    )

    distance_school_km = st.number_input(
        "Distance from School (KM)",
        min_value=0.0,
        max_value=100.0,
        value=1.0,
        key="school"
    )

st.divider()

# Prediction
if st.button("Predict House Price", use_container_width=True):

    input_data = pd.DataFrame([{
        "area_sqft": area_sqft,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "age_years": age_years,
        "floor_number": floor_number,
        "parking_spaces": parking_spaces,
        "distance_metro_km": distance_metro_km,
        "distance_school_km": distance_school_km
    }])

    try:
        prediction = model.predict(input_data)
        price = float(np.asarray(prediction).flatten()[0])

        st.success("Prediction Completed!")
        st.metric(
            label="Estimated House Price",
            value=f"₹ {price:.2f} Lakh"
        )

    except Exception as e:
        st.error(f"Prediction Error: {e}")
