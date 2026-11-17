
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import csv
import io
from datetime import datetime

st.set_page_config(
    page_title="Intelligent Bridge Monitoring",
    page_icon="🌉",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {max-width: 1320px; padding-top: 1rem;}
    section[data-testid="stSidebar"] {background: #f1f5f9;}
    div[data-testid="stMetric"] {
        background: white; border: 1px solid #dbe4ee;
        padding: 12px; border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌉 Intelligent Bridge Monitoring System")
st.caption("Continuous monitoring • Event-triggered special attention • Structural change detection")

# Simplified simply-supported beam model.
# Additional sensor channels are simulated indicators, not real instrument measurements.
L = 30.0
E = 200e9
I = 0.08
x = np.linspace(0, L, 401)
sensor_positions = np.linspace(2.0, 28.0, 11)

# ---------------- Sidebar controls ----------------
st.sidebar.header("Vehicle Simulation")
weight = st.sidebar.slider("Vehicle weight (N)", 5000, 100000, 20000, 5000)
axles = st.sidebar.slider("Number of axles", 2, 5, 4)
spacing = st.sidebar.slider("Axle spacing (m)", 2.0, 8.0, 3.0, 0.5)

st.sidebar.header("Adaptive Monitoring")
trigger = st.sidebar.slider("Deflection attention trigger (mm)", 0.1, 5.0, 0.7, 0.1)

st.sidebar.header("Structural Change Experiment")
stiffness_change = st.sidebar.slider("Global stiffness reduction (%)", 0, 30, 15, 5)

st.sidebar.header("Localization Demonstration")
local_location = st.sidebar.slider("Simulated change location (m)", 3, 27, 15, 3)
local_reduction = st.sidebar.slider("Local change signal (%)", 5, 30, 15, 5)


def beam_response(vehicle_position: float, inertia: float):
    """Return moment and deflection arrays for the moving multi-axle load."""
    moment = np.zeros_like(x)
    deflection = np.zeros_like(x)
    axle_load = weight / axles

    for axle_index in range(axles):
        a = vehicle_position - axle_index * spacing
        if 0.0 <= a <= L:
            b = L - a
            moment += np.where(
                x <= a,
                axle_load * b * x / L,
                axle_load * a * (L - x) / L,
            )

            left = x <= a
            right = ~left
            deflection[left] += (
                axle_load * b * x[left]
                * (L**2 - b**2 - x[left]**2)
                / (6 * L * E * inertia)
            )
            deflection[right] += (
                axle_load * a * (L - x[right])
                * (L**2 - a**2 - (L - x[right])**2)
                / (6 * L * E * inertia)
            )

    return moment, deflection


# ---------------- Baseline and changed bridge responses ----------------
changed_inertia = I * (1 - stiffness_change / 100.0)
vehicle_positions = np.linspace(-axles * spacing, L, 140)

moment_envelope = np.zeros_like(x)
baseline_envelope = np.zeros_like(x)
current_envelope = np.zeros_like(x)

for vehicle_position in vehicle_positions:
    moment, baseline_deflection = beam_response(vehicle_position, I)
    _, current_deflection = beam_response(vehicle_position, changed_inertia)
    moment_envelope = np.maximum(moment_envelope, moment)
    baseline_envelope = np.maximum(baseline_envelope, np.abs(baseline_deflection))
    current_envelope = np.maximum(current_envelope, np.abs(current_deflection))

baseline_peak = float(np.max(baseline_envelope) * 1000)
changed_peak = float(np.max(current_envelope) * 1000)
peak_moment = float(np.max(moment_envelope))
response_increase = (
    (changed_peak - baseline_peak) / baseline_peak * 100.0
    if baseline_peak > 0 else 0.0
)

# ---------------- Five always-on sensor types ----------------
deflection_mm = np.interp(sensor_positions, x, current_envelope) * 1000.0
baseline_deflection_mm = np.interp(sensor_positions, x, baseline_envelope) * 1000.0

# Strain is a simplified outer-fibre proxy derived from the deflection shape.
curvature = np.gradient(np.gradient(current_envelope, x), x)
strain_micro = np.interp(sensor_positions, x, np.abs(curvature)) * 0.5 * 1e6

# Vibration is a simplified response-amplitude index, not measured acceleration.
vibration_index = 0.15 + deflection_mm * 4.0

# Environmental and load channels are synthetic scenario indicators.
temperature_c = 22.0 + 3.0 * np.sin(np.pi * sensor_positions / L)
traffic_load_index = np.clip(
    (weight / 100000.0) * 100.0 * (0.65 + 0.35 * np.sin(np.pi * sensor_positions / L)),
    0, 100,
)

normal_data = {
    "Deflection (mm)": np.round(deflection_mm, 3),
    "Strain proxy (µε)": np.round(strain_micro, 2),
    "Vibration index": np.round(vibration_index, 3),
    "Temperature (°C)": np.round(temperature_c, 2),
    "Traffic/load index (%)": np.round(traffic_load_index, 1),
}

# Special attention activates from the live deflection trigger
# or the separate baseline comparison rule.
sensor_attention = deflection_mm > trigger
persistent_change = response_increase >= 5.0
special_mode = bool(np.any(sensor_attention) or persistent_change)

# ---------------- Six special-attention-only sensor types ----------------
local_shape = np.exp(-((sensor_positions - local_location) ** 2) / (2 * 4.0**2))

tilt_degrees = np.round(deflection_mm * 0.002, 4)
humidity_percent = np.round(48 + 17 * np.sin(2 * np.pi * sensor_positions / L), 1)
corrosion_indicator = np.round(np.clip((humidity_percent - 45) * 2.0, 0, 100), 1)
crack_width_proxy = np.round(local_reduction / 1000.0 * local_shape, 4)
acoustic_activity_proxy = np.round((local_reduction * local_shape) * 1.8, 1)
joint_displacement_mm = np.round(deflection_mm * 0.18 + local_shape * 0.03, 4)

special_data = {
    "Tilt proxy (°)": tilt_degrees,
    "Humidity (%)": humidity_percent,
    "Corrosion indicator (%)": corrosion_indicator,
    "Crack-width proxy (mm)": crack_width_proxy,
    "Acoustic activity proxy": acoustic_activity_proxy,
    "Joint displacement proxy (mm)": joint_displacement_mm,
}

# ---------------- Five compact tabs ----------------
tab_overview, tab_sensors, tab_change, tab_localization, tab_history = st.tabs([
    "📊 Overview & Bridge",
    "📡 Sensor Network",
    "🔍 Change Detection",
    "📍 Localization",
    "📈 History & Long-Term Trends",
])

# TAB 1: Overview and 3D sensor layout
with tab_overview:
    st.subheader("Simulation Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Maximum bending moment", f"{peak_moment:,.0f} Nm")
    c2.metric("Maximum deflection", f"{changed_peak:.3f} mm")
    c3.metric("Always-on readings", f"{len(sensor_positions) * 5}")
    c4.metric("Special-attention readings", f"{len(sensor_positions) * 6 if special_mode else 0}")

    if special_mode:
        st.warning("SPECIAL-ATTENTION MODE ACTIVE — 6 extra sensor types are reporting.")
    else:
        st.success("NORMAL MODE — 5 sensor types are continuously reporting; 6 types are on standby.")

    st.subheader("3D Bridge Sensor Network")
    st.caption("Each sensor row represents one sensor type at 11 locations along the 30 m bridge.")

    fig3d = go.Figure()
    fig3d.add_trace(go.Mesh3d(
        x=[0, 30, 30, 0], y=[-2, -2, 2, 2], z=[2, 2, 2, 2],
        i=[0, 0], j=[1, 2], k=[2, 3],
        color="lightblue", opacity=0.55, name="Bridge deck",
    ))

    for y_side in [-1.65, 1.65]:
        fig3d.add_trace(go.Scatter3d(
            x=[0, 30], y=[y_side, y_side], z=[1.55, 1.55],
            mode="lines", line=dict(color="gray", width=8),
            name="Main support beam", showlegend=(y_side < 0),
        ))

    active_types = [
        ("Deflection", "royalblue"),
        ("Strain", "seagreen"),
        ("Vibration", "darkorange"),
        ("Temperature", "mediumpurple"),
        ("Traffic/load", "deepskyblue"),
    ]

    if special_mode:
        active_types += [
            ("Tilt", "crimson"),
            ("Humidity", "deeppink"),
            ("Corrosion", "saddlebrown"),
            ("Crack-width", "magenta"),
            ("Acoustic activity", "goldenrod"),
            ("Joint displacement", "dimgray"),
        ]

    row_positions = np.linspace(-1.35, 1.35, len(active_types))

    for row_y, (sensor_name, color) in zip(row_positions, active_types):
        fig3d.add_trace(go.Scatter3d(
            x=sensor_positions,
            y=[row_y] * len(sensor_positions),
            z=[2.22] * len(sensor_positions),
            mode="markers",
            marker=dict(size=5 if special_mode else 6, color=color),
            name=sensor_name,
        ))

    fig3d.update_layout(
        height=420,
        margin=dict(l=0, r=0, t=20, b=0),
        scene=dict(
            xaxis=dict(title="Bridge length (m)", range=[0, 30]),
            yaxis=dict(title="Sensor rows", range=[-2, 2]),
            zaxis=dict(title="Height", range=[0, 4]),
            aspectratio=dict(x=2.5, y=0.7, z=0.5),
            camera=dict(eye=dict(x=0.25, y=-2.4, z=1.1)),
        ),
        legend=dict(orientation="h"),
    )
    st.plotly_chart(fig3d, width="stretch")

    with st.expander("Sensor color key", expanded=False):
        st.write("🔵 Deflection  •  🟢 Strain  •  🟠 Vibration  •  🟣 Temperature  •  🩵 Traffic/load")
        st.write("🔴 Tilt  •  💗 Humidity  •  🤎 Corrosion  •  🟪 Crack-width  •  🟡 Acoustic activity  •  ⚫ Joint displacement")

    c1, c2 = st.columns(2)

    with c1:
        fig = go.Figure(go.Scatter(
            x=x, y=moment_envelope, mode="lines", name="Bending moment"
        ))
        fig.update_layout(
            title="Bending Moment Along Bridge",
            xaxis_title="Position (m)",
            yaxis_title="Moment (Nm)",
            height=290,
        )
        st.plotly_chart(fig, width="stretch")

    with c2:
        fig = go.Figure(go.Scatter(
            x=x, y=current_envelope * 1000, mode="lines", name="Current deflection"
        ))
        fig.update_layout(
            title="Bridge Deflection",
            xaxis_title="Position (m)",
            yaxis_title="Deflection (mm)",
            height=290,
        )
        st.plotly_chart(fig, width="stretch")


# TAB 2: Sensor readings
with tab_sensors:
    st.subheader("Sensor Network — 11 Stations Along the Bridge")
    st.write("Five sensor types report continuously at all 11 stations: **55 normal-mode readings**.")

    normal_table = {"Station (m)": np.round(sensor_positions, 1)}
    normal_table.update(normal_data)
    st.dataframe(normal_table, width="stretch", hide_index=True, height=360)

    normal_chart = go.Figure()
    normal_chart.add_trace(go.Scatter(
        x=sensor_positions, y=deflection_mm,
        mode="lines+markers", name="Deflection (mm)"
    ))
    normal_chart.add_trace(go.Scatter(
        x=sensor_positions, y=vibration_index,
        mode="lines+markers", name="Vibration index"
    ))
    normal_chart.add_trace(go.Scatter(
        x=sensor_positions, y=traffic_load_index / 20.0,
        mode="lines+markers", name="Load index ÷ 20 (visual scale)"
    ))
    normal_chart.update_layout(
        title="Always-on Sensor Patterns",
        xaxis_title="Bridge position (m)",
        yaxis_title="Reading / visual scale",
        height=340,
    )
    st.plotly_chart(normal_chart, width="stretch")

    st.divider()
    st.subheader("Special-Attention-Only Sensors")

    if special_mode:
        st.warning("ACTIVE: 6 additional sensor types are reporting at 11 stations (66 additional readings).")

        special_table = {"Station (m)": np.round(sensor_positions, 1)}
        special_table.update(special_data)
        st.dataframe(special_table, width="stretch", hide_index=True, height=360)

        special_chart = go.Figure()
        special_chart.add_trace(go.Scatter(
            x=sensor_positions, y=tilt_degrees,
            mode="lines+markers", name="Tilt proxy (°)"
        ))
        special_chart.add_trace(go.Scatter(
            x=sensor_positions, y=crack_width_proxy,
            mode="lines+markers", name="Crack-width proxy (mm)"
        ))
        special_chart.add_trace(go.Scatter(
            x=sensor_positions, y=joint_displacement_mm,
            mode="lines+markers", name="Joint displacement proxy (mm)"
        ))
        special_chart.update_layout(
            title="Special-Attention Sensor Patterns",
            xaxis_title="Bridge position (m)",
            yaxis_title="Modeled indicator",
            height=330,
        )
        st.plotly_chart(special_chart, width="stretch")
    else:
        st.info(
            "STANDBY: Tilt, humidity, corrosion, crack-width, acoustic-activity, "
            "and joint-displacement channels are not collecting special-mode readings."
        )

    st.caption(
        "All non-deflection channels are educational simulated indicators or proxies, "
        "not calibrated measurements from physical sensors."
    )


# TAB 3: Adaptive attention and change detection
with tab_change:
    st.subheader("Adaptive Attention Decision")
    c1, c2, c3 = st.columns(3)
    c1.metric("Baseline peak", f"{baseline_peak:.3f} mm")
    c2.metric("Current peak", f"{changed_peak:.3f} mm")
    c3.metric("Response increase", f"{response_increase:.1f}%")

    st.write(f"Deflection trigger: **{trigger:.2f} mm**")
    st.write(
        f"Stations exceeding trigger: **{int(np.sum(sensor_attention))} "
        f"of {len(sensor_positions)}**"
    )

    if persistent_change and np.any(sensor_attention):
        st.warning("PERSISTENT CHANGE DETECTED — SPECIAL ATTENTION ACTIVE")
        st.write(
            "The baseline comparison detected a response increase, and one or more "
            "always-on deflection sensors exceeded the trigger."
        )
    elif persistent_change:
        st.warning("PERSISTENT CHANGE DETECTED — SPECIAL ATTENTION ACTIVE")
        st.write(
            "The baseline comparison triggered special attention even though no "
            "individual deflection station crossed the absolute trigger."
        )
    elif np.any(sensor_attention):
        st.warning("SENSOR ATTENTION ACTIVE — PERSISTENT CHANGE NOT CONFIRMED")
        st.write(
            "A sensor crossed the attention trigger, but the overall baseline "
            "comparison stayed below the persistent-change criterion."
        )
    else:
        st.success("NORMAL MODE — SPECIAL-ATTENTION SENSORS ON STANDBY")

    fig = go.Figure(go.Bar(
        x=["Original bridge", "Changed bridge"],
        y=[baseline_peak, changed_peak],
        text=[f"{baseline_peak:.3f} mm", f"{changed_peak:.3f} mm"],
        textposition="outside",
    ))
    fig.update_layout(
        title="Baseline vs. Changed Bridge Response",
        yaxis_title="Maximum deflection (mm)",
        height=330,
    )
    st.plotly_chart(fig, width="stretch")

    sensor_plot = go.Figure(go.Bar(
        x=sensor_positions, y=deflection_mm, name="Deflection"
    ))
    sensor_plot.add_hline(
        y=trigger, line_dash="dash", annotation_text="Attention trigger"
    )
    sensor_plot.update_layout(
        title="Always-on Deflection Stations",
        xaxis_title="Station (m)",
        yaxis_title="Deflection (mm)",
        height=320,
    )
    st.plotly_chart(sensor_plot, width="stretch")

    st.caption(
        "The persistent-change criterion is a modeled 5% increase from baseline. "
        "This is an educational threshold, not an engineering inspection rule."
    )


# TAB 4: Structural change localization
with tab_localization:
    st.subheader("Structural Change Localization")
    st.write(
        "This separate illustration creates a modeled sensor-response pattern "
        "around the selected location."
    )

    local_shape = np.exp(
        -((sensor_positions - local_location) ** 2) / (2 * 4.0**2)
    )
    local_signal = local_reduction * local_shape
    nearest_index = int(np.argmax(local_signal))
    nearest_position = float(sensor_positions[nearest_index])

    loc_fig = go.Figure(go.Bar(
        x=[f"{p:.1f} m" for p in sensor_positions],
        y=local_signal,
        marker_color=[
            "red" if i == nearest_index else "seagreen"
            for i in range(len(sensor_positions))
        ],
    ))
    loc_fig.update_layout(
        title="Illustrative Local Sensor Signal",
        xaxis_title="Sensor station",
        yaxis_title="Signal strength (%)",
        height=330,
    )
    st.plotly_chart(loc_fig, width="stretch")

    st.info(f"Strongest modeled response: station at {nearest_position:.1f} m.")
    st.caption(
        "This Gaussian pattern is an illustrative mathematical demonstration, "
        "not a verified crack-location algorithm."
    )


# TAB 5: Session history and CSV export
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
        hist_fig.add_trace(go.Scatter(
            x=[r["Saved at"] for r in history],
            y=[r["Baseline deflection (mm)"] for r in history],
            mode="lines+markers",
            name="Baseline",
        ))
        hist_fig.add_trace(go.Scatter(
            x=[r["Saved at"] for r in history],
            y=[r["Current deflection (mm)"] for r in history],
            mode="lines+markers",
            name="Current",
        ))
        hist_fig.update_layout(
            title="Saved Simulation Response History",
            xaxis_title="Saved snapshot",
            yaxis_title="Deflection (mm)",
            height=330,
        )
        st.plotly_chart(hist_fig, width="stretch")

        st.dataframe(history, width="stretch", hide_index=True, height=250)

        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=list(history[0].keys()))
        writer.writeheader()
        writer.writerows(history)

        st.download_button(
            "Download History CSV",
            buffer.getvalue(),
            file_name="bridge_history.csv",
            mime="text/csv",
        )
    else:
        st.info(
            "No snapshots saved yet. Change the simulation settings and click "
            "Save Current Simulation Reading."
        )

    st.caption(
        "Session history may clear when the app restarts. Download the CSV to "
        "preserve records. These are simulation snapshots, not real bridge sensor logs."
    )


st.caption(
    "Educational simulation using a simplified beam model. It is not a real bridge "
    "measurement system or a certified structural safety assessment."
)
