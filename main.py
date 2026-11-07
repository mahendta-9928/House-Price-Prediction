
import streamlit as st
import joblib
import pandas as pd
import numpy as np

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="EstateIQ | House Prediction",
    page_icon="🏡",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------

@st.cache_resource
def load_model():
    return joblib.load("price_prediction_app.pkl")

model = load_model()

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.stApp {
    background: #0b1120;
    color: #f1f5f9;
}

[data-testid="stSidebar"] {
    background: #111a2e;
    border-right: 1px solid #26344f;
}

.main .block-container {
    padding: 2rem 3rem;
    max-width: 1400px;
}

h1, h2, h3 {
    color: #f8fafc !important;
}

p, label {
    color: #aab7cc !important;
}

.hero {
    background: linear-gradient(120deg, #172554, #312e81, #4c1d95);
    padding: 35px;
    border-radius: 20px;
    margin-bottom: 25px;
    border: 1px solid #4338ca;
}

.hero h1 {
    font-size: 34px;
    margin-bottom: 8px;
}

.hero p {
    color: #dbeafe !important;
    font-size: 15px;
}

.section-card {
    background: #151f33;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #293955;
    margin-bottom: 15px;
}

.result-card {
    background: linear-gradient(135deg, #172554, #312e81);
    padding: 30px;
    border-radius: 20px;
    border: 1px solid #6366f1;
    text-align: center;
    margin-top: 25px;
}

.result-card h2 {
    color: #c7d2fe !important;
    font-size: 18px;
}

.price {
    color: #ffffff;
    font-size: 42px;
    font-weight: 800;
    margin: 12px 0;
}

div.stButton > button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 14px;
    font-weight: 700;
    width: 100%;
}

div.stButton > button:hover {
    background: #7c3aed;
    color: white;
    border: none;
}

[data-testid="stMetric"] {
    background: #151f33;
    padding: 18px;
    border: 1px solid #293955;
    border-radius: 14px;
}

[data-testid="stMetricValue"] {
    color: #a5b4fc;
}

hr {
    border-color: #293955;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("## 🏡 EstateIQ")

    st.caption("REAL ESTATE INTELLIGENCE")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        ["Dashboard", "About Project"],
        key="navigation"
    )

    st.divider()

    st.markdown("### 🤖 ML Model")
    st.success("Model Loaded")

    st.caption("Powered by Machine Learning")

    st.divider()

    st.caption("© 2026 EstateIQ  -- BY Mahendra Sharma")


# ---------------- DASHBOARD ----------------

if page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>🏠 House Price Prediction</h1>
        <p>
        Smart property valuation powered by Machine Learning.
        Enter your property details to discover its estimated market value.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Top metrics

    m1, m2, m3 = st.columns(3)

    m1.metric("MODEL TYPE", "Linear Regression")
    m2.metric("INPUT FEATURES", "08")
    m3.metric("PREDICTION", "Real Time")

    st.write("")

    st.markdown("## 📝 Property Information")
    st.caption("Fill in the details below to estimate your property value.")

    # ---------------- INPUT FORM ----------------

    with st.form("house_prediction_form"):

        left, right = st.columns(2, gap="large")

        with left:

            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("### 📐 Property Details")

            area_sqft = st.number_input(
                "Area (Square Feet)",
                100, 10000, 1000,
                key="area"
            )

            bedrooms = st.number_input(
                "Bedrooms",
                1, 10, 2,
                key="bedrooms"
            )

            bathrooms = st.number_input(
                "Bathrooms",
                1, 10, 2,
                key="bathrooms"
            )

            age_years = st.number_input(
                "Property Age (Years)",
                0, 100, 5,
                key="age"
            )

            st.markdown('</div>', unsafe_allow_html=True)

        with right:

            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("### 🏢 Location & Facilities")

            floor_number = st.number_input(
                "Floor Number",
                0, 100, 1,
                key="floor"
            )

            parking_spaces = st.number_input(
                "Parking Spaces",
                0, 10, 1,
                key="parking"
            )

            distance_metro_km = st.number_input(
                "Distance from Metro (KM)",
                0.0, 100.0, 2.0,
                key="metro"
            )

            distance_school_km = st.number_input(
                "Distance from School (KM)",
                0.0, 100.0, 1.0,
                key="school"
            )

            st.markdown('</div>', unsafe_allow_html=True)

        predict_button = st.form_submit_button(
            "🚀 Predict House Price",
            use_container_width=True
        )

    # ---------------- PREDICTION ----------------

    if predict_button:

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

            st.markdown(f"""
            <div class="result-card">
                <h2>✨ Estimated Property Value</h2>
                <div class="price">₹ {price:,.2f} Lakh</div>
                <p>Prediction generated successfully</p>
            </div>
            """, unsafe_allow_html=True)

            st.write("")

            st.markdown("### 📊 Property Summary")

            a, b, c, d = st.columns(4)

            a.metric("Area", f"{area_sqft:,} sqft")
            b.metric("Bedrooms", bedrooms)
            c.metric("Bathrooms", bathrooms)
            d.metric("Parking", parking_spaces)

            st.caption(
                "Note: This is an ML-based estimate, not a guaranteed market valuation."
            )

        except Exception as e:

            st.error(f"Prediction Error: {e}")


# ---------------- ABOUT PAGE ----------------

elif page == "About Project":

    st.markdown("""
    <div class="hero">
        <h1>📊 About EstateIQ</h1>
        <p>Machine Learning Based House Price Prediction System</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎯 Project Objective")

    st.write("""
    EstateIQ is a machine learning application designed
    to estimate house prices based on property characteristics,
    facilities and location-related information.
    """)

    st.markdown("### 🛠️ Technologies Used")

    c1, c2, c3 = st.columns(3)

    c1.info("🐍 Python")
    c2.info("📊 Pandas & NumPy")
    c3.info("🤖 Scikit-learn")

    st.markdown("### 📌 Model Information")

    st.write("""
    - Algorithm: Linear Regression
    - Input Features: 8
    - Target Variable: House Price
    - Interface: Streamlit
    """)
