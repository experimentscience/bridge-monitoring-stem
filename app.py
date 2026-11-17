    normal_chart.update_layout(title="Always-on Sensor Patterns", xaxis_title="Bridge position (m)", yaxis_title="Reading / visual scale", height=340)
    st.plotly_chart(normal_chart, use_container_width=True)

    st.divider()
    st.subheader("Special-Attention-Only Sensors")
    if special_mode:
        st.warning("ACTIVE: 6 additional sensor types are reporting at 11 stations (66 additional readings).")
        special_table = {"Station (m)": np.round(sensor_positions, 1)}
        special_table.update(special_data)
        st.dataframe(special_table, use_container_width=True, hide_index=True, height=360)

        special_chart = go.Figure()
        special_chart.add_trace(go.Scatter(x=sensor_positions, y=tilt_degrees, mode="lines+markers", name="Tilt proxy (°)"))
        special_chart.add_trace(go.Scatter(x=sensor_positions, y=crack_width_proxy, mode="lines+markers", name="Crack-width proxy (mm)"))
        special_chart.add_trace(go.Scatter(x=sensor_positions, y=joint_displacement_mm, mode="lines+markers", name="Joint displacement proxy (mm)"))
        special_chart.update_layout(title="Special-Attention Sensor Patterns", xaxis_title="Bridge position (m)", yaxis_title="Modeled indicator", height=330)
        st.plotly_chart(special_chart, use_container_width=True)
    else:
        st.info("STANDBY: Tilt, humidity, corrosion, crack-width, acoustic-activity, and joint-displacement channels are not collecting special-mode readings.")

    st.caption("All non-deflection channels are educational simulated indicators or proxies, not calibrated measurements from physical sensors.")

# TAB 3: adaptive attention and change detection
with tab_change:
    st.subheader("Adaptive Attention Decision")
    c1, c2, c3 = st.columns(3)
    c1.metric("Baseline peak", f"{baseline_peak:.3f} mm")
    c2.metric("Current peak", f"{changed_peak:.3f} mm")
    c3.metric("Response increase", f"{response_increase:.1f}%")

    st.write(f"Deflection trigger: **{trigger:.2f} mm**")
    st.write(f"Stations exceeding trigger: **{int(np.sum(sensor_attention))} of {len(sensor_positions)}**")
    if persistent_change and np.any(sensor_attention):
        st.warning("PERSISTENT CHANGE DETECTED — SPECIAL ATTENTION ACTIVE")
        st.write("The baseline comparison detected a response increase, and one or more always-on deflection sensors exceeded the trigger.")
    elif persistent_change:
        st.warning("PERSISTENT CHANGE DETECTED — SPECIAL ATTENTION ACTIVE")
        st.write("The baseline comparison triggered special attention even though no individual deflection station crossed the absolute trigger.")
    elif np.any(sensor_attention):
        st.warning("SENSOR ATTENTION ACTIVE — PERSISTENT CHANGE NOT CONFIRMED")
        st.write("A sensor crossed the attention trigger, but the overall baseline comparison stayed below the persistent-change criterion.")
    else:
        st.success("NORMAL MODE — SPECIAL-ATTENTION SENSORS ON STANDBY")

    fig = go.Figure(go.Bar(
        x=["Original bridge", "Changed bridge"],
        y=[baseline_peak, changed_peak],
        text=[f"{baseline_peak:.3f} mm", f"{changed_peak:.3f} mm"],
        textposition="outside",
    ))
    fig.update_layout(title="Baseline vs. Changed Bridge Response", yaxis_title="Maximum deflection (mm)", height=330)
    st.plotly_chart(fig, use_container_width=True)

    sensor_plot = go.Figure(go.Bar(x=sensor_positions, y=deflection_mm, name="Deflection"))
    sensor_plot.add_hline(y=trigger, line_dash="dash", annotation_text="Attention trigger")
    sensor_plot.update_layout(title="Always-on Deflection Stations", xaxis_title="Station (m)", yaxis_title="Deflection (mm)", height=320)
    st.plotly_chart(sensor_plot, use_container_width=True)

    st.caption("The persistent-change criterion is a modeled 5% increase from baseline. This is an educational threshold, not an engineering inspection rule.")

# TAB 4: simplified localization illustration
with tab_localization:
    st.subheader("Structural Change Localization")
    st.write("This separate illustration creates a modeled sensor-response pattern around the selected location.")
    local_shape = np.exp(-((sensor_positions - local_location) ** 2) / (2 * 4.0**2))
    local_signal = local_reduction * local_shape
    nearest_index = int(np.argmax(local_signal))
    nearest_position = float(sensor_positions[nearest_index])

    loc_fig = go.Figure(go.Bar(
        x=[f"{p:.1f} m" for p in sensor_positions],
        y=local_signal,
        marker_color=["red" if i == nearest_index else "seagreen" for i in range(len(sensor_positions))],
    ))
    loc_fig.update_layout(title="Illustrative Local Sensor Signal", xaxis_title="Sensor station", yaxis_title="Signal strength (%)", height=330)
    st.plotly_chart(loc_fig, use_container_width=True)
    st.info(f"Strongest modeled response: station at {nearest_position:.1f} m.")
    st.caption("This Gaussian pattern is an illustrative mathematical demonstration, not a verified crack-location algorithm.")

# TAB 5: session history + CSV export
with tab_history:
    st.subheader("Bridge History & Long-Term Trends")
    st.write("Save snapshots of different simulation settings and compare them.")
    if "bridge_history" not in st.session_state:
        st.session_state.bridge_history = []

    if st.button("Save Current Simulation Reading", key="save_history"):
        st.session_state.bridge_history.append({
            "Saved at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Vehicle weight (N)": int(weight),
            "Axles": int(axles),
            "Axle spacing (m)": float(spacing),
            "Stiffness reduction (%)": int(stiffness_change),
            "Baseline deflection (mm)": round(baseline_peak, 3),
            "Current deflection (mm)": round(changed_peak, 3),
            "Response increase (%)": round(response_increase, 1),
            "Special mode": bool(special_mode),
            "Always-on alerts": int(np.sum(sensor_attention)),
        })
        st.success("Simulation snapshot saved in this session.")

    history = st.session_state.bridge_history
    if history:
        st.metric("Saved snapshots", len(history))
        hist_fig = go.Figure()
        hist_fig.add_trace(go.Scatter(x=[r["Saved at"] for r in history], y=[r["Baseline deflection (mm)"] for r in history], mode="lines+markers", name="Baseline"))
        hist_fig.add_trace(go.Scatter(x=[r["Saved at"] for r in history], y=[r["Current deflection (mm)"] for r in history], mode="lines+markers", name="Current"))
        hist_fig.update_layout(title="Saved Simulation Response History", xaxis_title="Saved snapshot", yaxis_title="Deflection (mm)", height=330)
        st.plotly_chart(hist_fig, use_container_width=True)
        st.dataframe(history, use_container_width=True, hide_index=True, height=250)

        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=list(history[0].keys()))
        writer.writeheader()
        writer.writerows(history)
        st.download_button("Download History CSV", buffer.getvalue(), file_name="bridge_history.csv", mime="text/csv")
    else:
        st.info("No snapshots saved yet. Change the simulation settings and click Save Current Simulation Reading.")

    st.caption("Session history may clear when the app restarts. Download the CSV to preserve records. These are simulation snapshots, not real bridge sensor logs.")

st.caption("Educational simulation using a simplified beam model. It is not a real bridge measurement system or a certified structural safety assessment.")
