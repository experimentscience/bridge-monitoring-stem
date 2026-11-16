
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
[data-testid="stVerticalBlock"] {
    margin: 0 !important;
    padding: 0 !important;
    background: #07131d !important;
}
[data-testid="stHeader"], [data-testid="stToolbar"],
[data-testid="stSidebar"], footer {
    display: none !important;
}
iframe { border: 0 !important; }
</style>
""", unsafe_allow_html=True)

HTML = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
* { box-sizing:border-box; }
html,body,#scene {
    margin:0;width:100%;height:100%;
    overflow:hidden;font-family:Arial,sans-serif;
}
body { background:#8bbbd3;color:white; }
#scene { position:fixed;inset:0;z-index:0; }
canvas { display:block; }

.glass {
    background:linear-gradient(135deg,
        rgba(10,27,42,.82),rgba(13,43,60,.58));
    border:1px solid rgba(210,240,255,.24);
    border-radius:13px;
    backdrop-filter:blur(18px);
    -webkit-backdrop-filter:blur(18px);
    box-shadow:0 12px 35px #06152255,
        inset 0 1px 0 #ffffff20;
}
#header {
    position:absolute;z-index:5;top:15px;left:18px;right:18px;
    height:65px;padding:0 20px;
    display:flex;align-items:center;justify-content:space-between;
}
.brand { display:flex;align-items:center;gap:13px; }
.logo {
    width:39px;height:39px;border-radius:10px;
    display:grid;place-items:center;font-size:21px;
    background:#42bce533;border:1px solid #7adcf077;
}
h1 { font-size:15px;letter-spacing:1.3px;margin:0; }
.sub { font-size:9px;color:#a8cbdc;letter-spacing:1.7px;margin-top:5px; }
.status { font-size:10px;color:#d7eaf4;letter-spacing:1px; }
.dot {
    display:inline-block;width:7px;height:7px;
    background:#4de7a1;border-radius:50%;
    box-shadow:0 0 10px #4de7a1;margin-right:7px;
}
.panel {
    position:absolute;z-index:5;top:96px;
    padding:17px;width:258px;
}
#left { left:18px; }
#right { right:18px;width:280px; }
.heading {
    font-size:10px;letter-spacing:1.5px;
    color:#a9d8eb;font-weight:bold;margin-bottom:15px;
}
.label {
    font-size:9px;letter-spacing:1.1px;
    color:#8fb7ca;text-transform:uppercase;margin:13px 0 9px;
}
.control { margin:12px 0; }
.controlhead {
    display:flex;justify-content:space-between;
    font-size:10px;margin-bottom:6px;color:#d7e8f1;
}
.controlhead strong { color:white; }
input[type=range] { width:100%;accent-color:#42c8e8; }
select,button {
    width:100%;padding:9px;border-radius:7px;
    color:white;background:#102d40;
    border:1px solid #b5d9e344;font-size:10px;
}
button { cursor:pointer;margin-top:7px; }
button:hover { background:#1c536b; }
.separator {
    border-top:1px solid #ffffff20;
    margin-top:14px;padding-top:10px;
}
.grid {
    display:grid;grid-template-columns:1fr 1fr;gap:8px;
}
.metric {
    background:#ffffff0b;border:1px solid #ffffff15;
    border-radius:8px;padding:11px;
}
.metric small {
    display:block;font-size:8px;letter-spacing:1px;
    color:#9db9c9;text-transform:uppercase;
}
.metric strong { display:block;font-size:20px;margin-top:7px; }
.metric em { display:block;font-size:8px;color:#8daebe;margin-top:3px;font-style:normal; }
.blue { color:#75dcf7; }
.green { color:#65e8a7; }
.orange { color:#ffc17c; }
.red { color:#ff7777; }
.sensor {
    display:flex;justify-content:space-between;
    padding:9px 0;border-bottom:1px solid #ffffff12;
    font-size:9px;
}
.sensor i {
    display:inline-block;width:7px;height:7px;
    background:#4be7a0;border-radius:50%;margin-right:7px;
    box-shadow:0 0 8px #4be7a0;
}
.sensor i.extra { background:#ff655f;box-shadow:0 0 8px #ff655f; }
#bottom {
    position:absolute;z-index:5;left:18px;right:18px;bottom:15px;
    min-height:83px;padding:13px 18px;
    display:grid;grid-template-columns:repeat(4,1fr);
}
.bottomcell { padding:2px 15px;border-right:1px solid #ffffff20; }
.bottomcell:last-child { border:0; }
.bottomlabel { color:#9dbbcb;font-size:8px;letter-spacing:1.2px; }
.bottomvalue { font-size:17px;font-weight:bold;margin-top:8px; }
.bottomsub { color:#9db5c2;font-size:8px;margin-top:4px; }
#loading {
    position:absolute;inset:0;z-index:20;
    display:flex;align-items:center;justify-content:center;
    flex-direction:column;background:#739fb9;color:white;
    font-size:12px;letter-spacing:1.5px;
}
#loading strong { font-size:17px;margin-bottom:12px; }
#error {
    display:none;margin-top:16px;max-width:500px;
    padding:12px;background:#481f28;border-radius:8px;
    color:#ffd9d9;font-size:11px;letter-spacing:0;
}
#alert {
    position:absolute;z-index:7;top:90px;left:50%;
    transform:translateX(-50%);padding:10px 18px;
    font-size:10px;opacity:0;transition:opacity .3s;
    white-space:nowrap;
}
@media(max-width:850px) {
    .panel { width:205px;top:85px;padding:11px; }
    #right { width:220px; }
    #left { left:7px; }
    #right { right:7px; }
    #bottom { left:7px;right:7px; }
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
    <strong>INTELLIGENT BRIDGE MONITORING</strong>
    Loading bridge model and environment...
    <div id="error"></div>
</div>

<div id="header" class="glass">
    <div class="brand">
        <div class="logo">🌉</div>
        <div>
            <h1>INTELLIGENT BRIDGE MONITORING</h1>
            <div class="sub">STRUCTURAL HEALTH INTELLIGENCE SYSTEM</div>
        </div>
    </div>
    <div class="status">
        <span class="dot"></span>SYSTEM ONLINE
        &nbsp;&nbsp; | &nbsp;&nbsp;
        <span id="modeTop">CONTINUOUS MONITORING</span>
        &nbsp;&nbsp; | &nbsp;&nbsp;
        <span id="clock">--:--:--</span>
    </div>
</div>

<div id="left" class="panel glass">
    <div class="heading">SIMULATION CONTROLS</div>
    <div class="label">Traffic simulation</div>

    <div class="control">
        <div class="controlhead"><span>Vehicle load</span><strong id="weightText">18 tons</strong></div>
        <input id="weight" type="range" min="2" max="45" value="18">
    </div>
    <div class="control">
        <div class="controlhead"><span>Vehicle speed</span><strong id="speedText">55 km/h</strong></div>
        <input id="speed" type="range" min="10" max="110" value="55">
    </div>
    <div class="control">
        <div class="controlhead"><span>Traffic intensity</span><strong id="trafficText">45%</strong></div>
        <input id="traffic" type="range" min="0" max="100" value="45">
    </div>

    <div class="separator">
        <div class="label">Structural simulation</div>
        <div class="control">
            <div class="controlhead"><span>Stiffness change</span><strong id="stiffText">0%</strong></div>
            <input id="stiffness" type="range" min="0" max="30" value="0">
        </div>
        <div class="control">
            <div class="controlhead"><span>Trigger sensitivity</span><strong id="triggerText">65%</strong></div>
            <input id="trigger" type="range" min="10" max="100" value="65">
        </div>
        <div class="label">Test location</div>
        <select id="location">
            <option>Center span</option>
            <option>North approach</option>
            <option>South approach</option>
            <option>Main tower</option>
        </select>
        <button id="event">SIMULATE STRUCTURAL EVENT</button>
        <button id="reset">RESET SIMULATION</button>
    </div>
    <div class="separator">
        <button id="sensors">TOGGLE SENSOR MARKERS</button>
        <button id="camera">RESET CAMERA</button>
    </div>
</div>

<div id="right" class="panel glass">
    <div class="heading">LIVE STRUCTURAL TELEMETRY</div>
    <div class="grid">
        <div class="metric"><small>Deck strain</small><strong class="blue" id="strain">112</strong><em>με · simulated</em></div>
        <div class="metric"><small>Deflection</small><strong class="blue" id="deflection">3.2</strong><em>mm · simulated</em></div>
        <div class="metric"><small>Vibration</small><strong class="blue" id="vibration">0.18</strong><em>mm/s · simulated</em></div>
        <div class="metric"><small>Temperature</small><strong class="blue" id="temperature">27.4</strong><em>°C · simulated</em></div>
    </div>
    <div class="separator">
        <div class="heading">SENSOR NETWORK</div>
        <div class="sensor"><span><i></i>Primary strain sensors</span><b class="green">ACTIVE</b></div>
        <div class="sensor"><span><i></i>Accelerometers</span><b class="green">ACTIVE</b></div>
        <div class="sensor"><span><i></i>Displacement sensors</span><b class="green">ACTIVE</b></div>
        <div class="sensor"><span><i class="extra"></i>Acoustic sensors</span><b id="extra" class="orange">STANDBY</b></div>
        <div class="sensor"><span><i class="extra"></i>Thermal attention</span><b id="thermal" class="orange">STANDBY</b></div>
    </div>
    <div class="separator">
        <div class="heading">EVENT ANALYSIS</div>
        <div class="sensor"><span>Monitoring mode</span><b id="mode" class="green">NORMAL</b></div>
        <div class="sensor"><span>Change signal</span><b id="signal">LOW</b></div>
        <div class="sensor"><span>Persistence check</span><b id="persist">WAITING</b></div>
        <div class="sensor"><span>Interpretation</span><b id="interpret" class="green">BASELINE</b></div>
    </div>
</div>

<div id="alert" class="glass"></div>

<div id="bottom" class="glass">
    <div class="bottomcell">
        <div class="bottomlabel">TRAFFIC FLOW</div>
        <div class="bottomvalue" id="flow">45%</div>
        <div class="bottomsub">Relative to simulated normal traffic</div>
    </div>
    <div class="bottomcell">
        <div class="bottomlabel">VEHICLE ACTIVITY</div>
        <div class="bottomvalue" id="vehicleCount">4</div>
        <div class="bottomsub">Vehicles in simulation</div>
    </div>
    <div class="bottomcell">
        <div class="bottomlabel">SENSOR ATTENTION</div>
        <div class="bottomvalue green" id="attention">STANDARD</div>
        <div class="bottomsub">Adaptive attention state</div>
    </div>
    <div class="bottomcell">
        <div class="bottomlabel">DATA ACQUISITION</div>
        <div class="bottomvalue" id="samples">000001</div>
        <div class="bottomsub">Illustrative simulation samples</div>
    </div>
</div>

<script type="module">
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { RGBELoader } from "three/addons/loaders/RGBELoader.js";
import { Water } from "three/addons/objects/Water.js";

const $ = id => document.getElementById(id);
const sceneRoot = $("scene");

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x9fc6dc);
scene.fog = new THREE.FogExp2(0x9fc6dc,0.00035);

const camera = new THREE.PerspectiveCamera(
    43,innerWidth/innerHeight,0.1,5000
);
camera.position.set(170,90,220);

const renderer = new THREE.WebGLRenderer({
    antialias:true,
    powerPreference:"high-performance"
});
renderer.setSize(innerWidth,innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
sceneRoot.appendChild(renderer.domElement);

const controls = new OrbitControls(camera,renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = .045;
controls.target.set(0,28,0);
controls.minDistance = 55;
controls.maxDistance = 700;
controls.maxPolarAngle = Math.PI*.49;

scene.add(new THREE.HemisphereLight(0xd8edff,0x526b51,1.35));

const sun = new THREE.DirectionalLight(0xfff0d8,3.0);
sun.position.set(-180,250,130);
sun.castShadow = true;
sun.shadow.mapSize.set(2048,2048);
sun.shadow.camera.left = -300;
sun.shadow.camera.right = 300;
sun.shadow.camera.top = 300;
sun.shadow.camera.bottom = -300;
scene.add(sun);

const pmrem = new THREE.PMREMGenerator(renderer);
pmrem.compileEquirectangularShader();

const hdriURL =
"https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/1k/kloofendal_48d_partly_cloudy_puresky_1k.hdr";

new RGBELoader().load(
    hdriURL,
    texture => {
        texture.mapping = THREE.EquirectangularReflectionMapping;
        scene.background = texture;
        scene.environment = pmrem.fromEquirectangular(texture).texture;
        texture.dispose();
        pmrem.dispose();
    },
    undefined,
    error => console.warn("HDR environment unavailable; using scene lighting.",error)
);

// Water with animated normal maps and reflections
const water = new Water(
    new THREE.PlaneGeometry(5000,5000),
    {
        textureWidth:1024,
        textureHeight:1024,
        waterNormals:new THREE.TextureLoader().load(
            "https://threejs.org/examples/textures/waternormals.jpg",
            t => { t.wrapS=t.wrapT=THREE.RepeatWrapping; }
        ),
        sunDirection:new THREE.Vector3(-1,1,1).normalize(),
        sunColor:0xffffff,
        waterColor:0x285f78,
        distortionScale:2.5,
        fog:true
    }
);
water.rotation.x=-Math.PI/2;
water.position.y=-4;
scene.add(water);

// Distant shoreline
const terrainMaterial = new THREE.MeshStandardMaterial({
    color:0x66865b,roughness:1
});

function hill(x,y,z,sx,sy,sz,color){
    const mesh=new THREE.Mesh(
        new THREE.SphereGeometry(1,40,28),
        new THREE.MeshStandardMaterial({color,roughness:1})
    );
    mesh.position.set(x,y,z);
    mesh.scale.set(sx,sy,sz);
    mesh.receiveShadow=true;
    scene.add(mesh);
}
for(let i=0;i<16;i++){
    hill(-1000+i*135,12,-850-Math.random()*120,
        110,55+Math.random()*30,100,
        i%2?0x597b50:0x718c5c);
}
for(let i=0;i<14;i++){
    hill(-900+i*145,12,850+Math.random()*100,
        120,55+Math.random()*35,100,
        i%2?0x587950:0x718c5c);
}

// Bridge model
const bridgeGroup = new THREE.Group();
scene.add(bridgeGroup);

const bridgeURL =
"https://raw.githubusercontent.com/experimentscience/bridge-monitoring-stem/main/assets/cable-stayed-bridge.glb";

let bridgeReady=false;
let bridgeLength=380;
let bridgeWidth=64;
let deckHeight=10;

function prepareModel(root){
    // Turn the bridge so its longest horizontal axis runs left-to-right.
    let box=new THREE.Box3().setFromObject(root);
    let size=box.getSize(new THREE.Vector3());

    if(size.z>size.x){
        root.rotation.y=Math.PI/2;
    }

    box=new THREE.Box3().setFromObject(root);
    let center=box.getCenter(new THREE.Vector3());
    root.position.sub(center);

    box=new THREE.Box3().setFromObject(root);
    size=box.getSize(new THREE.Vector3());

    const longest=Math.max(size.x,size.z);
    const scale=380/longest;
    root.scale.setScalar(scale);

    box=new THREE.Box3().setFromObject(root);
    center=box.getCenter(new THREE.Vector3());
    root.position.x-=center.x;
    root.position.z-=center.z;
    root.position.y-=box.min.y;

    root.traverse(obj=>{
        if(!obj.isMesh)return;
        obj.castShadow=true;
        obj.receiveShadow=true;
        if(obj.material){
            obj.material.needsUpdate=true;
        }
    });

    bridgeLength=380;
    bridgeWidth=Math.min(64,size.z*scale);
    deckHeight=10;
}

function showError(message){
    $("error").style.display="block";
    $("error").textContent=message;
    $("loading").style.background="#492b35";
}

new GLTFLoader().load(
    bridgeURL,
    gltf=>{
        const model=gltf.scene;
        prepareModel(model);
        bridgeGroup.add(model);
        bridgeReady=true;
        $("loading").style.display="none";
        console.log("Actual bridge model loaded.");
    },
    progress=>{
        if(progress.total){
            console.log("Model loading:",
                Math.round(progress.loaded/progress.total*100)+"%");
        }
    },
    error=>{
        console.error(error);
        showError(
            "The bridge model could not be loaded. Check that the GLB exists in the GitHub main/assets folder and that the repository is public."
        );
    }
);

// Sensor marker system
const sensorGroup=new THREE.Group();
scene.add(sensorGroup);

const primarySensors=[];
const extraSensors=[];

function addSensor(x,y,z,extra=false){
    const color=extra?0xff514d:0x43f0a1;
    const material=new THREE.MeshStandardMaterial({
        color,emissive:color,emissiveIntensity:1.5
    });
    const marker=new THREE.Mesh(
        new THREE.SphereGeometry(.85,18,18),material
    );
    marker.position.set(x,y,z);
    sensorGroup.add(marker);

    const halo=new THREE.Mesh(
        new THREE.SphereGeometry(1.8,18,18),
        new THREE.MeshBasicMaterial({
            color,transparent:true,opacity:.17,
            side:THREE.BackSide
        })
    );
    halo.position.copy(marker.position);
    sensorGroup.add(halo);

    (extra?extraSensors:primarySensors).push({marker,halo});
}

// Initial marker positions are illustrative; refine after checking
// the model's deck alignment in the actual app.
for(let x=-165;x<=165;x+=33){
    addSensor(x,deckHeight+1,-9);
    addSensor(x,deckHeight+1,9);
}
for(const x of [-72,72]){
    addSensor(x,deckHeight+30,0,true);
    addSensor(x,deckHeight+55,0,true);
}

// Traffic vehicles
const vehicleGroup=new THREE.Group();
scene.add(vehicleGroup);
const vehicles=[];
const carColors=[0xe6e9eb,0x263e51,0xb2a27f,0x63747c,0xeeeeea];

function createCar(i){
    const g=new THREE.Group();
    const paint=new THREE.MeshStandardMaterial({
        color:carColors[i%carColors.length],
        metalness:.55,roughness:.28
    });
    const glass=new THREE.MeshPhysicalMaterial({
        color:0x182c3a,metalness:.25,
        roughness:.12,clearcoat:1
    });
    function part(w,h,d,y,mat,x=0){
        const m=new THREE.Mesh(
            new THREE.BoxGeometry(w,h,d),mat
        );
        m.position.set(x,y,0);
        m.castShadow=true;
        g.add(m);
    }
    part(7,1.7,3.1,1.2,paint);
    part(3.6,1.25,2.65,2.55,glass,.2);

    const wheelMat=new THREE.MeshStandardMaterial({
        color:0x171b20,roughness:.9
    });
    for(const x of [-2.2,2.2]){
        for(const z of [-1.6,1.6]){
            const wheel=new THREE.Mesh(
                new THREE.CylinderGeometry(.58,.58,.35,20),
                wheelMat
            );
            wheel.rotation.x=Math.PI/2;
            wheel.position.set(x,.58,z);
            g.add(wheel);
        }
    }
    vehicleGroup.add(g);
    return g;
}

for(let i=0;i<7;i++){
    vehicles.push({
        mesh:createCar(i),
        progress:i/7,
        lane:i%2===0?-5:5,
        speed:.00015+Math.random()*.00005
    });
}

// Controls and simulation
const weight=$("weight");
const speed=$("speed");
const traffic=$("traffic");
const stiffness=$("stiffness");
const trigger=$("trigger");

function labels(){
    $("weightText").textContent=weight.value+" tons";
    $("speedText").textContent=speed.value+" km/h";
    $("trafficText").textContent=traffic.value+"%";
    $("stiffText").textContent=stiffness.value+"%";
    $("triggerText").textContent=trigger.value+"%";
}
[weight,speed,traffic,stiffness,trigger].forEach(
    el=>el.addEventListener("input",labels)
);
labels();

let eventActive=false;
let elapsed=0;
let sample=0;
let persistence=0;
let sensorsVisible=true;

function alertMessage(message){
    const a=$("alert");
    a.textContent=message;
    a.style.opacity=1;
    clearTimeout(alertMessage.timer);
    alertMessage.timer=setTimeout(()=>a.style.opacity=0,3200);
}

$("event").onclick=()=>{
    eventActive=true;
    persistence=0;
    alertMessage("EVENT SIMULATION ACTIVATED · ADAPTIVE ATTENTION");
};
$("reset").onclick=()=>{
    eventActive=false;
    persistence=0;
    weight.value=18;
    speed.value=55;
    traffic.value=45;
    stiffness.value=0;
    trigger.value=65;
    labels();
    alertMessage("SIMULATION RESET · BASELINE RESTORED");
};
$("sensors").onclick=()=>{
    sensorsVisible=!sensorsVisible;
    sensorGroup.visible=sensorsVisible;
};
$("camera").onclick=()=>{
    camera.position.set(170,90,220);
    controls.target.set(0,28,0);
    controls.update();
};

function telemetry(t){
    const w=Number(weight.value);
    const tr=Number(traffic.value)/100;
    const st=Number(stiffness.value)/100;
    const sensitivity=Number(trigger.value);

    const trafficResponse=tr*(w/18)*.18;
    const structuralResponse=st*.75;
    const wave=Math.sin(t*1.3)*.035;

    const strain=105+trafficResponse*100+
        structuralResponse*90+wave*100;
    const deflection=2.7+trafficResponse*2.3+
        structuralResponse*3.2+Math.abs(wave)*2;
    const vibration=.13+trafficResponse*.45+
        structuralResponse*.3+Math.abs(wave)*.1;
    const temperature=27.4+Math.sin(t*.08)*1.2;

    const signal=trafficResponse*100+structuralResponse*100;
    const threshold=20+sensitivity*.45;
    const detected=signal>threshold;

    persistence=detected?Math.min(persistence+1,100):
        Math.max(0,persistence-1);

    const adaptive=eventActive||persistence>12;

    $("strain").textContent=strain.toFixed(0);
    $("deflection").textContent=deflection.toFixed(2);
    $("vibration").textContent=vibration.toFixed(2);
    $("temperature").textContent=temperature.toFixed(1);

    $("flow").textContent=traffic.value+"%";
    $("vehicleCount").textContent=Math.round(tr*8);
    $("samples").textContent=String(sample).padStart(6,"0");

    $("extra").textContent=adaptive?"ACTIVE":"STANDBY";
    $("thermal").textContent=adaptive?"ACTIVE":"STANDBY";
    $("attention").textContent=adaptive?"ADAPTIVE":"STANDARD";
    $("attention").className="bottomvalue "+(adaptive?"red":"green");

    $("mode").textContent=adaptive?"SPECIAL ATTENTION":"NORMAL";
    $("mode").className=adaptive?"red":"green";
    $("modeTop").textContent=adaptive?
        "ADAPTIVE ATTENTION":"CONTINUOUS MONITORING";

    $("signal").textContent=detected?"ELEVATED":"LOW";
    $("signal").className=detected?"orange":"green";
    $("persist").textContent=persistence>35?
        "PERSISTENT SIGNAL":"UNDER OBSERVATION";

    $("interpret").textContent=
        st>0&&persistence>35?"PERSISTENT CHANGE":
        detected?"REQUIRES REVIEW":"BASELINE";
    $("interpret").className=
        st>0&&persistence>35?"orange":
        detected?"orange":"green";
}

function animate(){
    requestAnimationFrame(animate);
    const delta=Math.min(clock.getDelta(),.05);
    elapsed+=delta;
    sample++;

    if(water.material.uniforms.time){
        water.material.uniforms.time.value+=delta*.4;
    }

    const trafficFactor=Number(traffic.value)/45;
    vehicles.forEach(v=>{
        v.progress+=v.speed*delta*60*trafficFactor;
        if(v.progress>1.08)v.progress=-.08;
        v.mesh.position.set(
            -190+v.progress*380,
            deckHeight+2.8,
            v.lane
        );
    });

    [...primarySensors,...extraSensors].forEach(s=>{
        const pulse=1+Math.sin(elapsed*3+s.marker.position.x*.04)*.1;
        s.marker.scale.setScalar(pulse);
        s.halo.scale.setScalar(1+Math.sin(elapsed*2)*.1);
    });

    // Small illustrative movement, not a structural physics model.
    bridgeGroup.position.y=
        Math.sin(elapsed*2)*Number(stiffness.value)/100*.1;

    telemetry(elapsed);
    $("clock").textContent=new Date().toLocaleTimeString();

    controls.update();
    renderer.render(scene,camera);
}

const clock=new THREE.Clock();
animate();

window.addEventListener("resize",()=>{
    camera.aspect=innerWidth/innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth,innerHeight);
});
</script>
</body>
</html>
"""

components.html(HTML, height=1050, scrolling=False)
