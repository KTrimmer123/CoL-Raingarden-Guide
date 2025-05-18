import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Retrofit Raingarden Calculator", layout="centered")

st.title("Retrofit Raingarden Calculator")

# Inputs
ra_area = st.number_input("Raingarden Area (m²)", min_value=0.0)
catchment_area = st.number_input("Catchment Area (m²)", min_value=0.0)

void_ratios = {
    "Geocellular": 0.95,
    "Hydrorock": 0.94,
    "Gravel": 0.3,
    "None (clay/no voids)": 0.0
}
void_choice = st.selectbox("Attenuation Form", list(void_ratios.keys()))
void_ratio = void_ratios[void_choice]

freeboard_mm = st.number_input("Freeboard (mm)", min_value=0.0)
storm_dur = st.selectbox("Storm Duration (hr)", [1, 3, 6, 12, 24])
infiltration_enabled = st.checkbox("Include Infiltration (0.036 m/hr)", value=False)

# Calculation logic
def calculate_storage(ra_area, catchment_area, void_ratio, freeboard_mm, storm_hr, infiltration_enabled):
    rainfall_depth_mm = 30  # static design storm depth
    runoff_volume = catchment_area * (rainfall_depth_mm / 1000)
    infiltration_volume = 0
    if infiltration_enabled:
        infiltration_rate = 0.036  # m/hr
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

results = calculate_storage(ra_area, catchment_area, void_ratio, freeboard_mm, storm_dur, infiltration_enabled)

# Results
st.subheader("Results")
st.metric("Runoff Volume (m³)", results["Runoff Volume (m³)"])
st.metric("Storage Provided (m³)", results["Storage Provided (m³)"])
st.metric("Infiltration Volume (m³)", results["Infiltration Volume (m³)"])
st.markdown(f"### {results['Result']}")

# Export to Excel
def export_excel(data):
    df = pd.DataFrame([data])
    df["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

# Export to PDF
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

# Export buttons
st.markdown("---")
st.subheader("Export Results")
col1, col2 = st.columns(2)
with col1:
    st.download_button("Download Excel", export_excel(results), file_name="raingarden_results.xlsx")
with col2:
    st.download_button("Download PDF", export_pdf(results), file_name="raingarden_results.pdf")
