
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Intelligent Bridge Monitoring",
    page_icon="🌉",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    margin: 0 !important;
    padding: 0 !important;
    background: #071522 !important;
}
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
footer {
    display: none !important;
}
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
iframe {
    border: 0 !important;
}
</style>
""", unsafe_allow_html=True)

BRIDGE_MODEL_URL = (
    "https://raw.githubusercontent.com/"
    "experimentscience/bridge-monitoring-stem/"
    "main/assets/cable-stayed-bridge.glb"
)

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
* { box-sizing: border-box; }

html, body {
    margin: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    font-family: Inter, Arial, sans-serif;
    color: white;
    background: #91c9e9;
}

#scene {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
}

#scene canvas {
    display: block;
}

.vignette {
    position: fixed;
    inset: 0;
    z-index: 1;
    pointer-events: none;
    background:
      linear-gradient(180deg, rgba(5,20,35,.26), transparent 24%),
      linear-gradient(0deg, rgba(3,18,30,.40), transparent 32%),
      linear-gradient(90deg, rgba(3,18,30,.20), transparent 35%, transparent 70%, rgba(3,18,30,.18));
}

.panel {
    position: fixed;
    z-index: 3;
    background: linear-gradient(
        145deg,
        rgba(8,27,43,.78),
        rgba(10,35,53,.55)
    );
    border: 1px solid rgba(180,225,255,.25);
    box-shadow:
        0 12px 45px rgba(0,0,0,.24),
        inset 0 1px 0 rgba(255,255,255,.10);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-radius: 13px;
}

#header {
    top: 17px;
    left: 20px;
    right: 20px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
}

.brand {
    display: flex;
    align-items: center;
    gap: 13px;
}

.brand-icon {
    width: 38px;
    height: 38px;
    display: grid;
    place-items: center;
    border-radius: 10px;
    background: rgba(40,170,220,.20);
    border: 1px solid rgba(100,210,255,.35);
    font-size: 21px;
}

.brand-title {
    font-size: 16px;
    font-weight: 750;
    letter-spacing: .3px;
}

.brand-sub {
    font-size: 10px;
    color: #a6c6d8;
    margin-top: 4px;
    letter-spacing: 1.7px;
}

.header-right {
    display: flex;
    gap: 24px;
    align-items: center;
    font-size: 11px;
}

.status {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #d5e8f3;
}

.dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #55e5a1;
    box-shadow: 0 0 12px #55e5a1;
}

.mode-pill {
    padding: 8px 12px;
    border-radius: 20px;
    border: 1px solid rgba(80,220,170,.35);
    background: rgba(35,180,125,.13);
    color: #7ef0bd;
    font-size: 10px;
    letter-spacing: 1px;
}

#left {
    top: 98px;
    left: 20px;
    width: 255px;
    padding: 17px;
}

#right {
    top: 98px;
    right: 20px;
    width: 285px;
    padding: 17px;
}

.section-title {
    font-size: 10px;
    color: #8fb4ca;
    letter-spacing: 1.8px;
    font-weight: 700;
    margin-bottom: 14px;
}

.control {
    margin-bottom: 16px;
}

.control-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11px;
    color: #d6e7f0;
    margin-bottom: 7px;
}

.control-value {
    color: #6bd7ff;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
}

input[type=range] {
    width: 100%;
    accent-color: #45c8f4;
    cursor: pointer;
}

select {
    width: 100%;
    padding: 9px;
    border-radius: 7px;
    background: rgba(4,20,34,.8);
    color: white;
    border: 1px solid rgba(160,210,240,.25);
    outline: none;
    font-size: 11px;
}

.action-row {
    display: flex;
    gap: 8px;
    margin-top: 12px;
}

button {
    cursor: pointer;
    border: 1px solid rgba(120,205,245,.30);
    border-radius: 7px;
    color: white;
    background: rgba(35,130,175,.25);
    padding: 9px 11px;
    font-size: 10px;
    font-weight: 700;
    transition: .2s;
}

button:hover {
    background: rgba(45,175,225,.42);
    border-color: rgba(130,225,255,.7);
}

button.primary {
    background: linear-gradient(110deg,#087fae,#16a9cb);
    border: none;
}

button.active {
    border-color: #5ce8ae;
    color: #8bf3c5;
    background: rgba(45,190,130,.18);
}

.metric-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 9px;
    margin-bottom: 17px;
}

.metric {
    background: rgba(255,255,255,.045);
    border: 1px solid rgba(180,220,245,.10);
    border-radius: 9px;
    padding: 11px;
}

.metric-label {
    color: #8eafc2;
    font-size: 9px;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

.metric-number {
    font-size: 21px;
    font-weight: 750;
    font-variant-numeric: tabular-nums;
}

.metric-unit {
    font-size: 10px;
    color: #91b1c5;
    margin-left: 3px;
}

.metric-note {
    font-size: 9px;
    color: #8edbb8;
    margin-top: 5px;
}

.sensor-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 9px 0;
    border-bottom: 1px solid rgba(180,220,245,.10);
    font-size: 10px;
}

.sensor-name {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #d4e5ee;
}

.sensor-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #55e5a1;
    box-shadow: 0 0 8px #55e5a1;
}

.sensor-dot.red {
    background: #ff6577;
    box-shadow: 0 0 8px #ff6577;
}

.sensor-state {
    color: #80dcb6;
    font-size: 9px;
}

.sensor-state.red {
    color: #ff8793;
}

.alert-box {
    padding: 11px;
    border-radius: 8px;
    background: rgba(65,170,125,.10);
    border: 1px solid rgba(85,220,155,.22);
    margin-top: 14px;
}

.alert-heading {
    color: #79e4b1;
    font-size: 10px;
    font-weight: 750;
    letter-spacing: .7px;
    margin-bottom: 6px;
}

.alert-text {
    font-size: 10px;
    color: #c0d8e5;
    line-height: 1.55;
}

#bottom {
    bottom: 17px;
    left: 20px;
    right: 20px;
    min-height: 91px;
    display: grid;
    grid-template-columns: 1.1fr 1fr 1.25fr 1fr;
    align-items: center;
    padding: 12px 18px;
    gap: 20px;
}

.bottom-block {
    min-width: 0;
    border-right: 1px solid rgba(180,220,245,.14);
    padding-right: 14px;
}

.bottom-block:last-child {
    border: none;
}

.bottom-label {
    font-size: 9px;
    color: #8eafc2;
    letter-spacing: 1.2px;
    margin-bottom: 8px;
}

.bottom-value {
    font-size: 15px;
    font-weight: 700;
}

.bottom-small {
    font-size: 9px;
    color: #a8c5d4;
    margin-top: 5px;
}

.bar {
    height: 5px;
    width: 100%;
    background: rgba(255,255,255,.12);
    border-radius: 8px;
    overflow: hidden;
    margin-top: 8px;
}

.bar-fill {
    height: 100%;
    width: 35%;
    background: linear-gradient(90deg,#28b7e6,#6ce6b0);
    border-radius: 8px;
}

#loading {
    position: fixed;
    inset: 0;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    background: linear-gradient(150deg,#83b9d8,#d0e8ef);
    color: #12334a;
    transition: opacity .8s;
}

.loader-ring {
    width: 48px;
    height: 48px;
    border: 3px solid rgba(20,70,100,.15);
    border-top-color: #087fae;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 18px;
}

@keyframes spin { to { transform: rotate(360deg); } }

#loading-title {
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 2px;
}

#loading-message {
    font-size: 11px;
    margin-top: 9px;
    opacity: .7;
}

#model-error {
    display: none;
    position: fixed;
    z-index: 8;
    left: 50%;
    top: 50%;
    transform: translate(-50%,-50%);
    background: rgba(20,35,50,.92);
    border: 1px solid rgba(255,150,150,.4);
    padding: 18px;
    border-radius: 10px;
    max-width: 420px;
    font-size: 12px;
    line-height: 1.6;
}

#camera-label {
    position: fixed;
    z-index: 2;
    right: 25px;
    bottom: 126px;
    color: rgba(255,255,255,.8);
    font-size: 9px;
    letter-spacing: 1.5px;
    text-shadow: 0 2px 5px #123;
    pointer-events: none;
}

@media(max-width:900px) {
    #left { width: 215px; }
    #right { width: 235px; }
    #bottom { grid-template-columns: 1fr 1fr; }
}

@media(max-width:650px) {
    #header { left: 8px; right: 8px; top: 8px; }
    #left { left: 8px; top: 82px; width: 190px; }
    #right { right: 8px; top: 82px; width: 190px; }
    #bottom { left: 8px; right: 8px; bottom: 8px; }
    .header-right { gap: 8px; }
}
</style>
</head>

<body>
<div id="scene"></div>
<div class="vignette"></div>

<div id="loading">
    <div class="loader-ring"></div>
    <div id="loading-title">INTELLIGENT BRIDGE SYSTEM</div>
    <div id="loading-message">Initializing 3D environment and bridge model...</div>
</div>

<div id="model-error">
    <strong>Bridge model could not be loaded.</strong>
    <br>
    Check that the GLB file exists in the GitHub assets folder,
    that the repository is public, and that the model URL is accessible.
    <br><br>
    <span id="model-error-detail"></span>
</div>

<header id="header" class="panel">
    <div class="brand">
        <div class="brand-icon">🌉</div>
        <div>
            <div class="brand-title">INTELLIGENT BRIDGE MONITORING</div>
            <div class="brand-sub">STRUCTURAL INTELLIGENCE PLATFORM</div>
        </div>
    </div>
    <div class="header-right">
        <div class="status"><span class="dot"></span> SYSTEM ONLINE</div>
        <div class="mode-pill" id="mode-pill">CONTINUOUS MONITORING</div>
        <div id="clock">--:--:--</div>
    </div>
</header>

<aside id="left" class="panel">
    <div class="section-title">SIMULATION CONTROL</div>

    <div class="control">
        <div class="control-head">
            <span>Vehicle load</span>
            <span class="control-value" id="weight-value">18 tons</span>
        </div>
        <input id="weight" type="range" min="2" max="40" value="18">
    </div>

    <div class="control">
        <div class="control-head">
            <span>Vehicle speed</span>
            <span class="control-value" id="speed-value">55 km/h</span>
        </div>
        <input id="speed" type="range" min="10" max="110" value="55">
    </div>

    <div class="control">
        <div class="control-head">
            <span>Traffic intensity</span>
            <span class="control-value" id="traffic-value">65%</span>
        </div>
        <input id="traffic" type="range" min="0" max="100" value="65">
    </div>

    <div class="control">
        <div class="control-head">
            <span>Structural change</span>
            <span class="control-value" id="change-value">0%</span>
        </div>
        <input id="change" type="range" min="0" max="30" value="0">
    </div>

    <div class="control">
        <div class="control-head"><span>Monitoring mode</span></div>
        <select id="monitor-mode">
            <option value="adaptive">Adaptive monitoring</option>
            <option value="continuous">Continuous only</option>
            <option value="attention">Special attention test</option>
        </select>
    </div>

    <div class="control">
        <div class="control-head"><span>Event sensitivity</span></div>
        <input id="sensitivity" type="range" min="10" max="90" value="55">
    </div>

    <div class="action-row">
        <button class="primary" id="start">PAUSE SIMULATION</button>
        <button id="reset">RESET</button>
    </div>
    <div class="action-row">
        <button id="camera-reset">RESET CAMERA</button>
        <button id="export">EXPORT CSV</button>
    </div>
</aside>

<aside id="right" class="panel">
    <div class="section-title">LIVE STRUCTURAL TELEMETRY</div>

    <div class="metric-grid">
        <div class="metric">
            <div class="metric-label">STRAIN</div>
            <div class="metric-number"><span id="strain">142</span><span class="metric-unit">με</span></div>
            <div class="metric-note">Primary sensor</div>
        </div>
        <div class="metric">
            <div class="metric-label">DEFLECTION</div>
            <div class="metric-number"><span id="deflection">4.2</span><span class="metric-unit">mm</span></div>
            <div class="metric-note">Deck response</div>
        </div>
        <div class="metric">
            <div class="metric-label">VIBRATION</div>
            <div class="metric-number"><span id="vibration">0.18</span><span class="metric-unit">g</span></div>
            <div class="metric-note">Dynamic response</div>
        </div>
        <div class="metric">
            <div class="metric-label">TEMPERATURE</div>
            <div class="metric-number"><span id="temperature">28.4</span><span class="metric-unit">°C</span></div>
            <div class="metric-note">Deck sensor</div>
        </div>
    </div>

    <div class="section-title">SENSOR NETWORK</div>

    <div class="sensor-row">
        <div class="sensor-name"><span class="sensor-dot"></span> Strain sensors</div>
        <div class="sensor-state">ACTIVE</div>
    </div>
    <div class="sensor-row">
        <div class="sensor-name"><span class="sensor-dot"></span> Vibration sensors</div>
        <div class="sensor-state">ACTIVE</div>
    </div>
    <div class="sensor-row">
        <div class="sensor-name"><span class="sensor-dot"></span> Temperature sensors</div>
        <div class="sensor-state">ACTIVE</div>
    </div>
    <div class="sensor-row">
        <div class="sensor-name"><span class="sensor-dot red"></span> Extra attention sensors</div>
        <div class="sensor-state red" id="extra-state">STANDBY</div>
    </div>

    <div class="alert-box" id="alert-box">
        <div class="alert-heading" id="alert-heading">● STRUCTURAL STATUS: NORMAL</div>
        <div class="alert-text" id="alert-text">
            Primary sensors are continuously monitoring the bridge.
            No unusual response is currently detected.
        </div>
    </div>
</aside>

<div id="camera-label">INTERACTIVE 3D ENVIRONMENT · DRAG TO ORBIT · SCROLL TO ZOOM</div>

<footer id="bottom" class="panel">
    <div class="bottom-block">
        <div class="bottom-label">TRAFFIC FLOW</div>
        <div class="bottom-value"><span id="traffic-bottom">65</span>%</div>
        <div class="bottom-small">Relative to normal traffic</div>
        <div class="bar"><div class="bar-fill" id="traffic-bar"></div></div>
    </div>

    <div class="bottom-block">
        <div class="bottom-label">VEHICLES ON BRIDGE</div>
        <div class="bottom-value"><span id="vehicle-count">4</span></div>
        <div class="bottom-small">Simulated traffic count</div>
    </div>

    <div class="bottom-block">
        <div class="bottom-label">EVENT DETECTION</div>
        <div class="bottom-value" id="event-state">NO EVENT</div>
        <div class="bottom-small" id="event-description">Baseline response within expected range</div>
    </div>

    <div class="bottom-block">
        <div class="bottom-label">PERSISTENCE ANALYSIS</div>
        <div class="bottom-value" id="persistence">NO CHANGE</div>
        <div class="bottom-small" id="persistence-description">No persistent deviation detected</div>
    </div>
</footer>

<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
  }
}
</script>

<script type="module">
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { Sky } from "three/addons/objects/Sky.js";

const MODEL_URL = "__MODEL_URL__";

const container = document.getElementById("scene");

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x9ccfe9);
scene.fog = new THREE.FogExp2(0x9ccfe9, 0.00085);

const camera = new THREE.PerspectiveCamera(
    42,
    window.innerWidth / window.innerHeight,
    0.1,
    5000
);
camera.position.set(0, 75, 155);

const renderer = new THREE.WebGLRenderer({
    antialias: true,
    alpha: false,
    powerPreference: "high-performance"
});

renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.12;
container.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.045;
controls.target.set(0, 23, 0);
controls.maxPolarAngle = Math.PI * 0.49;
controls.minDistance = 35;
controls.maxDistance = 330;
controls.autoRotate = false;

scene.add(new THREE.HemisphereLight(0xd9efff, 0x52715b, 2.1));

const sunLight = new THREE.DirectionalLight(0xfff0d5, 3.0);
sunLight.position.set(-100, 150, 90);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(2048, 2048);
sunLight.shadow.camera.left = -180;
sunLight.shadow.camera.right = 180;
sunLight.shadow.camera.top = 180;
sunLight.shadow.camera.bottom = -180;
scene.add(sunLight);

const sky = new Sky();
sky.scale.setScalar(4500);
scene.add(sky);

sky.material.uniforms.turbidity.value = 7;
sky.material.uniforms.rayleigh.value = 2.4;
sky.material.uniforms.mieCoefficient.value = 0.004;
sky.material.uniforms.mieDirectionalG.value = 0.78;

const sunDirection = new THREE.Vector3();
sunDirection.setFromSphericalCoords(
    1,
    THREE.MathUtils.degToRad(83),
    THREE.MathUtils.degToRad(205)
);
sky.material.uniforms.sunPosition.value.copy(sunDirection);

const waterGeometry = new THREE.PlaneGeometry(5000, 5000);
const waterMaterial = new THREE.MeshPhysicalMaterial({
    color: 0x3188a7,
    roughness: 0.24,
    metalness: 0.12,
    clearcoat: 0.8,
    clearcoatRoughness: 0.18
});
const water = new THREE.Mesh(waterGeometry, waterMaterial);
water.rotation.x = -Math.PI / 2;
water.position.y = -5;
water.receiveShadow = true;
scene.add(water);

const terrainMaterial = new THREE.MeshStandardMaterial({
    color: 0x527d54,
    roughness: 1
});

function createHill(x, z, sx, sy, sz) {
    const hill = new THREE.Mesh(
        new THREE.SphereGeometry(1, 40, 32),
        terrainMaterial
    );
    hill.position.set(x, -4, z);
    hill.scale.set(sx, sy, sz);
    hill.receiveShadow = true;
    hill.castShadow = true;
    scene.add(hill);
}

createHill(-250, -170, 180, 40, 110);
createHill(220, -210, 190, 50, 130);
createHill(-370, 20, 130, 35, 100);
createHill(370, 30, 150, 38, 120);

const farGreen = new THREE.MeshStandardMaterial({
    color: 0x63865b,
    roughness: 1
});

for (let i = 0; i < 35; i++) {
    const x = (Math.random() - 0.5) * 850;
    const z = -180 - Math.random() * 200;
    const tree = new THREE.Group();

    const trunk = new THREE.Mesh(
        new THREE.CylinderGeometry(0.5, 0.8, 8, 8),
        new THREE.MeshStandardMaterial({color:0x70533b})
    );
    trunk.position.y = 4;
    tree.add(trunk);

    const crown = new THREE.Mesh(
        new THREE.SphereGeometry(5 + Math.random() * 3, 12, 10),
        farGreen
    );
    crown.position.y = 10;
    tree.add(crown);

    tree.position.set(x, -4, z);
    scene.add(tree);
}

const bridgeRoot = new THREE.Group();
scene.add(bridgeRoot);

const sensorGroup = new THREE.Group();
scene.add(sensorGroup);

const vehicleGroup = new THREE.Group();
scene.add(vehicleGroup);

let bridgeLoaded = false;
let bridgeLength = 200;
let bridgeWidth = 18;
let bridgeHeight = 45;
let bridgeTop = 25;

function showError(message) {
    document.getElementById("model-error").style.display = "block";
    document.getElementById("model-error-detail").textContent = message;
}

function makeSensor(position, color, radius=1.0) {
    const group = new THREE.Group();

    const material = new THREE.MeshStandardMaterial({
        color,
        emissive: color,
        emissiveIntensity: 1.6,
        roughness: 0.25,
        metalness: 0.2
    });

    const core = new THREE.Mesh(
        new THREE.SphereGeometry(radius, 18, 18),
        material
    );
    group.add(core);

    const ring = new THREE.Mesh(
        new THREE.TorusGeometry(radius * 1.8, 0.10, 8, 32),
        material
    );
    ring.rotation.x = Math.PI / 2;
    group.add(ring);

    const glow = new THREE.PointLight(color, 3, 13);
    group.add(glow);

    group.position.copy(position);
    group.userData.ring = ring;
    sensorGroup.add(group);

    return group;
}

function installSensors() {
    sensorGroup.clear();

    const half = bridgeLength * 0.42;
    const z = 0;

    for (let i = 0; i < 9; i++) {
        const x = -half + (2 * half * i / 8);
        makeSensor(
            new THREE.Vector3(x, bridgeTop + 1.2, z),
            0x45efac,
            0.65
        );
    }

    const extraPositions = [
        [-half * 0.55, bridgeTop + 3, -bridgeWidth * 0.35],
        [0, bridgeTop + 3, -bridgeWidth * 0.35],
        [half * 0.55, bridgeTop + 3, -bridgeWidth * 0.35],
        [-half * 0.55, bridgeTop + 3, bridgeWidth * 0.35],
        [0, bridgeTop + 3, bridgeWidth * 0.35],
        [half * 0.55, bridgeTop + 3, bridgeWidth * 0.35]
    ];

    extraPositions.forEach(p => {
        const s = makeSensor(
            new THREE.Vector3(p[0], p[1], p[2]),
            0xff526a,
            0.55
        );
        s.visible = false;
        s.userData.extra = true;
    });
}

function normalizeBridge(model) {
    const box = new THREE.Box3().setFromObject(model);
    const size = new THREE.Vector3();
    const center = new THREE.Vector3();
    box.getSize(size);
    box.getCenter(center);

    if (!isFinite(size.x) || !isFinite(size.y) || !isFinite(size.z)) {
        throw new Error("The model has invalid dimensions.");
    }

    // Center the model around its bounding-box center.
    model.position.sub(center);

    // Scale the model to a useful visualization size.
    const longest = Math.max(size.x, size.y, size.z);
    const scale = 220 / longest;
    model.scale.setScalar(scale);

    // Recalculate dimensions after scaling.
    const scaledBox = new THREE.Box3().setFromObject(model);
    const scaledSize = new THREE.Vector3();
    scaledBox.getSize(scaledSize);

    bridgeLength = Math.max(scaledSize.x, scaledSize.z);
    bridgeWidth = Math.min(scaledSize.x, scaledSize.z);
    bridgeHeight = scaledSize.y;

    // The asset is expected to have its road deck approximately horizontal.
    // This centers the model at the scene origin without changing its orientation.
    const finalBox = new THREE.Box3().setFromObject(model);
    model.position.y -= finalBox.min.y;

    bridgeTop = Math.max(5, scaledSize.y * 0.45);

    model.traverse(child => {
        if (child.isMesh) {
            child.castShadow = true;
            child.receiveShadow = true;

            if (child.material) {
                child.material.needsUpdate = true;
            }
        }
    });

    bridgeRoot.add(model);

    controls.target.set(0, Math.max(15, scaledSize.y * 0.35), 0);
    camera.position.set(0, Math.max(55, scaledSize.y * 0.8), Math.max(130, bridgeLength * 0.72));

    installSensors();
}

const loader = new GLTFLoader();

loader.load(
    MODEL_URL,
    gltf => {
        try {
            normalizeBridge(gltf.scene);
            bridgeLoaded = true;
            document.getElementById("loading-message").textContent =
                "Bridge model loaded. Preparing monitoring environment...";
            setTimeout(() => {
                const loading = document.getElementById("loading");
                loading.style.opacity = "0";
                setTimeout(() => loading.remove(), 900);
            }, 600);
        } catch (e) {
            showError("Model loaded but could not be positioned: " + e.message);
            document.getElementById("loading-message").textContent =
                "Bridge model setup failed.";
        }
    },
    xhr => {
        if (xhr.total) {
            const percent = Math.round(xhr.loaded / xhr.total * 100);
            document.getElementById("loading-message").textContent =
                "Loading bridge model: " + percent + "%";
        }
    },
    error => {
        console.error("GLB load error:", error);
        showError("Loading failed. Check the GitHub raw URL, filename, and repository visibility.");
        document.getElementById("loading-message").textContent =
            "Unable to load bridge model.";
    }
);

const vehicleMaterials = [
    new THREE.MeshStandardMaterial({color:0xe8f0f5, metalness:.65, roughness:.3}),
    new THREE.MeshStandardMaterial({color:0x183f5d, metalness:.55, roughness:.35}),
    new THREE.MeshStandardMaterial({color:0xd6a94b, metalness:.5, roughness:.35}),
    new THREE.MeshStandardMaterial({color:0xb6c4ce, metalness:.6, roughness:.3})
];

function createVehicle(index) {
    const group = new THREE.Group();
    const material = vehicleMaterials[index % vehicleMaterials.length];

    const body = new THREE.Mesh(
        new THREE.BoxGeometry(7, 2.5, 3.2),
        material
    );
    body.position.y = 2;
    body.castShadow = true;
    group.add(body);

    const cabin = new THREE.Mesh(
        new THREE.BoxGeometry(3.1, 1.8, 2.9),
        new THREE.MeshPhysicalMaterial({
            color:0x91c7df,
            metalness:.45,
            roughness:.15,
            transparent:true,
            opacity:.85
        })
    );
    cabin.position.set(-.8, 3.9, 0);
    group.add(cabin);

    for (const x of [-2.2, 2.2]) {
        for (const z of [-1.65, 1.65]) {
            const wheel = new THREE.Mesh(
                new THREE.CylinderGeometry(.65,.65,.35,20),
                new THREE.MeshStandardMaterial({color:0x17212a, roughness:.85})
            );
            wheel.rotation.x = Math.PI / 2;
            wheel.position.set(x, .85, z);
            group.add(wheel);
        }
    }

    vehicleGroup.add(group);
    return {
        group,
        progress: Math.random(),
        speed: .00035 + Math.random() * .0002
    };
}

const vehicles = [];
for (let i = 0; i < 6; i++) {
    vehicles.push(createVehicle(i));
}

let running = true;
let elapsed = 0;
let eventDuration = 0;
let persistentDuration = 0;
let history = [];

const weightInput = document.getElementById("weight");
const speedInput = document.getElementById("speed");
const trafficInput = document.getElementById("traffic");
const changeInput = document.getElementById("change");
const modeInput = document.getElementById("monitor-mode");
const sensitivityInput = document.getElementById("sensitivity");

function updateSliderLabels() {
    document.getElementById("weight-value").textContent =
        weightInput.value + " tons";
    document.getElementById("speed-value").textContent =
        speedInput.value + " km/h";
    document.getElementById("traffic-value").textContent =
        trafficInput.value + "%";
    document.getElementById("change-value").textContent =
        changeInput.value + "%";
}

[weightInput, speedInput, trafficInput, changeInput].forEach(el => {
    el.addEventListener("input", updateSliderLabels);
});

function setExtraSensors(active) {
    sensorGroup.children.forEach(sensor => {
        if (sensor.userData.extra) {
            sensor.visible = active;
        }
    });
    document.getElementById("extra-state").textContent =
        active ? "ACTIVE" : "STANDBY";
    document.getElementById("extra-state").className =
        active ? "sensor-state red" : "sensor-state";
}

function updateVehiclePositions() {
    const traffic = Number(trafficInput.value) / 100;
    const activeCount = Math.max(0, Math.round(traffic * vehicles.length));

    vehicles.forEach((vehicle, i) => {
        const visible = i < activeCount;
        vehicle.group.visible = visible;

        if (!visible) return;

        vehicle.progress += vehicle.speed * (Number(speedInput.value) / 55);
        if (vehicle.progress > 1) vehicle.progress = 0;

        const x = -bridgeLength * 0.42 +
            vehicle.progress * bridgeLength * 0.84;

        const z = 0;
        vehicle.group.position.set(x, bridgeTop + 0.2, z);
    });

    document.getElementById("vehicle-count").textContent = activeCount;
    document.getElementById("traffic-bottom").textContent = trafficInput.value;
    document.getElementById("traffic-bar").style.width = trafficInput.value + "%";
}

function updateTelemetry(dt) {
    const weight = Number(weightInput.value);
    const speed = Number(speedInput.value);
    const traffic = Number(trafficInput.value);
    const structuralChange = Number(changeInput.value);
    const sensitivity = Number(sensitivityInput.value);
    const mode = modeInput.value;

    const wave = Math.sin(elapsed * 1.8);
    const smallWave = Math.sin(elapsed * 4.2);

    const temporaryLoad = weight * (traffic / 100) * (speed / 55);
    const baselineStrain = 90 + temporaryLoad * 2.8;
    const measuredStrain = baselineStrain + wave * 5 +
        structuralChange * 1.7;

    const deflection = 1.4 + temporaryLoad * .095 +
        Math.abs(wave) * .25 + structuralChange * .075;

    const vibration = .06 + (speed / 110) * .10 +
        (traffic / 100) * .045 + Math.abs(smallWave) * .018;

    const temperature = 28.4 + Math.sin(elapsed * .05) * .5;

    document.getElementById("strain").textContent =
        measuredStrain.toFixed(0);
    document.getElementById("deflection").textContent =
        deflection.toFixed(2);
    document.getElementById("vibration").textContent =
        vibration.toFixed(3);
    document.getElementById("temperature").textContent =
        temperature.toFixed(1);

    const deviation = structuralChange > 0;
    const eventScore = Math.min(
        100,
        Math.round(
            (Math.abs(measuredStrain - baselineStrain) * .7) +
            (vibration * 100) +
            structuralChange * 1.5
        )
    );

    const eventDetected = eventScore >= sensitivity * .65 || deviation;
    const attentionActive =
        mode === "attention" ||
        (mode === "adaptive" && eventDetected);

    setExtraSensors(attentionActive);

    if (eventDetected) eventDuration += dt;
    else eventDuration = Math.max(0, eventDuration - dt * .6);

    if (deviation && eventDuration > 5) persistentDuration += dt;
    else persistentDuration = Math.max(0, persistentDuration - dt * .5);

    const persistent = persistentDuration > 8;

    const pill = document.getElementById("mode-pill");
    pill.textContent = attentionActive
        ? "SPECIAL ATTENTION ACTIVE"
        : "CONTINUOUS MONITORING";

    document.getElementById("event-state").textContent =
        eventDetected ? "EVENT DETECTED" : "NO EVENT";

    document.getElementById("event-description").textContent =
        eventDetected
        ? "Additional measurements are being collected"
        : "Baseline response within expected range";

    document.getElementById("persistence").textContent =
        persistent ? "PERSISTENT DEVIATION" :
        deviation ? "OBSERVING" : "NO CHANGE";

    document.getElementById("persistence-description").textContent =
        persistent
        ? "Deviation has continued beyond the observation window"
        : deviation
        ? "Waiting for repeated measurements"
        : "No persistent deviation detected";

    const alertHeading = document.getElementById("alert-heading");
    const alertText = document.getElementById("alert-text");

    if (persistent) {
        alertHeading.textContent = "● PERSISTENT CHANGE INDICATOR";
        alertHeading.style.color = "#ff8c99";
        alertText.textContent =
            "The simulation shows a continuing deviation from the baseline. " +
            "Additional sensor data is active for comparison.";
    } else if (eventDetected) {
        alertHeading.textContent = "● EVENT UNDER OBSERVATION";
        alertHeading.style.color = "#ffd27c";
        alertText.textContent =
            "A response outside the selected trigger threshold has been detected. " +
            "The system is collecting additional measurements.";
    } else {
        alertHeading.textContent = "● STRUCTURAL STATUS: NORMAL";
        alertHeading.style.color = "#79e4b1";
        alertText.textContent =
            "Primary sensors are continuously monitoring the bridge. " +
            "No unusual response is currently detected.";
    }

    history.push({
        time: new Date().toISOString(),
        strain: measuredStrain.toFixed(2),
        deflection: deflection.toFixed(3),
        vibration: vibration.toFixed(4),
        temperature: temperature.toFixed(2),
        traffic,
        weight,
        speed,
        event: eventDetected,
        special_attention: attentionActive,
        structural_change: structuralChange,
        persistent_indicator: persistent
    });

    if (history.length > 1500) history.shift();
}

document.getElementById("start").addEventListener("click", () => {
    running = !running;
    document.getElementById("start").textContent =
        running ? "PAUSE SIMULATION" : "RESUME SIMULATION";
});

document.getElementById("reset").addEventListener("click", () => {
    weightInput.value = 18;
    speedInput.value = 55;
    trafficInput.value = 65;
    changeInput.value = 0;
    sensitivityInput.value = 55;
    modeInput.value = "adaptive";

    elapsed = 0;
    eventDuration = 0;
    persistentDuration = 0;
    history = [];

    updateSliderLabels();
    setExtraSensors(false);
});

document.getElementById("camera-reset").addEventListener("click", () => {
    camera.position.set(
        0,
        Math.max(55, bridgeHeight * .8),
        Math.max(130, bridgeLength * .72)
    );
    controls.target.set(0, Math.max(15, bridgeHeight * .35), 0);
    controls.update();
});

document.getElementById("export").addEventListener("click", () => {
    if (!history.length) {
        alert("No simulation data has been collected yet.");
        return;
    }

    const headers = Object.keys(history[0]);
    const csv = [
        headers.join(","),
        ...history.map(row =>
            headers.map(key => row[key]).join(",")
        )
    ].join("\n");

    const blob = new Blob([csv], {type:"text/csv"});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "bridge-monitoring-simulation.csv";
    a.click();
    URL.revokeObjectURL(url);
});

modeInput.addEventListener("change", () => {
    if (modeInput.value === "continuous") {
        document.getElementById("mode-pill").textContent =
            "CONTINUOUS MONITORING";
    }
});

let lastTime = performance.now();

function animate(now) {
    requestAnimationFrame(animate);

    const dt = Math.min((now - lastTime) / 1000, .05);
    lastTime = now;

    if (running) {
        elapsed += dt;
        updateVehiclePositions();
        updateTelemetry(dt);
    }

    sensorGroup.children.forEach(sensor => {
        if (sensor.userData.ring) {
            sensor.userData.ring.rotation.z += dt * 1.2;
        }
    });

    waterMaterial.color.offsetHSL(0, 0, 0);

    controls.update();
    renderer.render(scene, camera);

    document.getElementById("clock").textContent =
        new Date().toLocaleTimeString();
}

requestAnimationFrame(animate);

window.addEventListener("resize", () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
</script>
</body>
</html>
"""

html = html.replace("__MODEL_URL__", BRIDGE_MODEL_URL)

components.html(
    html,
    height=1100,
    scrolling=False,
)

