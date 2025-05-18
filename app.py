import streamlit as st
import pandas as pd
import numpy as np
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# -------- Login Setup --------
names = ["City User"]
usernames = ["city"]
passwords = ["raingarden123"]

hashed_passwords = stauth.Hasher(passwords).generate()

credentials = {
    "usernames": {
        usernames[0]: {
            "name": names[0],
            "password": hashed_passwords[0]
        }
    }
}

authenticator = stauth.Authenticate(
    credentials, "raingarden_app", "abcdef", cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login("Login", "main")

# --------- Main App ---------
if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.title("Retrofit Raingarden Calculator")

    # Tooltips
    tooltips = {
        "ra_area": "Raingarden Area = Area of the raingarden available",
        "catchment": "Catchment Area = Total catchment drained to raingarden (including raingarden area itself)",
        "void_ratio": "Attenuation Form = Material used for surface water attenuation (void ratio selection)",
        "freeboard": "Freeboard = Water storage above the planting level but contained within the kerb",
        "storm_dur": "Storm Duration = Length of rainfall event used in the storage design. Select 1-hr as default",
        "infiltration": "Include Infiltration = Apply the average infiltration rate across the City"
    }

    # Inputs
    st.number_input("Raingarden Area (m²)", min_value=0.0, key="ra_area", help=tooltips["ra_area"])
    st.number_input("Catchment Area (m²)", min_value=0.0, key="catchment", help=tooltips["catchment"])

    void_ratios = {"Geocellular": 0.95, "Hydrorock": 0.94, "Gravel": 0.3, "None (clay/no voids)": 0.0}
    void_choice = st.selectbox("Attenuation Form", list(void_ratios.keys()), help=tooltips["void_ratio"])
    void_ratio = void_ratios[void_choice]

    st.number_input("Freeboard (mm)", min_value=0.0, key="freeboard", help=tooltips["freeboard"])
    storm_dur = st.selectbox("Storm Duration (hr)", [1, 3, 6, 12, 24], help=tooltips["storm_dur"])
    infiltration_enabled = st.checkbox("Include Infiltration (0.036 m/hr)", value=False, help=tooltips["infiltration"])

    # Calculation
    def calculate_storage(ra_area, catchment_area, void_ratio, freeboard_mm, storm_hr, infiltration_enabled):
        rainfall_depth_mm = 30
        runoff_volume = catchment_area * (rainfall_depth_mm / 1000)
        infiltration_volume = 0
        if infiltration_enabled:
            infiltration_rate = 0.036
            infiltration_volume = ra_area * infiltration_rate * storm_hr

        freeboard_depth_m = freeboard_mm / 1000
        attenuation_storage = ra_area * void_ratio
        freeboard_storage = ra_area * freeboard_depth_m
        total_storage = attenuation_storage + freeboard_storage + infiltration_volume

        pass_fail = "✅ Pass" if total_storage >= runoff_volume else "❌ Fail"

        return {
            "Runoff Volume (m³)": round(runoff_volume, 2),
            "Storage Provided (m³)": round(total_storage, 2),
            "Infiltration Volume (m³)": round(infiltration_volume, 2),
            "Result": pass_fail
        }

    results = calculate_storage(
        st.session_state["ra_area"],
        st.session_state["catchment"],
        void_ratio,
        st.session_state["freeboard"],
        storm_dur,
        infiltration_enabled
    )

    st.subheader("Results")
    st.metric("Runoff Volume (m³)", results["Runoff Volume (m³)"])
    st.metric("Storage Provided (m³)", results["Storage Provided (m³)"])
    st.metric("Infiltration Volume (m³)", results["Infiltration Volume (m³)"])
    st.markdown(f"### {results['Result']}")

    # Export: Excel
    def export_excel(data):
        df = pd.DataFrame([data])
        df["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()

    # Export: PDF
    def export_pdf(data):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        p.setFont("Helvetica", 12)
        text = p.beginText(40, 800)
        text.textLine("Retrofit Raingarden Calculator Results")
        text.textLine(" ")
        for k, v in data.items():
            text.textLine(f"{k}: {v}")
        text.textLine(" ")
        text.textLine(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        p.drawText(text)
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer.getvalue()

    st.markdown("---")
    st.subheader("Export Results")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("Download Excel", export_excel(results), file_name="raingarden_results.xlsx")
    with col2:
        st.download_button("Download PDF", export_pdf(results), file_name="raingarden_results.pdf")

elif authentication_status is False:
    st.error("Username or password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
