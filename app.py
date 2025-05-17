import streamlit as st
from calculator import calculate_storage, get_required_storage, pass_fail

st.set_page_config(page_title="City of London Raingarden Guide", page_icon="💧")

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
    "Coarse Graded Aggregate": 0.3,
    "Hydrorock": 0.4,
    "Geocellular": 0.94
}
void_label = st.selectbox("Attenuation Form", list(void_options.keys()))
void_ratio = void_options[void_label]

depth = st.number_input("Attenuation Depth (mm)", min_value=0.0, value=300.0)
freeboard = st.selectbox("Freeboard (mm)", [150, 200, 250])
storm_duration = st.selectbox("Storm Duration", ["1hr", "3hr", "6hr"])

# ---- CALCULATIONS ----
required = get_required_storage(catchment, storm_duration)
available = calculate_storage(area, void_ratio, depth, freeboard)


st.subheader("Catchment Ratio Check")
if area >= 0.1 * catchment:
    st.success("PASS: Raingarden area is at least 10% of catchment")
else:
    st.error("FAIL: Raingarden area is less than 10% of catchment")

st.subheader("Results")


if required:
    st.markdown(f"**Storage Required for {storm_duration} Storm**")
    for label, vol in required.items():
        st.write(f"{label}: {vol:.2f} m³")

    st.metric("Available Volume in Raingarden", f"{available:.2f} m³")

    result = pass_fail(required, available)
    st.subheader("Return Period Check")
    for label, verdict in result.items():
        if verdict == "PASS":
            st.success(f"{label}: PASS")
        else:
            st.error(f"{label}: FAIL")
else:
    st.warning("Catchment size too large for FEH table.")
