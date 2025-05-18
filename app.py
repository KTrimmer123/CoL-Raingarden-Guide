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

    .centered-logo {
        display: flex;
        justify-content: center;
        margin-top: -2rem;
        margin-bottom: 0.5rem;
    }

    .login-heading {
        text-align: center;
        font-family: 'Poppins', sans-serif;
        font-size: 2.5rem;
        font-weight: 600;
        line-height: 2.2rem;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
    }

    .enginuity-logo {
        margin-top: 1.75rem;
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
            <p>
                This tool is the intellectual property of the Enginuity Collective and is made available solely for professional use. It has been developed to support the delivery of sustainable drainage systems (SuDS) and climate-resilient urban design. Use of this tool is intended exclusively for qualified civil engineers and built environment professionals with the appropriate expertise to interpret and apply the outputs responsibly. Unauthorised distribution or misuse is strictly prohibited.<br><br>
                For troubleshooting or professional advice on the use of this tool, please contact <a href="mailto:info@enginuitydesign.co.uk">info@enginuitydesign.co.uk</a>.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# --- CALCULATOR PAGE ---
st.title("City of London Raingarden Guide")

# (Calculator logic continues as before...)
