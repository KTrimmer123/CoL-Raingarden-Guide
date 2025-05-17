import streamlit as st
from calculator import calculate_storage, get_required_storage, pass_fail

st.set_page_config(page_title="City of London Raingarden Guide", page_icon="💧")

# --- Custom fonts, layout, and input styling ---
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

    .streamlit-expanderHeader > div {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.15rem !important;
    }

    .main .block-container {
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    .stMetric {
        text-align: left !important;
    }

    .centered-logo {
        display: flex;
        justify-content: center;
        margin-top: -2.5rem;
        margin-bottom: 0.5rem;
    }

    .login-heading {
        text-align: center;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 2.2rem;
        line-height: 1.4;
        margin-bottom: 2rem;
    }

    .login-form {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .stTextInput > div > input {
        border: 2px solid #ccc !important;
        border-radius: 4px !important;
    }

    .stTextInput > div > input:focus {
        border: 2px solid #17E0A7 !important;
        box-shadow: 0 0 0 0.15rem rgba(23, 224, 167, 0.3) !important;
    }

    .stTextInput:has(.stTextInput-error) > div > input {
        border: 2px solid #ccc !important;
        box-shadow: none !important;
    }

    /* Hide 'Press Enter to submit form' message */
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
            <img src='https://raw.githubusercontent.com/KTrimmer123/CoL-Raingarden-Guide/main/assets/City_of_London_logo.svg.png' width='375'/>
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
        with st.container():
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
    st.stop()

# --- TOOL TITLE AFTER LOGIN ---
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

# --- RETURN PERIOD CHECK ---
if required:
    with st.expander("Return Period Check", expanded=True):
        result = pass_fail(required, available)
        for label, verdict in result.items():
            if verdict == "PASS":
                st.success(f"{label}: PASS")
            else:
                st.error(f"{label}: FAIL")
