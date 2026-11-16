
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import time

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Intelligent Bridge Monitoring",
    page_icon="🌉",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #101820;
    color: #edf4fa;
}
[data-testid="stSidebar"] {
    background-color: #172532;
}
.metric-card {
    background: #1c2d3b;
    border: 1px solid #344a5c;
    padding: 17px;
    border-radius: 10px;
    margin-bottom: 10px;
}
.metric-label {
    font-size: 12px;
    color: #9db4c6;
}
.metric-value {
    font-size: 27px;
    font-weight: 700;
    color: #eaf5ff;
}
.metric-unit {
    font-size: 11px;
    color: #91a9ba;
}
.section-title {
    color: #70c8ef;
    font-size: 19px;
    font-weight: 650;
}
.status-normal {
    color: #48dfa0;
    font-weight: bold;
}
.status-warning {
    color: #ffc46b;
    font-weight: bold;
}
.status-critical {
    color: #ff7777;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

if "sample" not in st.session_state:
    st.session_state.sample = 0

if "event_active" not in st.session_state:
    st.session_state.event_active = False

if "event_start" not in st.session_state:
    st.session_state.event_start = 0

if "event_history" not in st.session_state:
    st.session_state.event_history = []

if "simulation_running" not in st.session_state:
    st.session_state.simulation_running = True

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🌉 Intelligent Bridge Monitoring System")

st.caption(
    "Continuous Structural Health Monitoring | "
    "Event-Triggered Adaptive Sensor Attention"
)

st.divider()

# --------------------------------------------------
# SIDEBAR: SEVEN CONTROLS
# --------------------------------------------------

st.sidebar.title("Simulation Controls")
st.sidebar.caption("Configure the educational bridge simulation.")

vehicle_load = st.sidebar.slider(
    "1. Vehicle Load (tons)",
    2, 45, 18
)

vehicle_speed = st.sidebar.slider(
    "2. Vehicle Speed (km/h)",
    10, 110, 55
)

traffic_level = st.sidebar.slider(
    "3. Traffic Intensity (%)",
    0, 100, 45
)

stiffness_change = st.sidebar.slider(
    "4. Structural Change (%)",
    0, 30, 0
)

trigger_sensitivity = st.sidebar.slider(
    "5. Trigger Sensitivity (%)",
    10, 100, 65
)

persistence_window = st.sidebar.slider(
    "6. Persistence Window (samples)",
    3, 60, 15
)

sampling_interval = st.sidebar.selectbox(
    "7. Sampling Interval",
    [1, 2, 5, 10],
    index=1
)

st.sidebar.divider()

if st.sidebar.button("Simulate Structural Event", use_container_width=True):
    st.session_state.event_active = True
    st.session_state.event_start = st.session_state.sample
    st.session_state.event_history.append({
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Event": "Manual structural event simulation"
    })

if st.sidebar.button("Reset Simulation", use_container_width=True):
    st.session_state.history = []
    st.session_state.sample = 0
    st.session_state.event_active = False
    st.session_state.event_start = 0
    st.session_state.event_history = []
    st.rerun()

# --------------------------------------------------
# SENSOR SIMULATION ENGINE
# --------------------------------------------------

def generate_sensor_reading(sample):
    """
    Generate illustrative sensor measurements.
    These are simulated values, not actual bridge measurements.
    """

    rng = np.random.default_rng(sample + 2026)

    traffic_factor = traffic_level / 100
    load_factor = vehicle_load / 18
    speed_factor = vehicle_speed / 55

    structural_factor = stiffness_change / 100

    wave = np.sin(sample * 0.25)

    strain = (
        105
        + traffic_factor * load_factor * 25
        + structural_factor * 90
        + wave * 3
        + rng.normal(0, 1.5)
    )

    deflection = (
        2.7
        + traffic_factor * load_factor * 1.1
        + structural_factor * 3.2
        + rng.normal(0, 0.08)
    )

    vibration = (
        0.13
        + traffic_factor * speed_factor * 0.12
        + structural_factor * 0.30
        + abs(wave) * 0.03
        + rng.normal(0, 0.012)
    )

    temperature = (
        27.4
        + np.sin(sample * 0.02) * 1.2
        + rng.normal(0, 0.08)
    )

    tilt = (
        0.08
        + structural_factor * 0.6
        + rng.normal(0, 0.01)
    )

    humidity = (
        65
        + np.sin(sample * 0.015) * 4
        + rng.normal(0, 0.5)
    )

    corrosion = (
        0.15
        + structural_factor * 0.05
        + rng.normal(0, 0.005)
    )

    return {
        "Sample": sample,
        "Timestamp": datetime.now(),
        "Strain": strain,
        "Deflection": deflection,
        "Vibration": vibration,
        "Temperature": temperature,
        "Tilt": tilt,
        "Humidity": humidity,
        "Corrosion": corrosion,
        "Traffic": traffic_level,
        "Vehicle Load": vehicle_load,
        "Vehicle Speed": vehicle_speed
    }

# --------------------------------------------------
# SENSOR BASELINE
# --------------------------------------------------

BASELINE = {
    "Strain": 105,
    "Deflection": 2.7,
    "Vibration": 0.13,
    "Temperature": 27.4,
    "Tilt": 0.08,
    "Humidity": 65,
    "Corrosion": 0.15
}

def calculate_deviation(value, baseline):
    if baseline == 0:
        return 0
    return abs(value - baseline) / abs(baseline) * 100

def analyze_readings(reading):
    deviations = {
        key: calculate_deviation(reading[key], BASELINE[key])
        for key in BASELINE
    }

    maximum = max(deviations.values())

    threshold = 10 + trigger_sensitivity * 0.45

    return deviations, maximum, maximum >= threshold

# --------------------------------------------------
# GENERATE NEW SAMPLE
# --------------------------------------------------

if st.session_state.simulation_running:
    new_sample = generate_sensor_reading(
        st.session_state.sample
    )

    st.session_state.history.append(new_sample)
    st.session_state.sample += 1

    if len(st.session_state.history) > 500:
        st.session_state.history = st.session_state.history[-500:]

history_df = pd.DataFrame(st.session_state.history)

if history_df.empty:
    st.warning("Waiting for the first sensor reading.")
    st.stop()

latest = history_df.iloc[-1].to_dict()

deviations, maximum_deviation, signal_detected = analyze_readings(
    latest
)

# --------------------------------------------------
# EVENT-TRIGGERED ADAPTIVE ATTENTION
# --------------------------------------------------

if signal_detected:
    st.session_state.event_active = True
    st.session_state.event_start = st.session_state.sample

samples_since_trigger = (
    st.session_state.sample - st.session_state.event_start
)

if (
    st.session_state.event_active
    and samples_since_trigger >= persistence_window
    and not signal_detected
):
    st.session_state.event_active = False

adaptive_mode = st.session_state.event_active

if adaptive_mode:
    monitoring_status = "SPECIAL ATTENTION"
else:
    monitoring_status = "NORMAL MONITORING"

# --------------------------------------------------
# TOP STATUS
# --------------------------------------------------

status_col1, status_col2, status_col3, status_col4 = st.columns(4)

with status_col1:
    st.metric("System Status", "ONLINE")

with status_col2:
    st.metric("Monitoring Mode", monitoring_status)

with status_col3:
    st.metric("Samples Collected", st.session_state.sample)

with status_col4:
    st.metric("Maximum Deviation", f"{maximum_deviation:.2f}%")

st.divider()

# --------------------------------------------------
# FIVE ORIGINAL DASHBOARD TABS
# --------------------------------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Live Monitoring",
    "Event Detection",
    "Sensor History",
    "Data Export"
])

# ==================================================
# TAB 1: OVERVIEW
# ==================================================

with tab1:

    st.subheader("Bridge Monitoring Overview")

    st.markdown(
        "Continuous primary sensing with event-triggered "
        "adaptive attention."
    )

    cols = st.columns(4)

    metrics = [
        ("Deck Strain", latest["Strain"], "με"),
        ("Deflection", latest["Deflection"], "mm"),
        ("Vibration", latest["Vibration"], "mm/s"),
        ("Temperature", latest["Temperature"], "°C")
    ]

    for col, (name, value, unit) in zip(cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{name}</div>
                    <div class="metric-value">{value:.2f}</div>
                    <div class="metric-unit">{unit}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.subheader("Structural Sensor Status")

    sensor_data = pd.DataFrame({
        "Sensor": list(BASELINE.keys()),
        "Current Reading": [
            latest[k] for k in BASELINE
        ],
        "Baseline": [
            BASELINE[k] for k in BASELINE
        ],
        "Deviation (%)": [
            deviations[k] for k in BASELINE
        ]
    })

    st.dataframe(
        sensor_data,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Monitoring Architecture")

    st.markdown("""
    **NORMAL MODE**
    - Continuous strain monitoring
    - Continuous vibration monitoring
    - Continuous deflection monitoring
    - Continuous temperature monitoring

    **SPECIAL ATTENTION MODE**
    - Additional acoustic monitoring
    - Additional thermal analysis
    - Detailed tilt and displacement analysis
    - Extended signal observation
    - Persistence evaluation
    """)

    if adaptive_mode:
        st.warning(
            "Adaptive attention is active. "
            "Additional simulated monitoring channels are enabled."
        )
    else:
        st.success(
            "Normal monitoring mode is active."
        )

# ==================================================
# TAB 2: LIVE MONITORING
# ==================================================

with tab2:

    st.subheader("Live Sensor Monitoring")

    chart = make_subplots(
        rows=3,
        cols=1,
        subplot_titles=(
            "Strain",
            "Deflection",
            "Vibration"
        ),
        vertical_spacing=0.12
    )

    chart.add_trace(
        go.Scatter(
            x=history_df["Sample"],
            y=history_df["Strain"],
            name="Strain",
            line=dict(color="#48c9ef", width=2)
        ),
        row=1, col=1
    )

    chart.add_trace(
        go.Scatter(
            x=history_df["Sample"],
            y=history_df["Deflection"],
            name="Deflection",
            line=dict(color="#64dfa5", width=2)
        ),
        row=2, col=1
    )

    chart.add_trace(
        go.Scatter(
            x=history_df["Sample"],
            y=history_df["Vibration"],
            name="Vibration",
            line=dict(color="#f2b96e", width=2)
        ),
        row=3, col=1
    )

    chart.update_layout(
        height=680,
        template="plotly_dark",
        showlegend=False,
        margin=dict(l=15, r=15, t=50, b=20)
    )

    st.plotly_chart(
        chart,
        use_container_width=True
    )

    st.subheader("Additional Sensor Readings")

    extra_cols = st.columns(3)

    extra_metrics = [
        ("Tilt", latest["Tilt"], "degrees"),
        ("Humidity", latest["Humidity"], "%"),
        ("Corrosion Indicator", latest["Corrosion"], "index")
    ]

    for col, (name, value, unit) in zip(extra_cols, extra_metrics):
        with col:
            st.metric(name, f"{value:.3f} {unit}")

# ==================================================
# TAB 3: EVENT DETECTION
# ==================================================

with tab3:

    st.subheader("Event-Triggered Adaptive Attention")

    st.markdown("""
    The system continuously receives primary sensor readings.
    When a reading deviates sufficiently from its baseline,
    the system activates additional monitoring attention.
    """)

    if adaptive_mode:
        st.error("SPECIAL ATTENTION MODE ACTIVE")
    else:
        st.success("NORMAL MONITORING MODE")

    st.subheader("Baseline Comparison")

    deviation_df = pd.DataFrame({
        "Sensor": list(deviations.keys()),
        "Deviation (%)": list(deviations.values())
    })

    deviation_chart = go.Figure(
        go.Bar(
            x=deviation_df["Sensor"],
            y=deviation_df["Deviation (%)"],
            marker_color="#42bde9"
        )
    )

    deviation_chart.update_layout(
        template="plotly_dark",
        height=380,
        yaxis_title="Deviation (%)"
    )

    st.plotly_chart(
        deviation_chart,
        use_container_width=True
    )

    st.subheader("Event Interpretation")

    st.write(
        f"Maximum deviation: {maximum_deviation:.2f}%"
    )

    st.write(
        f"Trigger threshold: "
        f"{10 + trigger_sensitivity * 0.45:.2f}%"
    )

    st.write(
        f"Persistence observation: "
        f"{samples_since_trigger} samples"
    )

    if signal_detected:
        st.warning(
            "A simulated change signal has crossed the configured threshold."
        )
    else:
        st.info(
            "No simulated sensor deviation has crossed the trigger threshold."
        )

    if stiffness_change > 0:
        st.warning(
            "A persistent structural-change scenario has been configured "
            "in the simulation."
        )

    st.caption(
        "The persistence logic in this educational simulation is simplified. "
        "A real system would use validated multi-sensor trends and "
        "environmental compensation."
    )

    st.subheader("Event Log")

    if st.session_state.event_history:
        st.dataframe(
            pd.DataFrame(st.session_state.event_history),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No manually recorded events yet.")

# ==================================================
# TAB 4: SENSOR HISTORY
# ==================================================

with tab4:

    st.subheader("Long-Term Sensor History")

    st.write(
        f"Stored samples: {len(history_df)}"
    )

    selected_sensor = st.selectbox(
        "Select sensor",
        list(BASELINE.keys())
    )

    history_chart = go.Figure()

    history_chart.add_trace(
        go.Scatter(
            x=history_df["Sample"],
            y=history_df[selected_sensor],
            name="Measured value",
            mode="lines",
            line=dict(color="#50c9ef", width=2)
        )
    )

    history_chart.add_hline(
        y=BASELINE[selected_sensor],
        line_dash="dash",
        line_color="#f0bd6e",
        annotation_text="Initial baseline"
    )

    history_chart.update_layout(
        template="plotly_dark",
        height=430,
        xaxis_title="Sample",
        yaxis_title=selected_sensor
    )

    st.plotly_chart(
        history_chart,
        use_container_width=True
    )

    st.subheader("Recent Sensor Records")

    st.dataframe(
        history_df.tail(20),
        use_container_width=True,
        hide_index=True
    )

# ==================================================
# TAB 5: DATA EXPORT
# ==================================================

with tab5:

    st.subheader("Data Acquisition and Export")

    st.write(
        "Download the simulated sensor history for further analysis."
    )

    csv = history_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Sensor History CSV",
        data=csv,
        file_name="bridge_sensor_history.csv",
        mime="text/csv",
        use_container_width=True
    )

    event_df = pd.DataFrame(
        st.session_state.event_history
    )

    if not event_df.empty:
        event_csv = event_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇ Download Event Log CSV",
            data=event_csv,
            file_name="bridge_event_log.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.subheader("Simulation Configuration")

    configuration = pd.DataFrame({
        "Parameter": [
            "Vehicle Load",
            "Vehicle Speed",
            "Traffic Intensity",
            "Structural Change",
            "Trigger Sensitivity",
            "Persistence Window",
            "Sampling Interval"
        ],
        "Value": [
            vehicle_load,
            vehicle_speed,
            traffic_level,
            stiffness_change,
            trigger_sensitivity,
            persistence_window,
            sampling_interval
        ]
    })

    st.dataframe(
        configuration,
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "INTELLIGENT BRIDGE MONITORING SYSTEM | "
    "Educational simulation only. "
    "All generated sensor readings are illustrative, "
    "not real structural measurements."
)
