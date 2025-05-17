import streamlit as st
from calculator import calculate_storage, get_required_storage, pass_fail
from datetime import datetime
from fpdf import FPDF
import pandas as pd
import io

st.set_page_config(page_title="City of London Raingarden Guide", page_icon="💧")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- CSS Styling ---
if not st.session_state.logged_in:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&family=Poppins:wght@500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    h1 { font-family: 'Poppins', sans-serif !important; text-align: center; }
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

    with st.form("login_form"):
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if st.session_state.username == "city_of_london_rg_tool" and st.session_state.password == "SuDSnotfloods!":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Incorrect username or password")

    st.markdown("""
    <div class='enginuity-logo'>
        <div style="text-align: center;">
            <img src='https://raw.githubusercontent.com/KTrimmer123/CoL-Raingarden-Guide/main/assets/Enginuity_logo.jpg' width='240'/><br>
            <p style="font-size: 0.85rem; color: #555;">
                This tool is the intellectual property of the Enginuity Collective and is provided for professional use in support of sustainable drainage and climate-resilient design. It is intended for use by qualified civil engineers.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# --- CALCULATOR PAGE ---
st.title("City of London Raingarden Guide")

with st.expander("Input Parameters", expanded=False):
    area = st.number_input(
        "Raingarden Area (m²)",
        min_value=1,
        value=10,
        step=1,
        format="%d",
        help="Area of the raingarden available"
    )

    catchment = st.number_input(
        "Catchment Area (m²)",
        min_value=1,
        value=100,
        step=1,
        format="%d",
        help="Total catchment drained to raingarden (including raingarden area itself)"
    )

    void_options = {
        "Coarse Graded Aggregate": 0.3,
        "Hydrorock": 0.94,
        "Geocellular": 0.95
    }
    void_label = st.selectbox(
        "Attenuation Form",
        list(void_options.keys()),
        help="Material used for surface water attenuation (void ratio selection)"
    )
    void_ratio = void_options[void_label]

    depth = int(st.number_input(
        "Attenuation Depth (mm)",
        min_value=0,
        value=300,
        step=5,
        format="%d"
    ))

    freeboard = st.selectbox(
        "Freeboard (mm)",
        [150, 200, 250],
        help="Water storage above the planting level but contained within the kerb"
    )

    storm_duration = st.selectbox(
        "Storm Duration",
        ["1hr", "3hr", "6hr"],
        help="Length of rainfall event used in the storage design. Select 1-hr as default"
    )

    include_infiltration = st.checkbox(
        "Include infiltration in storage calculation",
        value=False,
        help="Apply the average infiltration rate across the City"
    )

# -- Calculations and Results (unchanged from before) --
# (omitted here for space, but let me know if you want the full app with calculations + export too)
