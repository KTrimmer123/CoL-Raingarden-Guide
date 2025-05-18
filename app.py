import streamlit as st
from calculator import calculate_storage, get_required_storage, pass_fail
from datetime import datetime
from fpdf import FPDF
import pandas as pd
import io

st.set_page_config(page_title="City of London Raingarden Guide", page_icon="💧")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_trigger" not in st.session_state:
    st.session_state.login_trigger = False

# --- CSS Styling ---
if not st.session_state.logged_in:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&family=Poppins:wght@500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    h1 { font-family: 'Poppins', sans-serif !important; text-align: center; }

    .centered-logo {
        display: flex;
        justify-content: center;
        margin-top: -3rem;
        margin-bottom: 0rem;
    }

    .login-heading {
        text-align: center;
        font-family: 'Poppins', sans-serif;
        font-size: 2.5rem;
        font-weight: 600;
        line-height: 2.2rem;
        margin-top: 1rem;
        margin-bottom: 1.25rem;
    }

    .enginuity-logo {
        margin-top: 1.25rem;
    }

    .enginuity-logo p {
        font-style: italic;
        font-size: 0.75rem;
        color: #555;
        margin-top: 1rem;
    }

    div[data-baseweb="input"] {
        border: 2px solid #ccc !important;
        border-radius: 4px !important;
        box-shadow: none !important;
    }
    div[data-baseweb="input"]:hover {
        border: 2px solid #17E0A7 !important;
        box-shadow: 0 0 0 0.15rem rgba(23,224,167,0.2) !important;
    }
    div[data-baseweb="input"]:focus-within {
        border: 2px solid #17E0A7 !important;
        box-shadow: 0 0 0 0.15rem rgba(23,224,167,0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    h1 { font-family: 'Poppins', sans-serif !important; text-align: center; }

    details > summary {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.25rem !important;
        color: #30322F !important;
    }

    div[data-baseweb="input"] {
        border: 2px solid #ccc !important;
        border-radius: 4px !important;
        box-shadow: none !important;
    }
    div[data-baseweb="input"]:hover {
        border: 2px solid #17E0A7 !important;
        box-shadow: 0 0 0 0.15rem rgba(23,224,167,0.2) !important;
    }
    div[data-baseweb="input"]:focus-within {
        border: 2px solid #ccc !important;
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN PAGE ---
if not st.session_state.logged_in:
    st.markdown("""
    <div class='centered-logo'>
        <img src='https://raw.githubusercontent.com/KTrimmer123/CoL-Raingarden-Guide/main/assets/City_of_London_logo.svg.png' width='300'/>
    </div>
    <div class='login-heading'>City of London<br>Raingarden Guide</div>
    """, unsafe_allow_html=True)

    st.text_input("Username", key="username", on_change=lambda: st.session_state.update(login_trigger=True))
    st.text_input("Password", type="password", key="password", on_change=lambda: st.session_state.update(login_trigger=True))

    if st.session_state.login_trigger:
        st.session_state.login_trigger = False
        username = st.session_state.get("username", "")
        password = st.session_state.get("password", "")
        if username and password:
            if username == "city_of_london_rg_tool" and password == "SuDSnotfloods!":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Incorrect username or password")

    st.markdown("""
    <div class='enginuity-logo'>
        <div style="text-align: center;">
            <img src='https://raw.githubusercontent.com/KTrimmer123/CoL-Raingarden-Guide/main/assets/Enginuity_logo.jpg' width='216'/><br>
            <p>
                This tool is the intellectual property of the Enginuity Collective and is made available solely for professional use. It has been developed to support the delivery of sustainable drainage systems (SuDS) and climate-resilient urban design. Use of this tool is intended exclusively for qualified civil engineers and built environment professionals with the appropriate expertise to interpret and apply the outputs responsibly. Unauthorised distribution or misuse is strictly prohibited. For troubleshooting or professional advice on the use of this tool, please contact <a href="mailto:info@enginuitydesign.co.uk">info@enginuitydesign.co.uk</a>.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# --- CALCULATOR PAGE ---

with st.expander("⚙️ Input Parameters", expanded=True):
    area = st.number_input("Raingarden Area (m²)", min_value=1, value=10, step=1, format="%d")
    catchment = st.number_input("Catchment Area (m²)", min_value=1, value=100, step=1, format="%d")
    void_options = {
        "Coarse Graded Aggregate": 0.3,
        "Hydrorock": 0.94,
        "Geocellular": 0.95
    }
    void_label = st.selectbox("Attenuation Form", list(void_options.keys()))
    void_ratio = void_options[void_label]
    depth = int(st.number_input("Attenuation Depth (mm)", min_value=0, value=300, step=5, format="%d"))
    freeboard = st.selectbox("Freeboard (mm)", [150, 200, 250])
    storm_duration = st.selectbox("Storm Duration", ["1hr", "3hr", "6hr"])
    include_infiltration = st.checkbox("Include infiltration in storage calculation", value=False)

required = get_required_storage(catchment, storm_duration)
available = calculate_storage(area, void_ratio, depth, freeboard)

infiltration_rate = 0.036
storm_durations_hrs = {"1hr": 1, "3hr": 3, "6hr": 6}
if required and include_infiltration:
    duration_hr = storm_durations_hrs[storm_duration]
    infiltrated_volume = infiltration_rate * area * duration_hr
    for key in required:
        required[key] = max(required[key] - infiltrated_volume, 0)

if required:
    with st.expander("📐 Catchment Ratio Check", expanded=True):
        if area >= 0.1 * catchment:
            st.success("PASS: Raingarden area is at least 10% of catchment")
            catchment_result = "PASS"
        else:
            st.error("FAIL: Raingarden area is less than 10% of catchment")
            catchment_result = "FAIL"

    with st.expander("🧮 Results", expanded=True):
        st.markdown(f"**Storage Required for {storm_duration} Storm**")
        for label, vol in required.items():
            st.write(f"{label}: {vol:.2f} m³")
        st.write(f"Available Volume in Raingarden: {available:.2f} m³")

    with st.expander("🌧️ Return Period Check", expanded=True):
        result = pass_fail(required, available)
        for label, verdict in result.items():
            if verdict == "PASS":
                st.success(f"{label}: PASS")
            else:
                st.error(f"{label}: FAIL")

    st.markdown("### Export Results")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    df = pd.DataFrame({
        "Storm Duration": [storm_duration],
        "Catchment Area (m²)": [catchment],
        "Raingarden Area (m²)": [area],
        "Void Ratio": [void_ratio],
        "Depth (mm)": [depth],
        "Freeboard (mm)": [freeboard],
        "Include Infiltration": [include_infiltration],
        "Available Volume (m³)": [available],
        "Catchment Check": [catchment_result],
        "Timestamp": [timestamp]
    })

    for label, vol in required.items():
        df[f"{label} Required (m³)"] = [vol]
        df[f"{label} Result"] = [result.get(label, "-")]

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Raingarden Results")

    st.download_button(
        label="📥 Download Excel",
        data=buffer.getvalue(),
        file_name=f"raingarden_results_{timestamp}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "City of London Raingarden Results", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.ln(5)

    pdf.cell(0, 10, f"Timestamp: {timestamp}", ln=True)
    pdf.cell(0, 10, f"Catchment Area: {catchment} m²", ln=True)
    pdf.cell(0, 10, f"Raingarden Area: {area} m²", ln=True)
    pdf.cell(0, 10, f"Void Ratio: {void_ratio}", ln=True)
    pdf.cell(0, 10, f"Depth: {depth} mm", ln=True)
    pdf.cell(0, 10, f"Freeboard: {freeboard} mm", ln=True)
    pdf.cell(0, 10, f"Storm Duration: {storm_duration}", ln=True)
    pdf.cell(0, 10, f"Infiltration: {'Yes' if include_infiltration else 'No'}", ln=True)
    pdf.cell(0, 10, f"Available Volume: {available:.2f} m³", ln=True)
    pdf.cell(0, 10, f"Catchment Ratio Check: {catchment_result}", ln=True)
    pdf.ln(5)

    for label in required:
        pdf.cell(0, 10, f"{label} Required: {required[label]:.2f} m³ - {result.get(label, '-')}", ln=True)

    pdf_data = pdf.output(dest="S").encode("latin1")

    st.download_button(
        label="📥 Download PDF",
        data=pdf_data,
        file_name=f"raingarden_results_{timestamp}.pdf",
        mime="application/pdf"
    )
