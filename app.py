
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Intelligent Bridge Monitoring",
    page_icon="🌉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], [data-testid="stMainBlockContainer"],
[data-testid="stVerticalBlock"], .stApp {
    margin: 0 !important;
    padding: 0 !important;
    max-width: 100% !important;
    background: #07121b !important;
}
[data-testid="stHeader"], [data-testid="stToolbar"],
[data-testid="stSidebar"], footer {
    display: none !important;
}
iframe {
    display: block;
    border: 0 !important;
}
</style>
""", unsafe_allow_html=True)

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
* { box-sizing:border-box; }
html, body {
    margin:0;
    width:100%;
    height:100%;
    overflow:hidden;
    font-family:Inter,Arial,sans-serif;
    background:#86b8d8;
    color:white;
}
#scene {
    position:fixed;
    inset:0;
    width:100%;
    height:100%;
    z-index:0;
}
canvas { display:block; }

.glass {
    background:linear-gradient(145deg,
        rgba(12,28,43,.80),
        rgba(13,37,54,.57));
    border:1px solid rgba(210,238,255,.25);
    box-shadow:0 12px 40px rgba(0,0,0,.20),
               inset 0 1px rgba(255,255,255,.12);
    backdrop-filter:blur(18px);
    -webkit-backdrop-filter:blur(18px);
    border-radius:13px;
}
#topbar {
    position:absolute;
    z-index:5;
    top:15px;
    left:18px;
    right:18px;
    height:64px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:0 20px;
}
.brand {
    display:flex;
    align-items:center;
    gap:13px;
}
.logo {
    width:38px;
    height:38px;
    border-radius:10px;
    display:grid;
    place-items:center;
    background:rgba(72,183,220,.2);
    border:1px solid rgba(120,220,255,.4);
    font-size:20px;
}
.brand h1 {
    font-size:16px;
    margin:0;
    letter-spacing:1.2px;
    font-weight:700;
}
.brand small {
    display:block;
    color:#a8c7d8;
    margin-top:4px;
    font-size:10px;
    letter-spacing:1.5px;
}
.topstatus {
    display:flex;
    align-items:center;
    gap:22px;
    font-size:11px;
    color:#d3e8f5;
}
.statusdot {
    width:8px;height:8px;border-radius:50%;
    display:inline-block;margin-right:7px;
    background:#4de4a1;
    box-shadow:0 0 12px #4de4a1;
}
#left {
    position:absolute;
    z-index:5;
    top:94px;
    left:18px;
    width:260px;
    padding:17px;
}
#right {
    position:absolute;
    z-index:5;
    top:94px;
    right:18px;
    width:285px;
    padding:17px;
}
.paneltitle {
    font-size:11px;
    font-weight:700;
    letter-spacing:1.6px;
    color:#a9d8ec;
    margin-bottom:15px;
    text-transform:uppercase;
}
.section {
    border-top:1px solid rgba(255,255,255,.12);
    padding-top:13px;
    margin-top:13px;
}
.sectionlabel {
    color:#9bb8c9;
    font-size:10px;
    text-transform:uppercase;
    letter-spacing:1px;
    margin-bottom:10px;
}
.control {
    margin:12px 0;
}
.controlhead {
    display:flex;
    justify-content:space-between;
    font-size:11px;
    margin-bottom:7px;
    color:#d9e9f2;
}
.controlhead strong { color:#fff; }
input[type=range] {
    width:100%;
    accent-color:#42c7e8;
    cursor:pointer;
}
select, button {
    font-family:inherit;
}
select {
    width:100%;
    padding:9px;
    color:#eaf7ff;
    background:rgba(4,17,28,.8);
    border:1px solid rgba(180,220,240,.25);
    border-radius:7px;
    outline:none;
}
button {
    border:1px solid rgba(135,220,250,.3);
    background:rgba(38,151,190,.19);
    color:#e8f8ff;
    border-radius:7px;
    padding:9px 11px;
    cursor:pointer;
    font-size:10px;
    letter-spacing:.4px;
}
button:hover {
    background:rgba(45,181,220,.34);
}
.primary {
    width:100%;
    margin-top:8px;
    background:rgba(30,160,190,.35);
}
.metricgrid {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:9px;
}
.metric {
    padding:12px;
    border-radius:9px;
    background:rgba(255,255,255,.055);
    border:1px solid rgba(255,255,255,.10);
}
.metric small {
    display:block;
    color:#9db9c9;
    font-size:9px;
    letter-spacing:.8px;
    text-transform:uppercase;
}
.metric strong {
    display:block;
    margin-top:7px;
    font-size:20px;
    font-weight:600;
}
.metric em {
    display:block;
    font-style:normal;
    color:#8faebe;
    font-size:9px;
    margin-top:4px;
}
.green { color:#62e8a7; }
.blue { color:#70d7f5; }
.orange { color:#ffc47b; }
.red { color:#ff7777; }
.sensorrow {
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:9px 0;
    border-bottom:1px solid rgba(255,255,255,.09);
    font-size:10px;
}
.sensorname {
    display:flex;align-items:center;gap:8px;
}
.sensordot {
    width:7px;height:7px;border-radius:50%;
    background:#4de6a0;
    box-shadow:0 0 9px #4de6a0;
}
.sensordot.extra {
    background:#ff6b64;
    box-shadow:0 0 9px #ff6b64;
}
#bottom {
    position:absolute;
    z-index:5;
    bottom:15px;
    left:18px;
    right:18px;
    min-height:95px;
    display:grid;
    grid-template-columns:1.2fr 1fr 1fr 1.3fr;
    gap:0;
    padding:13px 18px;
}
.bottomcell {
    padding:2px 17px;
    border-right:1px solid rgba(255,255,255,.13);
}
.bottomcell:last-child { border:0; }
.bottomlabel {
    color:#9dbdce;
    font-size:9px;
    letter-spacing:1.2px;
    text-transform:uppercase;
}
.bottomvalue {
    font-size:17px;
    margin-top:9px;
    font-weight:600;
}
.bottomsub {
    font-size:9px;color:#a4c0cf;margin-top:5px;
}
#alert {
    position:absolute;
    z-index:6;
    top:90px;
    left:50%;
    transform:translateX(-50%);
    padding:9px 17px;
    font-size:10px;
    letter-spacing:.7px;
    opacity:0;
    transition:opacity .3s;
    pointer-events:none;
    white-space:nowrap;
}
#hint {
    position:absolute;
    z-index:4;
    bottom:125px;
    left:50%;
    transform:translateX(-50%);
    color:white;
    text-shadow:0 2px 7px #183b50;
    font-size:10px;
    letter-spacing:1px;
    opacity:.8;
    pointer-events:none;
}
#loading {
    position:absolute;
    z-index:10;
    inset:0;
    display:flex;
    align-items:center;
    justify-content:center;
    flex-direction:column;
    background:linear-gradient(#9bc7df,#397e9e);
    color:white;
    transition:opacity .8s;
}
#loading strong { font-size:19px;letter-spacing:2px; }
#loading span { font-size:11px;margin-top:10px;opacity:.8; }
.loader {
    width:35px;height:35px;border:3px solid #ffffff55;
    border-top-color:white;border-radius:50%;
    animation:spin 1s linear infinite;margin-bottom:20px;
}
@keyframes spin { to { transform:rotate(360deg); } }

@media(max-width:850px) {
    #left { width:210px;left:8px;top:85px; }
    #right { width:220px;right:8px;top:85px; }
    #bottom { left:8px;right:8px;grid-template-columns:1fr 1fr; }
    #topbar {left:8px;right:8px;top:8px;}
    .topstatus {gap:8px;}
}
</style>

<script type="importmap">
{
 "imports": {
  "three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
  "three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
 }
}
</script>
</head>

<body>
<div id="scene"></div>

<div id="loading">
    <div class="loader"></div>
    <strong>INTELLIGENT BRIDGE MONITORING</strong>
    <span>Initializing 3D structural environment...</span>
</div>

<div id="topbar" class="glass">
    <div class="brand">
        <div class="logo">🌉</div>
        <div>
            <h1>INTELLIGENT BRIDGE MONITORING</h1>
            <small>STRUCTURAL HEALTH INTELLIGENCE SYSTEM</small>
        </div>
    </div>
    <div class="topstatus">
        <span><i class="statusdot"></i>SYSTEM ONLINE</span>
        <span id="modeLabel">CONTINUOUS MONITORING</span>
        <span id="clock">--:--:--</span>
    </div>
</div>

<div id="left" class="glass">
    <div class="paneltitle">Simulation controls</div>

    <div class="sectionlabel">Traffic simulation</div>

    <div class="control">
        <div class="controlhead">
            <span>Vehicle load</span><strong id="weightValue">18 tons</strong>
        </div>
        <input id="weight" type="range" min="2" max="45" value="18">
    </div>

    <div class="control">
        <div class="controlhead">
            <span>Vehicle speed</span><strong id="speedValue">55 km/h</strong>
        </div>
        <input id="speed" type="range" min="10" max="110" value="55">
    </div>

    <div class="control">
        <div class="controlhead">
            <span>Traffic intensity</span><strong id="trafficValue">45%</strong>
        </div>
        <input id="traffic" type="range" min="0" max="100" value="45">
    </div>

    <div class="section">
        <div class="sectionlabel">Structural simulation</div>

        <div class="control">
            <div class="controlhead">
                <span>Illustrative stiffness change</span>
                <strong id="stiffValue">0%</strong>
            </div>
            <input id="stiffness" type="range" min="0" max="30" value="0">
        </div>

        <div class="control">
            <div class="controlhead">
                <span>Trigger sensitivity</span>
                <strong id="triggerValue">65%</strong>
            </div>
            <input id="trigger" type="range" min="10" max="100" value="65">
        </div>

        <div class="control">
            <div class="controlhead"><span>Test location</span></div>
            <select id="location">
                <option value="center">Center span</option>
                <option value="north">North approach</option>
                <option value="south">South approach</option>
                <option value="tower">Main tower region</option>
            </select>
        </div>

        <button class="primary" id="eventButton">SIMULATE STRUCTURAL EVENT</button>
        <button class="primary" id="resetButton">RESET SIMULATION</button>
    </div>

    <div class="section">
        <div class="sectionlabel">Display</div>
        <button id="sensorButton">TOGGLE SENSOR VISIBILITY</button>
        <button id="cameraButton">RESET CAMERA</button>
    </div>
</div>

<div id="right" class="glass">
    <div class="paneltitle">Live structural telemetry</div>

    <div class="metricgrid">
        <div class="metric">
            <small>Deck strain</small>
            <strong class="blue" id="strain">112</strong>
            <em>με · illustrative</em>
        </div>
        <div class="metric">
            <small>Deck deflection</small>
            <strong class="blue" id="deflection">3.2</strong>
            <em>mm · illustrative</em>
        </div>
        <div class="metric">
            <small>Vibration</small>
            <strong class="blue" id="vibration">0.18</strong>
            <em>mm/s · illustrative</em>
        </div>
        <div class="metric">
            <small>Temperature</small>
            <strong class="blue" id="temperature">27.4</strong>
            <em>°C · simulated</em>
        </div>
    </div>

    <div class="section">
        <div class="paneltitle">Sensor network</div>
        <div class="sensorrow">
            <span class="sensorname"><i class="sensordot"></i>Primary strain sensors</span>
            <span class="green">ACTIVE</span>
        </div>
        <div class="sensorrow">
            <span class="sensorname"><i class="sensordot"></i>Accelerometers</span>
            <span class="green">ACTIVE</span>
        </div>
        <div class="sensorrow">
            <span class="sensorname"><i class="sensordot"></i>Displacement sensors</span>
            <span class="green">ACTIVE</span>
        </div>
        <div class="sensorrow">
            <span class="sensorname"><i class="sensordot extra"></i>Acoustic / extra sensors</span>
            <span id="extraStatus" class="orange">STANDBY</span>
        </div>
        <div class="sensorrow">
            <span class="sensorname"><i class="sensordot extra"></i>Thermal attention</span>
            <span id="thermalStatus" class="orange">STANDBY</span>
        </div>
    </div>

    <div class="section">
        <div class="paneltitle">Event analysis</div>
        <div class="sensorrow">
            <span>Monitoring mode</span><strong id="modeValue" class="green">NORMAL</strong>
        </div>
        <div class="sensorrow">
            <span>Change signal</span><strong id="changeValue">LOW</strong>
        </div>
        <div class="sensorrow">
            <span>Persistence check</span><strong id="persistence">WAITING</strong>
        </div>
        <div class="sensorrow">
            <span>System interpretation</span><strong id="interpretation" class="green">BASELINE</strong>
        </div>
    </div>
</div>

<div id="alert" class="glass"></div>

<div id="hint">DRAG TO ROTATE · SCROLL TO ZOOM · RIGHT-CLICK TO PAN</div>

<div id="bottom" class="glass">
    <div class="bottomcell">
        <div class="bottomlabel">Traffic flow</div>
        <div class="bottomvalue" id="trafficFlow">45%</div>
        <div class="bottomsub">Relative to simulated normal traffic</div>
    </div>
    <div class="bottomcell">
        <div class="bottomlabel">Vehicle activity</div>
        <div class="bottomvalue" id="vehicleCount">4</div>
        <div class="bottomsub">Vehicles in current simulation</div>
    </div>
    <div class="bottomcell">
        <div class="bottomlabel">Sensor attention</div>
        <div class="bottomvalue green" id="attention">STANDARD</div>
        <div class="bottomsub">Adaptive attention state</div>
    </div>
    <div class="bottomcell">
        <div class="bottomlabel">Data acquisition</div>
        <div class="bottomvalue" id="sampleCount">000001</div>
        <div class="bottomsub">Illustrative simulation samples</div>
    </div>
</div>

<script type="module">
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { Sky } from "three/addons/objects/Sky.js";
import { Water } from "three/addons/objects/Water.js";

const container = document.getElementById("scene");

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x91c5e5);
scene.fog = new THREE.FogExp2(0x9fc9df, 0.00065);

const camera = new THREE.PerspectiveCamera(
    48, window.innerWidth/window.innerHeight, 0.1, 3000
);
camera.position.set(180, 105, 235);

const renderer = new THREE.WebGLRenderer({
    antialias:true,
    alpha:false,
    powerPreference:"high-performance"
});
renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
renderer.setSize(window.innerWidth,window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
container.appendChild(renderer.domElement);

const controls = new OrbitControls(camera,renderer.domElement);
controls.target.set(0,30,0);
controls.enableDamping = true;
controls.dampingFactor = 0.045;
controls.minDistance = 70;
controls.maxDistance = 650;
controls.maxPolarAngle = Math.PI * 0.48;

scene.add(new THREE.HemisphereLight(0xd9efff,0x526b4c,1.8));

const sun = new THREE.DirectionalLight(0xfff2d9,3.2);
sun.position.set(-180,260,120);
sun.castShadow = true;
sun.shadow.mapSize.set(2048,2048);
sun.shadow.camera.left = -300;
sun.shadow.camera.right = 300;
sun.shadow.camera.top = 300;
sun.shadow.camera.bottom = -300;
scene.add(sun);

const sky = new Sky();
sky.scale.setScalar(10000);
scene.add(sky);
sky.material.uniforms.turbidity.value = 7;
sky.material.uniforms.rayleigh.value = 1.8;
sky.material.uniforms.mieCoefficient.value = 0.004;
sky.material.uniforms.mieDirectionalG.value = 0.82;

const sunVector = new THREE.Vector3();
sunVector.setFromSphericalCoords(
    1, THREE.MathUtils.degToRad(82),
    THREE.MathUtils.degToRad(210)
);
sky.material.uniforms.sunPosition.value.copy(sunVector);

const waterGeometry = new THREE.PlaneGeometry(4000,4000);
const water = new Water(waterGeometry,{
    textureWidth:1024,
    textureHeight:1024,
    waterNormals:new THREE.TextureLoader().load(
        "https://threejs.org/examples/textures/waternormals.jpg",
        t => {
            t.wrapS = t.wrapT = THREE.RepeatWrapping;
        }
    ),
    sunDirection:sunVector.clone().normalize(),
    sunColor:0xffffff,
    waterColor:0x276c88,
    distortionScale:3.0,
    fog:true
});
water.rotation.x = -Math.PI/2;
water.position.y = -3;
scene.add(water);

// Shoreline and terrain
const terrainMat = new THREE.MeshStandardMaterial({
    color:0x557d4b, roughness:1
});
const land = new THREE.Mesh(
    new THREE.PlaneGeometry(3000,3000),
    terrainMat
);
land.rotation.x = -Math.PI/2;
land.position.set(0,-8,-800);
scene.add(land);

function makeHill(x,z,sx,sy,sz,color) {
    const mesh = new THREE.Mesh(
        new THREE.SphereGeometry(1,48,32),
        new THREE.MeshStandardMaterial({
            color,roughness:1
        })
    );
    mesh.position.set(x,sy*0.18,z);
    mesh.scale.set(sx,sy,sz);
    mesh.receiveShadow = true;
    scene.add(mesh);
}
for(let i=0;i<15;i++){
    makeHill(
        -900+i*130,
        -700-Math.random()*280,
        90+Math.random()*90,
        40+Math.random()*70,
        80+Math.random()*100,
        i%2 ? 0x547b54 : 0x6c8e60
    );
}
for(let i=0;i<12;i++){
    makeHill(
        -850+i*150,
        650+Math.random()*180,
        100+Math.random()*100,
        45+Math.random()*65,
        80+Math.random()*100,
        0x64875b
    );
}

// Bridge group
const bridgeGroup = new THREE.Group();
scene.add(bridgeGroup);

const sensorGroup = new THREE.Group();
scene.add(sensorGroup);

const vehicleGroup = new THREE.Group();
scene.add(vehicleGroup);

const materials = {
    concrete:new THREE.MeshStandardMaterial({
        color:0xb9c1c6,roughness:.72,metalness:.08
    }),
    deck:new THREE.MeshStandardMaterial({
        color:0x59636a,roughness:.7,metalness:.2
    }),
    steel:new THREE.MeshStandardMaterial({
        color:0xdce3e6,roughness:.3,metalness:.72
    }),
    cable:new THREE.MeshStandardMaterial({
        color:0xf0f3f5,roughness:.3,metalness:.5
    }),
    road:new THREE.MeshStandardMaterial({
        color:0x303a40,roughness:.88
    }),
    white:new THREE.MeshStandardMaterial({
        color:0xe5e6d9,roughness:.6
    })
};

function beam(parent,a,b,radius,material,radial=8){
    const start = new THREE.Vector3(...a);
    const end = new THREE.Vector3(...b);
    const delta = new THREE.Vector3().subVectors(end,start);
    const mesh = new THREE.Mesh(
        new THREE.CylinderGeometry(radius,radius,delta.length(),radial),
        material
    );
    mesh.position.copy(start).add(end).multiplyScalar(.5);
    mesh.quaternion.setFromUnitVectors(
        new THREE.Vector3(0,1,0),delta.normalize()
    );
    mesh.castShadow = true;
    parent.add(mesh);
    return mesh;
}

function block(parent,x,y,z,sx,sy,sz,mat){
    const mesh = new THREE.Mesh(
        new THREE.BoxGeometry(sx,sy,sz),mat
    );
    mesh.position.set(x,y,z);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    parent.add(mesh);
    return mesh;
}

// Detailed fallback cable-stayed bridge
function buildFallbackBridge(){
    const g = bridgeGroup;
    const deckY = 27;
    const deckLength = 390;
    const deckWidth = 23;

    block(g,0,deckY,0,deckLength,3,deckWidth,materials.road);
    block(g,0,deckY-1.8,0,deckLength,1.2,deckWidth+2,materials.concrete);

    // Deck side girders
    for(const z of [-12,12]){
        block(g,0,deckY-2.7,z,deckLength,1.2,1.0,materials.steel);
        for(let x=-185;x<=185;x+=20){
            block(g,x,deckY-2.8,z,1.1,1.2,1.3,materials.steel);
        }
    }

    // Road markings
    for(let x=-180;x<190;x+=18){
        block(g,x,deckY+1.53,0,9,.06,.22,materials.white);
    }
    for(const z of [-8.8,8.8]){
        block(g,0,deckY+1.53,z,deckLength,.07,.22,materials.white);
    }

    // Railings
    for(const z of [-12,12]){
        for(let x=-190;x<=190;x+=8){
            block(g,x,deckY+3,z,.28,2.2,.28,materials.steel);
        }
        beam(g,[-195,deckY+4,z],[195,deckY+4,z],.23,materials.steel);
    }

    // Main pylons
    const towerXs = [-72,72];
    for(const x of towerXs){
        beam(g,[x,deckY-1,-1],[x,111,-1],2.7,materials.concrete,12);
        beam(g,[x-8,deckY-1,-1],[x,111,-1],2.1,materials.concrete,12);
        beam(g,[x+8,deckY-1,-1],[x,111,-1],2.1,materials.concrete,12);
        beam(g,[x,111,-1],[x,111,1],2.5,materials.concrete,12);

        // Cross beam and tower detailing
        beam(g,[x-8,65,-1],[x+8,65,-1],1.6,materials.concrete);
        beam(g,[x-6,85,-1],[x+6,85,-1],1.2,materials.concrete);

        // Cable fan on both sides of each tower
        for(let i=0;i<11;i++){
            const leftX = x-8-i*9;
            const rightX = x+8+i*9;
            const attachY = 103-i*4.5;
            beam(g,[x,attachY,0],[leftX,deckY+2,0],.13,materials.cable,6);
            beam(g,[x,attachY,0],[rightX,deckY+2,0],.13,materials.cable,6);
        }
    }

    // Approach supports
    for(const x of [-185,185]){
        block(g,x,12,0,5,25,27,materials.concrete);
    }
}

// Load actual GLB bridge asset
const MODEL_URL =
"https://raw.githubusercontent.com/experimentscience/bridge-monitoring-stem/main/assets/cable-stayed-bridge.glb";

let modelLoaded = false;

function fitBridgeModel(root){
    const box = new THREE.Box3().setFromObject(root);
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());

    if(!isFinite(size.x) || size.length()===0) {
        throw new Error("Bridge model has invalid dimensions");
    }

    root.position.sub(center);
    const refreshed = new THREE.Box3().setFromObject(root);
    root.position.y -= refreshed.min.y;

    const newBox = new THREE.Box3().setFromObject(root);
    const dims = newBox.getSize(new THREE.Vector3());

    // Normalize the model's longest horizontal dimension.
    const horizontal = Math.max(dims.x,dims.z);
    const scale = 390 / horizontal;
    root.scale.setScalar(scale);

    const finalBox = new THREE.Box3().setFromObject(root);
    const finalSize = finalBox.getSize(new THREE.Vector3());
    const finalCenter = finalBox.getCenter(new THREE.Vector3());

    root.position.x -= finalCenter.x;
    root.position.z -= finalCenter.z;
    root.position.y -= finalBox.min.y;

    // Bring the model above the water surface.
    root.position.y += 1;

    root.traverse(obj=>{
        if(obj.isMesh){
            obj.castShadow = true;
            obj.receiveShadow = true;
            if(obj.material){
                obj.material.needsUpdate = true;
            }
        }
    });
}

function loadBridge(){
    const loader = new GLTFLoader();
    loader.load(
        MODEL_URL,
        gltf=>{
            bridgeGroup.clear();
            const root = gltf.scene;
            fitBridgeModel(root);
            bridgeGroup.add(root);
            modelLoaded = true;
            console.log("Bridge GLB loaded successfully");
        },
        undefined,
        error=>{
            console.error("GLB could not be loaded:",error);
            buildFallbackBridge();
        }
    );
}
loadBridge();

// Sensor markers
const primarySensors = [];
const extraSensors = [];

function createSensor(x,y,z,extra=false){
    const color = extra ? 0xff514d : 0x36f2a0;
    const mat = new THREE.MeshStandardMaterial({
        color,
        emissive:color,
        emissiveIntensity:1.4,
        roughness:.25
    });
    const sphere = new THREE.Mesh(
        new THREE.SphereGeometry(extra?1.05:.8,16,16),
        mat
    );
    sphere.position.set(x,y,z);
    sensorGroup.add(sphere);

    const halo = new THREE.Mesh(
        new THREE.SphereGeometry(extra?2.2:1.7,16,16),
        new THREE.MeshBasicMaterial({
            color,
            transparent:true,
            opacity:.15,
            side:THREE.BackSide
        })
    );
    halo.position.copy(sphere.position);
    sensorGroup.add(halo);

    const sensor = {sphere,halo,extra};
    if(extra) extraSensors.push(sensor);
    else primarySensors.push(sensor);
}

for(let x=-165;x<=165;x+=33){
    createSensor(x,31,-8.5);
    createSensor(x,31,8.5);
}
for(const x of [-72,72]){
    createSensor(x,65,0,true);
    createSensor(x,90,0,true);
}
for(let x=-130;x<=130;x+=65){
    createSensor(x,31,0,true);
}

// Vehicles
const vehicleColors = [0xe9ecef,0x294c68,0xc5a26a,0x526c72,0xeeeeee];

function createVehicle(index){
    const group = new THREE.Group();
    const color = vehicleColors[index%vehicleColors.length];
    const bodyMat = new THREE.MeshStandardMaterial({
        color,roughness:.42,metalness:.25
    });
    const glassMat = new THREE.MeshStandardMaterial({
        color:0x253b4a,roughness:.2,metalness:.3
    });

    block(group,0,1.3,0,7.5,2.1,3.0,bodyMat);
    block(group,.6,2.7,0,3.4,1.2,2.7,glassMat);

    for(const x of [-2.4,2.4]){
        for(const z of [-1.55,1.55]){
            const wheel = new THREE.Mesh(
                new THREE.CylinderGeometry(.65,.65,.35,16),
                new THREE.MeshStandardMaterial({color:0x15191c})
            );
            wheel.rotation.x = Math.PI/2;
            wheel.position.set(x,.65,z);
            group.add(wheel);
        }
    }
    group.position.y = 29;
    vehicleGroup.add(group);
    return group;
}

const vehicles = [];
for(let i=0;i<7;i++){
    vehicles.push({
        mesh:createVehicle(i),
        progress:(i/7),
        lane:i%2===0?-4.5:4.5,
        speed:.00012+Math.random()*.00008
    });
}

// Simulation state
let eventActive = false;
let eventTime = 0;
let samples = 0;
let sensorVisible = true;
let eventPersistence = 0;
let lastEventSignal = 0;

const $ = id=>document.getElementById(id);
const weight = $("weight");
const speed = $("speed");
const traffic = $("traffic");
const stiffness = $("stiffness");
const trigger = $("trigger");

function updateLabels(){
    $("weightValue").textContent = weight.value+" tons";
    $("speedValue").textContent = speed.value+" km/h";
    $("trafficValue").textContent = traffic.value+"%";
    $("stiffValue").textContent = stiffness.value+"%";
    $("triggerValue").textContent = trigger.value+"%";
}
[weight,speed,traffic,stiffness,trigger].forEach(el=>{
    el.addEventListener("input",updateLabels);
});
updateLabels();

function showAlert(message){
    const a=$("alert");
    a.textContent=message;
    a.style.opacity=1;
    clearTimeout(showAlert.timer);
    showAlert.timer=setTimeout(()=>a.style.opacity=0,3500);
}

$("eventButton").onclick=()=>{
    eventActive=true;
    eventTime=0;
    eventPersistence=0;
    showAlert("EVENT SIMULATION ACTIVATED · ADAPTIVE ATTENTION ENABLED");
};

$("resetButton").onclick=()=>{
    eventActive=false;
    eventTime=0;
    eventPersistence=0;
    stiffness.value=0;
    traffic.value=45;
    weight.value=18;
    speed.value=55;
    updateLabels();
    showAlert("SIMULATION RESET · RETURNING TO BASELINE");
};

$("sensorButton").onclick=()=>{
    sensorVisible=!sensorVisible;
    sensorGroup.visible=sensorVisible;
};

$("cameraButton").onclick=()=>{
    camera.position.set(180,105,235);
    controls.target.set(0,30,0);
    controls.update();
};

function updateTelemetry(time){
    const trafficVal=Number(traffic.value);
    const weightVal=Number(weight.value);
    const stiffnessVal=Number(stiffness.value);
    const sensitivity=Number(trigger.value);

    const trafficFactor=trafficVal/100;
    const loadFactor=weightVal/18;
    const naturalWave=Math.sin(time*1.3)*.035;
    const vehicleResponse=trafficFactor*loadFactor*.18;
    const structuralResponse=stiffnessVal/100*.75;

    const strain=105+vehicleResponse*100+structuralResponse*90+
                 naturalWave*100;
    const deflection=2.7+vehicleResponse*2.3+
                     structuralResponse*3.2+Math.abs(naturalWave)*2;
    const vibration=.13+vehicleResponse*.45+
                    structuralResponse*.3+Math.abs(naturalWave)*.1;
    const temperature=27.4+Math.sin(time*.08)*1.2;

    const signal=vehicleResponse*100+structuralResponse*100;
    const threshold=20+(sensitivity/100)*45;
    const triggered=signal>threshold;

    if(triggered){
        eventPersistence++;
    } else {
        eventPersistence=Math.max(0,eventPersistence-1);
    }

    const adaptive=eventActive || eventPersistence>12;

    $("strain").textContent=strain.toFixed(0);
    $("deflection").textContent=deflection.toFixed(2);
    $("vibration").textContent=vibration.toFixed(2);
    $("temperature").textContent=temperature.toFixed(1);

    $("trafficFlow").textContent=trafficVal+"%";
    $("vehicleCount").textContent=
        Math.max(0,Math.round(trafficVal/15));
    $("sampleCount").textContent=String(samples).padStart(6,"0");

    $("extraStatus").textContent=adaptive?"ACTIVE":"STANDBY";
    $("thermalStatus").textContent=adaptive?"ACTIVE":"STANDBY";
    $("attention").textContent=adaptive?"ADAPTIVE":"STANDARD";
    $("attention").className="bottomvalue "+(adaptive?"red":"green");

    $("modeValue").textContent=adaptive?"SPECIAL ATTENTION":"NORMAL";
    $("modeValue").className=adaptive?"red":"green";
    $("modeLabel").textContent=adaptive?
        "ADAPTIVE ATTENTION":"CONTINUOUS MONITORING";

    $("changeValue").textContent=triggered?"ELEVATED":"LOW";
    $("changeValue").className=triggered?"orange":"green";

    $("persistence").textContent=eventPersistence>35?
        "PERSISTENT SIGNAL":"UNDER OBSERVATION";

    if(stiffnessVal>0 && eventPersistence>35){
        $("interpretation").textContent="PERSISTENT CHANGE";
        $("interpretation").className="orange";
    } else if(triggered){
        $("interpretation").textContent="REQUIRES REVIEW";
        $("interpretation").className="orange";
    } else {
        $("interpretation").textContent="BASELINE";
        $("interpretation").className="green";
    }

    if(eventActive){
        eventTime+=.016;
        if(eventTime>12){
            eventActive=false;
            showAlert("EVENT WINDOW COMPLETE · CONTINUE OBSERVING THE SIGNAL");
        }
    }

    lastEventSignal=signal;
}

// Clock
function updateClock(){
    $("clock").textContent=new Date().toLocaleTimeString();
}
setInterval(updateClock,1000);
updateClock();

// Animation
const clock = new THREE.Clock();
let elapsed=0;

function animate(){
    requestAnimationFrame(animate);
    const delta=Math.min(clock.getDelta(),.05);
    elapsed+=delta;
    samples++;

    water.material.uniforms.time.value += delta*.45;

    for(const v of vehicles){
        const trafficFactor=Number(traffic.value)/45;
        v.progress += v.speed*delta*60*trafficFactor;
        if(v.progress>1.08) v.progress=-.08;

        const x=-195+v.progress*390;
        v.mesh.position.set(x,29,v.lane);
    }

    // Sensor pulse effect
    for(const s of [...primarySensors,...extraSensors]){
        const pulse=1+Math.sin(elapsed*3+s.sphere.position.x*.05)*.12;
        s.sphere.scale.setScalar(pulse);
        s.halo.scale.setScalar(1+Math.sin(elapsed*2)*.12);
    }

    // Visual bridge response in the educational simulation
    const response=Number(stiffness.value)/100;
    bridgeGroup.position.y=Math.sin(elapsed*2)*response*.12;

    updateTelemetry(elapsed);
    controls.update();
    renderer.render(scene,camera);
}
animate();

window.addEventListener("resize",()=>{
    camera.aspect=window.innerWidth/window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth,window.innerHeight);
});

setTimeout(()=>{
    const loading=$("loading");
    loading.style.opacity=0;
    setTimeout(()=>loading.remove(),900);
},2500);

</script>
</body>
</html>
"""

components.html(html, height=1100, scrolling=False)
