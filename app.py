# --- CALCULATOR PAGE (sticky header already applied above) ---

st.markdown("---")  # Divider before Input

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

required = get_required_storage(catchment, storm_duration)
available = calculate_storage(area, void_ratio, depth, freeboard)

infiltration_rate = 0.036
storm_durations_hrs = {"1hr": 1, "3hr": 3, "6hr": 6}
if required and include_infiltration:
    duration_hr = storm_durations_hrs[storm_duration]
    infiltrated_volume = infiltration_rate * area * duration_hr
    for key in required:
        required[key] = max(required[key] - infiltrated_volume, 0)

st.markdown("---")  # Divider before Catchment Ratio

with st.expander("Catchment Ratio Check", expanded=False):
    if area >= 0.1 * catchment:
        st.success("PASS: Raingarden area is at least 10% of catchment")
    else:
        st.error("FAIL: Raingarden area is less than 10% of catchment")

st.markdown("---")  # Divider before Results

with st.expander("Results", expanded=False):
    if required:
        st.markdown(f"**Storage Required for {storm_duration} Storm**")
        for label, vol in required.items():
            st.write(f"{label}: {vol:.2f} m³")
        st.write(f"Available Volume in Raingarden: {available:.2f} m³")
    else:
        st.warning("Catchment size too large for FEH table.")

st.markdown("---")  # Divider before Return Period Check

if required:
    with st.expander("Return Period Check", expanded=False):
        result = pass_fail(required, available)
        for label, verdict in result.items():
            if verdict == "PASS":
                st.success(f"{label}: PASS")
            else:
                st.error(f"{label}: FAIL")
