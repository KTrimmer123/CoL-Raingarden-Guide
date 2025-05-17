import streamlit as st
from calculator import calculate_storage, get_required_storage, pass_fail

st.set_page_config(page_title="City of London Raingarden Guide", page_icon="💧")

# --- Track login state ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- CSS styles based on login state ---
if not st.session_state.logged_in:
    # GREEN focus styling for login page
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&family=Poppins:wght@500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    h1 { font-family: 'Poppins', sans-serif !important; font-size: 1.9rem !important; text-align: center; font-weight: 600 !important; }
    .login-heading { text-align: center; font-family: 'Poppins', sans-serif; font-size: 2.5rem; font-weight: 600; margin-bottom: 2rem; }
    .centered-logo {
        display: flex;
        justify-content: center;
        margin-top: -2rem;
        margin-bottom: 1.25rem;
    }
    div[data-baseweb="input"] {
        border: 2px solid #ccc !important;
        border-radius: 4px !important;
        box-shadow: none !important;
    }
    div[data-baseweb="input"]:focus-within {
        border: 2px solid #17E0A7 !important;
        box-shadow: 0 0 0 0.15rem rgba(23, 224, 167, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    # NO focus styling for calculator page
    st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    h1 { font-family: 'Poppins', sans-serif !important; font-size: 1.9rem !important; text-align: center; font-weight: 600 !important; }
    .streamlit-expanderHeader > div {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.15rem !important;
    }
    div[data-baseweb="input"] {
        border: 2px solid #ccc !important;
        border-radius: 4px !important;
        box-shadow: none !important;
    }
    div[data-baseweb="input"]:focus-within {
        border: 2px solid #ccc !important;
        box-shadow: none !important;
    }
    .stNumberInput input:focus {
        outline: none !important;
        border: none !important;
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

    with st.form("login_form"):
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if st.session_state.username == "city_of_london_rg_tool" and st.session_state.password == "SuDSnotfloods!":
            st.session_state.logged_in = True
            st.success("Login successful! Loading tool...")
            st.rerun()
        else:
            st.error("Incorrect username or password")

    st.markdown("""
    <div class='enginuity-logo'>
        <div style="text-align: center;">
            <img src='https://raw.githubusercontent.com/KTrimmer123/CoL-Raingarden-Guide/main/assets/Enginuity_logo.jpg' width='240'/><br>
            <p style="font-size: 0.85rem; color: #555; margin-top: 0.5rem;">
                This tool is the intellectual property of Enginuity and is provided for professional use in support of sustainable drainage and climate-resilient design. It is intended for use by qualified civil engineers.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# --- CALCULATOR PAGE ---
st.title("City of London Raingarden Guide")

with st.expander("Input Parameters", expanded=False):
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

# --- CALCULATIONS ---
required = get_required_storage(catchment, storm_duration)
available = calculate_storage(area, void_ratio, depth, freeboard)

# --- INFILTRATION ADJUSTMENT ---
infiltration_rate = 0.036  # m/hr
storm_durations_hrs = {"1hr": 1, "3hr": 3, "6hr": 6}

if required and include_infiltration:
    duration_hr = storm_durations_hrs[storm_duration]
    infiltrated_volume = infiltration_rate * area * duration_hr
    for key in required:
        required[key] = max(required[key] - infiltrated_volume, 0)

# --- CATCHMENT CHECK ---
with st.expander("Catchment Ratio Check", expanded=False):
    if area >= 0.1 * catchment:
        st.success("PASS: Raingarden area is at least 10% of catchment")
    else:
        st.error("FAIL: Raingarden area is less than 10% of catchment")

# --- RESULTS ---
with st.expander("Results", expanded=False):
    if required:
        st.markdown(f"**Storage Required for {storm_duration} Storm**")
        for label, vol in required.items():
            st.write(f"{label}: {vol:.2f} m³")
        st.write(f"Available Volume in Raingarden: {available:.2f} m³")
    else:
        st.warning("Catchment size too large for FEH table.")

# --- RETURN PERIOD CHECK ---
if required:
    with st.expander("Return Period Check", expanded=False):
        result = pass_fail(required, available)
        for label, verdict in result.items():
            if verdict == "PASS":
                st.success(f"{label}: PASS")
            else:
                st.error(f"{label}: FAIL")
