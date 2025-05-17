import streamlit as st
from calculator import calculate_storage, get_required_storage, pass_fail

st.set_page_config(page_title="City of London Raingarden Guide", page_icon="💧")

# --- Custom fonts and layout ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&family=Poppins:wght@500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
    }

    .main .block-container {
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        text-align: left !important;
    }

    .stMetric {
        text-align: left !important;
    }

    .centered-logo {
        display: flex;
        justify-content: center;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- SIMPLE LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("City of London Raingarden Guide")
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if username == "city_of_london_rg_tool" and password == "SuDSnotfloods!":
        st.session_state.logged_in = True
        st.success("Login successful! Loading tool...")
        st.rerun()
    elif username and password:
        st.error("Incorrect username or password")
    st.stop()

# --- LOGO + TOOL TITLE ---
st.markdown(
    """
    <div class='centered-logo'>
        <img src='https://raw.githubusercontent.com/KTrimmer123/CoL-Raingarden-Guide/main/assets/City_of_London_logo.svg.png' width='300'/>
    </div>
    """,
    unsafe_allow_html=True
)
st.title("City of London Raingarden Guide")

# --- INPUT SECTION ---
with st.expander("Input Parameters", expanded=True):
    area = st.number_input("Raingarden Area (m²)", min_value=1.0, value=10.0)
    catchment = st.number_input("Catchment Area (m²)", min_value=1.0, value=100.0)

    void_options = {
        "Coarse Graded Aggregate": 0.3,
        "Hydrorock": 0.4,
        "Geocellular": 0.94
    }
    void_label = st.selectbox("Attenuation Form", list(void_options.keys()))
    void_ratio = void_options[void_label]

    depth = int(st.number_input("Attenuation Depth (mm)", min_value=0, value=300, step=5, format="%d"))
    freeboard = st.selectbox("Freeboard (mm)", [150, 200, 250])
    storm_duration = st.selectbox("Storm Duration", ["1hr", "3hr", "6hr"])

# --- CALCULATIONS ---
required = get_required_storage(catchment, storm_duration)
available = calculate_storage(area, void_ratio, depth, freeboard)

# --- CATCHMENT CHECK ---
with st.expander("Catchment Ratio Check", expanded=True):
    if area >= 0.1 * catchment:
        st.success("PASS: Raingarden area is at least 10% of catchment")
    else:
        st.error("FAIL: Raingarden area is less than 10% of catchment")

# --- RESULTS SECTION ---
with st.expander("Results", expanded=True):
    if required:
        st.markdown(f"**Storage Required for {storm_duration} Storm**")
        for label, vol in required.items():
            st.write(f"{label}: {vol:.2f} m³")

        st.write(f"Available Volume in Raingarden: {available:.2f} m³")
    else:
        st.warning("Catchment size too large for FEH table.")

# --- RETURN PERIOD CHECK (not nested) ---
if required:
    with st.expander("Return Period Check", expanded=True):
        result = pass_fail(required, available)
        for label, verdict in result.items():
            if verdict == "PASS":
                st.success(f"{label}: PASS")
            else:
                st.error(f"{label}: FAIL")
