import streamlit as st
import pandas as pd
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Retrofit SuDS Raingarden Calculator", layout="centered")

# Title
st.title("🌧️ Retrofit SuDS Raingarden Calculator")

# Tooltip helper
def tooltip(label, text):
    return f"{label} ℹ️: {text}"

# Inputs with tooltips
raingarden_area = st.number_input(
    label=tooltip("Raingarden Area (m²)", "Area of the raingarden available"),
    min_value=0.0,
    step=0.1,
    format="%.2f"
)

catchment_area = st.number_input(
    label=tooltip("Catchment Area (m²)", "Total catchment drained to raingarden (including raingarden area itself)"),
    min_value=0.0,
    step=0.1,
    format="%.2f"
)

void_choice = st.selectbox(
    label=tooltip("Attenuation Form", "Material used for surface water attenuation (void ratio selection)"),
    options=["Raingarden Soil", "Geocellular", "Hydrorock"],
)

void_dict = {
    "Raingarden Soil": 0.25,
    "Geocellular": 0.95,
    "Hydrorock": 0.94,
}
void_ratio = void_dict[void_choice]

freeboard = st.number_input(
    label=tooltip("Freeboard (m)", "Water storage above the planting level but contained within the kerb"),
    min_value=0.0,
    step=0.01,
    format="%.2f"
)

storm_duration = st.selectbox(
    label=tooltip("Storm Duration", "Length of rainfall event used in the storage design. Select 1-hr as default"),
    options=["1-hr", "3-hr", "6-hr"],
    index=0
)

# FEH rainfall data (depths in mm)
feh_depths = {
    "1-hr": {
        "1 in 2": 18.2,
        "1 in 10": 27.3,
        "1 in 30": 35.5,
        "1 in 100": 43.5,
        "1 in 100 + CC": 60.9,
    },
    "3-hr": {
        "1 in 2": 25.2,
        "1 in 10": 37.9,
        "1 in 30": 48.4,
        "1 in 100": 57.9,
        "1 in 100 + CC": 81.1,
    },
    "6-hr": {
        "1 in 2": 29.2,
        "1 in 10": 43.9,
        "1 in 30": 55.6,
        "1 in 100": 66.6,
        "1 in 100 + CC": 93.2,
    }
}

# Calculation
def calculate_storage(rainfall_mm):
    runoff_volume_m3 = (catchment_area * (rainfall_mm / 1000))  # m³
    available_storage_m3 = (raingarden_area * void_ratio) + (raingarden_area * freeboard)
    return runoff_volume_m3, available_storage_m3

# Results
st.markdown("### 📊 Results")
results = []
for event, depth in feh_depths[storm_duration].items():
    runoff, storage = calculate_storage(depth)
    status = "✅ Pass" if storage >= runoff else "❌ Fail"
    results.append({
        "Event": event,
        "Rainfall Depth (mm)": depth,
        "Runoff Volume (m³)": round(runoff, 2),
        "Storage Volume (m³)": round(storage, 2),
        "Result": status
    })

df = pd.DataFrame(results)
st.dataframe(df, use_container_width=True)

# Export buttons
col1, col2 = st.columns(2)
with col1:
    if st.download_button(
        label="📄 Export to Excel",
        data=df.to_excel(index=False, engine='openpyxl'),
        file_name="raingarden_calculation.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ):
        st.success("Excel file exported!")

with col2:
    if st.download_button(
        label="🧾 Export to CSV",
        data=df.to_csv(index=False),
        file_name="raingarden_calculation.csv",
        mime="text/csv",
    ):
        st.success("CSV file exported!")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for the City of London | Enginuity")
