import streamlit as st
import pandas as pd

st.set_page_config(page_title="Retrofit SuDS Raingarden Calculator", layout="centered")

st.title("Retrofit SuDS Raingarden Calculator")

# Inputs
raingarden_area = st.number_input("Raingarden Area (m²)", min_value=0.0, step=0.1, format="%.2f")
catchment_area = st.number_input("Catchment Area (m²)", min_value=0.0, step=0.1, format="%.2f")

attenuation_form = st.selectbox("Attenuation Form", ["Raingarden Soil", "Geocellular", "Hydrorock"])
void_ratios = {"Raingarden Soil": 0.25, "Geocellular": 0.95, "Hydrorock": 0.94}
void_ratio = void_ratios[attenuation_form]

freeboard = st.number_input("Freeboard (m)", min_value=0.0, step=0.01, format="%.2f")

storm_duration = st.selectbox("Storm Duration", ["1-hr", "3-hr", "6-hr"], index=0)

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

def calculate_storage(rainfall_mm):
    runoff_volume = catchment_area * (rainfall_mm / 1000)
    storage_volume = raingarden_area * void_ratio + raingarden_area * freeboard
    return runoff_volume, storage_volume

st.subheader("Results")

for event, depth in feh_depths[storm_duration].items():
    runoff, storage = calculate_storage(depth)
    st.write(f"**{event}**:")
    st.write(f"- Rainfall Depth: {depth} mm")
    st.write(f"- Runoff Volume: {runoff:.2f} m³")
    st.write(f"- Storage Volume: {storage:.2f} m³")
    if storage >= runoff:
        st.success("Pass ✅")
    else:
        st.error("Fail ❌")
