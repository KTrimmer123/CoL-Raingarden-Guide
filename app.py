import streamlit as st
from calculator import calculate_storage, get_required_storage, pass_fail

st.set_page_config(page_title="City of London Raingarden Guide", page_icon="💧")

# --- Custom fonts and layout styling ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&family=Poppins:wght@500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    h1 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.9rem !important;
        text-align: center;
    }

    h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
    }

    .main {
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .stApp {
        overflow: hidden;
    }

    .streamlit-expanderHeader > div {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.15rem !important;
    }

    .main .block-container {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    .centered-logo {
        display: flex;
        justify-content: center;
        margin-top: -2rem;
        margin-bottom: 1.25rem;
    }

    .enginuity-logo {
        display: flex;
        justify-content: center;
        margin-top: 1rem;
    }

    .login-heading {
        text-align: center;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 2.5rem;
        line-height: 1.4;
        margin-bottom: 2rem;
    }

    div[data-baseweb="input"] {
        background: none !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }

    .stTextInput > div > input {
        border: 2px solid #ccc !important;
        border-radius: 4px !important;
    }

    .stTextInput > div > input:focus {
        border: 2px solid #17E0A7 !important;
        box-shadow: 0 0 0 0.15rem rgba(23, 224, 167, 0.3) !important;
    }

    input:focus {
        outline: none !important;
        border: 2px solid #17E0A7 !important;
        box-shadow: 0 0 0 0.15rem rgba(23, 224, 167, 0.3) !important;
    }

    .stTextInput:has(.stTextInput-error) > div > input {
        border: 2px solid #ccc !important;
        box-shadow: none !important;
    }

    button + p {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- SIMPLE LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown(
        """
        <div class='centered-logo'>
            <img src='https://raw.githubusercontent.com/KTrimmer123/CoL-Raingarden-Guide/main/assets/City_of_London_logo.svg.png' width='300'/>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='login-heading'>
            City of London<br>Raingarden Guide
        </div>
        """,
        unsafe_allow_html=True
    )

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

    st.markdown(
        """
        <div class='enginuity-logo'>
            <div style="text-align: center;">
                <img src='https://raw.githubusercontent.com/KTrimmer123/CoL-Raingarden-Guide/main/assets/Enginuity_logo.jpg' width='240'/><br>
                <p style="font-size: 0.85rem; color: #555; margin-top: 0.5rem;">
                    This tool is the intellectual property of Enginuity and is provided for professional use in support of sustainable drainage and climate-resilient design. It is intended for use by qualified civil engineers.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()

# --- TOOL TITLE AFTER LOGIN ---
st.title("City of London Raingarden Guide")

# --- INPUT SECTION ---
with st.expander("Input Parameters", expanded=False):
    area = st.number_input("Raingarden Area (m²)", min_value=1, value=10, step=1, format="%d")
    catchment = st.number_input("Catchment Area (m²)", min_value=1, value=100, step=1, format="%d")

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

    include_infiltration = st.checkbox("Include infiltration in storage calculation", value=False)

# --- CALCULATIONS ---
required = get_required_storage(catchment, storm_duration)
available = calculate_storage(area, void_ratio, depth, freeboard)

# --- Apply infiltration if selected ---
infiltration_rate = 0.036  # m/hr
storm_durations_hrs = {"1hr": 1, "3hr": 3, "6hr": 6}

if required and include_infiltration:
    duration_hr = storm_durations_hrs[storm_duration]
    infiltrated_volume = infiltration_rate * area * duration_hr  # m³

    for key in required:
        required[key] = max(required[key] - infiltrated_volume, 0)

# --- CATCHMENT CHECK ---
with st.expander("Catchment Ratio Check", expanded=False):
    if area >= 0.1 * catchment:
        st.success("PASS: Raingarden area is at least 10% of catchment")
    else:
        st.error("FAIL: Raingarden area is less than 10% of catchment")

# --- RESULTS SECTION ---
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
