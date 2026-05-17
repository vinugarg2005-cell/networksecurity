import streamlit as st
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

# Page config
st.set_page_config(
    page_title="Phishing Website Detector",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Phishing Website Detection System")

st.write("Upload a CSV file to detect phishing websites.")

# File uploader
uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)

        st.subheader("Uploaded Data")
        st.dataframe(df.head())

        # Load model
        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")

        # Create model object
        network_model = NetworkModel(
            preprocessor=preprocessor,
            model=final_model
        )

        # Predict
        y_pred = network_model.predict(df)


        # Add prediction column
        df["Prediction"] = y_pred

        # Label mapping
        df["Prediction_Label"] = df["Prediction"].map({
            0: "Phishing",
            1: "Safe"
        })

        prediction = df["Prediction_Label"].iloc[0]

        if prediction == "Phishing":
            st.error(f"⚠️ Website Prediction: {prediction}")
        else:
            st.success(f"✅ Website Prediction: {prediction}")

        st.subheader("Prediction Results")
        st.dataframe(df)

        # Download button
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Results",
            data=csv,
            file_name="prediction_output.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error: {e}")