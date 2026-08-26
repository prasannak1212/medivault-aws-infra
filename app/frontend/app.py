import streamlit as st
import requests
from datetime import date

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="MediVault",
    page_icon="🏥"
)

st.title("MediVault")
st.subheader("Scan Upload")

patient_id = st.text_input("Patient ID")

patient_name = st.text_input("Patient Name")

gender = st.selectbox(
    "Gender",
    ["Male", "Female", "Other"]
)

age = st.number_input(
    "Age",
    min_value=0,
    max_value=120,
    value=30
)

scan_date = st.date_input(
    "Scan Date",
    value=date.today()
)

image = st.file_uploader(
    "Upload Scan Image",
    type=["jpg", "jpeg", "png"]
)

if st.button("Upload Scan"):

    if not patient_id:
        st.error("Please enter Patient ID.")

    elif not patient_name:
        st.error("Please enter Patient Name.")

    elif image is None:
        st.error("Please select a scan image.")

    else:

        files = {
            "image": (
                image.name,
                image.getvalue(),
                image.type
            )
        }

        data = {
            "patient_name": patient_name,
            "gender": gender,
            "age": age,
            "scan_date": str(scan_date)
        }

        response = requests.post(
            f"{API_URL}/patients/{patient_id}/scan",
            data=data,
            files=files
        )

        if response.status_code == 200:
            result = response.json()

            st.success("Scan uploaded successfully!")

            st.write("Image:", result["image"])
            st.write(
                "Patient Info:",
                result["patient_info"]
            )

        else:
            st.error(
                f"Upload failed: {response.text}"
            )