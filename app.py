import streamlit as st
from calculator import calculate_storage, get_required_storage, pass_fail

st.set_page_config(page_title="City of London Raingarden Guide", page_icon="💧")

# Stronger left-align styling for all app content
st.markdown(
    """
    <style>
    /* Force main container to left-align */
    .main .block-container {
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        text-align: left !important;
    }

    /* Align headers */
    h1, h2, h3, h4 {
        text-align: left !important;
    }

    /* Align metric outputs */
    .stMetric {
        text-align: left !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- SIMPLE LOGIN ----
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
