import streamlit as st
from calculator import calculate_storage, get_required_storage, pass_fail

st.set_page_config(page_title="City of London Raingarden Guide", page_icon="💧")

# Left-align everything with padding
st.markdown(
    """
    <style>
    .block-container {
        text-align: left;
        padding-left: 2rem;
        padding-right: 2rem;
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
        st.rerun()
    elif username and password:
        st.error("Incorrect username or password")
    st.stop()

# ---- CALCULATOR ----
st.title("City of London Raingarden Guide")

st.subheader("Input Parameters")
area = st.number_input("Raingarden Area (m²)", min_value=1.0, value=10.0)
catchment = st.number_input("Catchment Area (m²)", min_value=1.0, value=100.0)

void_options = {
