# (same setup and calculation code as before above...)

# --- EXPORT SECTION ---
if required:
    st.markdown("### Export Results")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    df = pd.DataFrame({
        "Storm Duration": [storm_duration],
        "Catchment Area (m²)": [catchment],
        "Raingarden Area (m²)": [area],
        "Void Ratio": [void_ratio],
        "Depth (mm)": [depth],
        "Freeboard (mm)": [freeboard],
        "Include Infiltration": [include_infiltration],
        "Available Volume (m³)": [available],
        "Catchment Check": [catchment_result],
        "Timestamp": [timestamp]
    })

    for label, vol in required.items():
        df[f"{label} Required (m³)"] = [vol]
        df[f"{label} Result"] = [result.get(label, "-")]

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Raingarden Results")

    st.download_button(
        label="📥 Download Excel",
        data=buffer.getvalue(),
        file_name=f"raingarden_results_{timestamp}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # --- PDF Export (Fixed) ---
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "City of London Raingarden Results", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.ln(5)

    pdf.cell(0, 10, f"Timestamp: {timestamp}", ln=True)
    pdf.cell(0, 10, f"Catchment Area: {catchment} m²", ln=True)
    pdf.cell(0, 10, f"Raingarden Area: {area} m²", ln=True)
    pdf.cell(0, 10, f"Void Ratio: {void_ratio}", ln=True)
    pdf.cell(0, 10, f"Depth: {depth} mm", ln=True)
    pdf.cell(0, 10, f"Freeboard: {freeboard} mm", ln=True)
    pdf.cell(0, 10, f"Storm Duration: {storm_duration}", ln=True)
    pdf.cell(0, 10, f"Infiltration: {'Yes' if include_infiltration else 'No'}", ln=True)
    pdf.cell(0, 10, f"Available Volume: {available:.2f} m³", ln=True)
    pdf.cell(0, 10, f"Catchment Ratio Check: {catchment_result}", ln=True)
    pdf.ln(5)

    for label in required:
        pdf.cell(0, 10, f"{label} Required: {required[label]:.2f} m³ - {result.get(label, '-')}", ln=True)

    pdf_data = pdf.output(dest="S").encode("latin1")

    st.download_button(
        label="📥 Download PDF",
        data=pdf_data,
        file_name=f"raingarden_results_{timestamp}.pdf",
        mime="application/pdf"
    )
