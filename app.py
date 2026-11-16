
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
#MainMenu,footer,header,[data-testid="stToolbar"],
[data-testid="stDecoration"],[data-testid="stStatusWidget"] {
    display:none!important;
}
.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"],
.main,.block-container {
    padding:0!important;
    margin:0!important;
    max-width:100%!important;
    background:#9acde9!important;
}
iframe {border:0!important;}
</style>
""", unsafe_allow_html=True)

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">

<script type="importmap">
{
 "imports":{
  "three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
  "three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
 }
}
</script>

<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;
font-family:Inter,Arial,sans-serif;background:#9acde9;color:#effaff}
#world{position:fixed;inset:0}
#world canvas{width:100%;height:100%;display:block}

.glass{
 position:absolute;z-index:4;color:#edfaff;
 background:linear-gradient(145deg,rgba(7,28,45,.82),rgba(9,42,62,.68));
 border:1px solid rgba(150,220,255,.38);
 border-radius:13px;
 box-shadow:0 12px 35px rgba(0,25,45,.24),inset 0 1px rgba(255,255,255,.09);
 backdrop-filter:blur(17px);-webkit-backdrop-filter:blur(17px);
 padding:13px
}
#header{top:13px;left:15px;right:15px;height:66px;
display:flex;align-items:center;justify-content:space-between;padding:10px 19px}
.logo{font-size:17px;font-weight:850;letter-spacing:1px}
.kicker{font-size:9px;color:#a5d8ec;letter-spacing:2px;margin-top:4px}
.headright{display:flex;gap:8px;align-items:center}
.tag{padding:8px 11px;border-radius:20px;background:rgba(30,83,108,.55);
border:1px solid rgba(151,221,249,.3);font-size:9px;white-space:nowrap}
.green{color:#5df0b2}
#left{left:15px;top:94px;width:248px;max-height:calc(100vh - 245px);overflow:auto}
#right{right:15px;top:94px;width:270px;max-height:calc(100vh - 245px);overflow:auto}
.heading{font-size:10px;letter-spacing:1.6px;color:#9cdef6;font-weight:800;margin-bottom:12px}
.subheading{font-size:9px;letter-spacing:1.2px;color:#85c9e6;
margin:13px 0 8px;padding-top:10px;border-top:1px solid #ffffff22}
label{display:flex;justify-content:space-between;gap:5px;
font-size:10px;color:#c4deeb;margin:9px 0 5px}
output{color:white;font-weight:700}
input[type=range]{width:100%;accent-color:#42d8ee;height:13px}
select{width:100%;padding:8px;background:#12354a;color:white;
border:1px solid #4c829d;border-radius:7px;font-size:10px}
button{background:linear-gradient(120deg,#147f9e,#20b4c7);
border:1px solid #60d9e9;color:white;border-radius:7px;
padding:9px;font-size:9px;font-weight:800;cursor:pointer}
button.secondary{background:#183f56;border-color:#47788e}
button:hover{filter:brightness(1.2)}
.buttons{display:flex;gap:7px;margin-top:9px}
.buttons button{flex:1}
.metricgrid{display:grid;grid-template-columns:1fr 1fr;gap:7px}
.metric{padding:9px;border:1px solid #a6ddf022;border-radius:8px;
background:rgba(53,111,137,.2)}
.metricname{font-size:8px;color:#a9d1e3;letter-spacing:.6px}
.metricvalue{font-size:19px;font-weight:850;margin-top:5px}
.unit{font-size:8px;color:#9bc4d8}
.sensor{display:flex;justify-content:space-between;
padding:7px 0;border-bottom:1px solid #ffffff16;font-size:9px;color:#c5deeb}
.on{color:#5de9ae;font-weight:800}.off{color:#f2bd82;font-weight:800}
.alert{padding:9px;border-radius:8px;font-size:9px;line-height:1.6;
background:#185c594f;border:1px solid #52d7ae55;margin-top:8px}
.warning{background:#9b63344c;border-color:#ffbd7655}
#bottom{bottom:13px;left:15px;right:15px;min-height:105px;
display:grid;grid-template-columns:1fr 1fr 1.6fr 1fr;gap:12px}
.bottomlabel{font-size:8px;color:#9dd6ed;letter-spacing:1.5px;margin-bottom:8px}
.big{font-size:20px;font-weight:850}
.muted{font-size:9px;color:#a9cbdc;margin-top:5px}
#chart{width:100%;height:53px}
#chart polyline{fill:none;stroke:#59e0ef;stroke-width:2}
#chart polygon{fill:#49cde522}
#hint{position:absolute;z-index:3;bottom:132px;right:300px;
font-size:9px;color:#153c50;background:#e8f7f8aa;padding:7px 10px;border-radius:7px}
#disclaimer{position:absolute;z-index:3;bottom:132px;left:50%;
transform:translateX(-50%);font-size:8px;color:#163c50;
background:#eaf8f5aa;padding:6px 10px;border-radius:20px;white-space:nowrap}
#loading{position:absolute;inset:0;z-index:10;display:grid;place-content:center;
text-align:center;color:#153a50;background:linear-gradient(#94cce9,#d5e9df);
font-size:17px;font-weight:800}
#loading small{font-size:10px;font-weight:500;margin-top:10px}
#toast{display:none;position:absolute;z-index:12;top:90px;left:50%;
transform:translateX(-50%);background:#123b51;padding:9px 15px;
border-radius:8px;font-size:10px}
@media(max-width:850px){
 #left{width:215px;left:8px}
 #right{width:225px;right:8px}
 #bottom{left:8px;right:8px;grid-template-columns:1fr 1fr}
 #header{left:8px;right:8px}
}
@media(max-width:600px){
 #left{top:85px;width:47%;max-height:48vh}
 #right{top:85px;width:47%;max-height:48vh}
 #bottom{max-height:25vh;overflow:auto}
 .logo{font-size:11px}.tag{font-size:7px;padding:6px}
 #disclaimer,#hint{display:none}
}
</style>
</head>

<body>
<div id="world"></div>
<div id="loading">INITIALIZING DIGITAL BRIDGE ENVIRONMENT
<small>Loading bridge geometry and sensor network</small></div>
<div id="toast"></div>

<div id="header" class="glass">
 <div>
  <div class="logo">INTELLIGENT BRIDGE MONITORING</div>
  <div class="kicker">STRUCTURAL INTELLIGENCE · DIGITAL TWIN</div>
 </div>
 <div class="headright">
  <div class="tag"><span class="green">●</span> SYSTEM ONLINE</div>
  <div class="tag" id="mode">CONTINUOUS MONITORING</div>
  <div class="tag" id="clock">00:00:00</div>
 </div>
</div>

<div id="left" class="glass">
 <div class="heading">01 / SIMULATION CONTROL</div>

 <label>Vehicle weight <output id="weightV">18 t</output></label>
 <input id="weight" type="range" min="5" max="45" value="18">

 <label>Vehicle speed <output id="speedV">55 km/h</output></label>
 <input id="speed" type="range" min="10" max="110" value="55">

 <label>Number of axles <output id="axleV">3</output></label>
 <input id="axles" type="range" min="2" max="6" value="3">

 <label>Traffic volume <output id="trafficV">65%</output></label>
 <input id="traffic" type="range" min="0" max="100" value="65">

 <div class="subheading">STRUCTURAL CHANGE SCENARIO</div>

 <label>Stiffness change <output id="stiffV">0%</output></label>
 <input id="stiff" type="range" min="0" max="30" value="0">

 <label>Local change signal <output id="localV">0%</output></label>
 <input id="local" type="range" min="0" max="100" value="0">

 <label>Test location</label>
 <select id="location">
  <option>Midspan</option>
  <option>North tower</option>
  <option>South tower</option>
  <option>Deck joint</option>
  <option>Cable zone</option>
 </select>

 <label>Event trigger sensitivity <output id="triggerV">65%</output></label>
 <input id="trigger" type="range" min="10" max="100" value="65">

 <div class="subheading">MONITORING CONFIGURATION</div>
 <select id="monitor">
  <option value="adaptive">Adaptive attention</option>
  <option value="primary">Primary sensors only</option>
  <option value="all">All sensors always active</option>
 </select>

 <label>Time step <output id="stepV">1.0 s</output></label>
 <input id="step" type="range" min="1" max="10" value="1">

 <div class="buttons">
  <button id="run">Ⅱ PAUSE</button>
  <button id="reset" class="secondary">↺ RESET</button>
 </div>
 <div class="buttons">
  <button id="addVehicle">＋ VEHICLE</button>
  <button id="camera" class="secondary">CAMERA RESET</button>
 </div>
</div>

<div id="right" class="glass">
 <div class="heading">02 / LIVE STRUCTURAL TELEMETRY</div>

 <div class="metricgrid">
  <div class="metric"><div class="metricname">DECK DEFLECTION</div>
   <div class="metricvalue" id="deflection">2.40</div>
   <div class="unit">mm · simulated</div></div>
  <div class="metric"><div class="metricname">STRAIN PROXY</div>
   <div class="metricvalue" id="strain">118</div>
   <div class="unit">με · simulated</div></div>
  <div class="metric"><div class="metricname">VIBRATION</div>
   <div class="metricvalue" id="vibration">0.12</div>
   <div class="unit">g · simulated</div></div>
  <div class="metric"><div class="metricname">TEMPERATURE</div>
   <div class="metricvalue" id="temperature">27.0</div>
   <div class="unit">°C · simulated</div></div>
 </div>

 <div class="subheading">SENSOR NETWORK</div>
 <div class="sensor"><span>Primary sensors</span><b class="on">55 ONLINE</b></div>
 <div class="sensor"><span>Additional sensors</span><b id="extra" class="off">66 STANDBY</b></div>
 <div class="sensor"><span>Strain gauges</span><b class="on">ACTIVE</b></div>
 <div class="sensor"><span>Accelerometers</span><b class="on">ACTIVE</b></div>
 <div class="sensor"><span>Temperature sensors</span><b class="on">ACTIVE</b></div>
 <div class="sensor"><span>Tilt sensors</span><b id="tilt" class="off">STANDBY</b></div>
 <div class="sensor"><span>Acoustic sensors</span><b id="acoustic" class="off">STANDBY</b></div>
 <div class="sensor"><span>Joint displacement</span><b id="joint" class="off">STANDBY</b></div>

 <div class="subheading">03 / EVENT ANALYSIS</div>
 <div class="metricgrid">
  <div class="metric"><div class="metricname">BASELINE DEVIATION</div>
   <div class="metricvalue" id="deviation">0.0%</div></div>
  <div class="metric"><div class="metricname">PERSISTENCE</div>
   <div class="metricvalue" id="persistence">LOW</div></div>
 </div>
 <div id="alert" class="alert">
  Normal simulated operating pattern. Primary monitoring active.
 </div>

 <div class="subheading">ADDITIONAL SENSOR READINGS</div>
 <div class="sensor"><span>Tilt estimate</span><b id="tiltValue">0.02°</b></div>
 <div class="sensor"><span>Humidity</span><b>68%</b></div>
 <div class="sensor"><span>Corrosion proxy</span><b id="corrosion">Low</b></div>
 <div class="sensor"><span>Crack-width proxy</span><b id="crack">0.00 mm</b></div>
 <div class="sensor"><span>Acoustic activity</span><b id="acousticValue">Low</b></div>
 <div class="sensor"><span>Joint displacement</span><b id="jointValue">0.30 mm</b></div>
</div>

<div id="hint">DRAG TO ORBIT · SCROLL TO ZOOM</div>
<div id="disclaimer">EDUCATIONAL SIMULATION · NOT A REAL BRIDGE SAFETY SYSTEM</div>

<div id="bottom" class="glass">
 <div>
  <div class="bottomlabel">TRAFFIC / LOAD</div>
  <div class="big" id="trafficBig">65%</div>
  <div class="muted">Relative traffic volume</div>
  <div class="muted" id="count">Vehicles: 1</div>
 </div>
 <div>
  <div class="bottomlabel">STRUCTURAL RESPONSE</div>
  <div class="big" id="response">NORMAL</div>
  <div class="muted" id="responseNote">Within simulated baseline</div>
 </div>
 <div>
  <div class="bottomlabel">SENSOR HISTORY / RESPONSE TREND</div>
  <svg id="chart" viewBox="0 0 400 55" preserveAspectRatio="none">
   <polygon id="fill" points="0,52 400,52"/>
   <polyline id="line" points="0,35 400,35"/>
  </svg>
  <div class="muted">Recent simulated measurements</div>
 </div>
 <div>
  <div class="bottomlabel">SYSTEM ACTIONS</div>
  <div class="buttons">
   <button id="export">EXPORT CSV</button>
   <button id="sensorToggle" class="secondary">HIDE SENSORS</button>
  </div>
  <div class="muted" id="exportStatus">Live data collection</div>
 </div>
</div>

<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {Sky} from 'three/addons/objects/Sky.js';

const $ = id => document.getElementById(id);
const root=$('world');
const scene=new THREE.Scene();
scene.background=new THREE.Color(0x9acde9);
scene.fog=new THREE.Fog(0x9acde9,650,1900);

const camera=new THREE.PerspectiveCamera(43,innerWidth/innerHeight,.1,5000);
const defaultCamera=new THREE.Vector3(0,105,360);
camera.position.copy(defaultCamera);

const renderer=new THREE.WebGLRenderer({antialias:true,alpha:false});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.setSize(innerWidth,innerHeight);
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.15;
root.appendChild(renderer.domElement);

const controls=new OrbitControls(camera,renderer.domElement);
controls.enableDamping=true;
controls.dampingFactor=.055;
controls.maxPolarAngle=Math.PI*.49;
controls.minDistance=35;
controls.maxDistance=850;
controls.target.set(0,38,0);

scene.add(new THREE.HemisphereLight(0xdaf5ff,0x54725a,2.1));

const sun=new THREE.DirectionalLight(0xfff1d8,3.2);
sun.position.set(-200,300,140);
sun.castShadow=true;
sun.shadow.mapSize.set(2048,2048);
sun.shadow.camera.left=-400;
sun.shadow.camera.right=400;
sun.shadow.camera.top=400;
sun.shadow.camera.bottom=-400;
scene.add(sun);

const sky=new Sky();
sky.scale.setScalar(4500);
sky.material.uniforms.turbidity.value=6;
sky.material.uniforms.rayleigh.value=2.4;
sky.material.uniforms.mieCoefficient.value=.004;
sky.material.uniforms.mieDirectionalG.value=.8;
sky.material.uniforms.sunPosition.value.copy(sun.position).normalize();
scene.add(sky);

const water=new THREE.Mesh(
 new THREE.PlaneGeometry(5000,5000),
 new THREE.MeshStandardMaterial({
  color:0x287d9d,roughness:.22,metalness:.22
 })
);
water.rotation.x=-Math.PI/2;
water.position.y=-8;
water.receiveShadow=true;
scene.add(water);

const landMat=new THREE.MeshStandardMaterial({color:0x64865a,roughness:1});
for(let i=0;i<22;i++){
 const hill=new THREE.Mesh(new THREE.SphereGeometry(1,32,20),landMat);
 hill.scale.set(75+(i%4)*22,13+(i%3)*5,42);
 hill.position.set(-650+i*65,-4,i%2===0?-250:280);
 scene.add(hill);
}

const bridgeGroup=new THREE.Group();
scene.add(bridgeGroup);
const sensors=new THREE.Group();
scene.add(sensors);
const vehicles=new THREE.Group();
scene.add(vehicles);

let deckY=35;
const bridgeLength=300;
let modelLoaded=false;
let vehicleObjects=[];
let showSensors=true;
let active=true;
let elapsed=0;
let history=[];
let data=[];
let eventDuration=0;
let lastValues={};
let clockSeconds=0;

function mat(color,roughness=.6,metalness=.2){
 return new THREE.MeshStandardMaterial({color,roughness,metalness});
}
const concrete=mat(0xc4cbd0,.78,.1);
const steel=mat(0x9caeb9,.34,.65);
const cableMat=mat(0xe3edf0,.35,.5);
const roadMat=mat(0x303941,.9,.05);
const white=mat(0xf4f4e8,.65,.05);
const greenMat=new THREE.MeshStandardMaterial({
 color:0x34f2a2,emissive:0x087d4b,emissiveIntensity:1.5
});
const redMat=new THREE.MeshStandardMaterial({
 color:0xff5267,emissive:0x8d1024,emissiveIntensity:1.5
});

function box(parent,x,y,z,sx,sy,sz,material){
 const m=new THREE.Mesh(new THREE.BoxGeometry(sx,sy,sz),material);
 m.position.set(x,y,z);
 m.castShadow=true;
 m.receiveShadow=true;
 parent.add(m);
 return m;
}

function cylinder(parent,a,b,r1,r2,material,segments=12){
 const d=new THREE.Vector3().subVectors(b,a);
 const m=new THREE.Mesh(
  new THREE.CylinderGeometry(r1,r2,d.length(),segments),
  material
 );
 m.position.copy(a).add(b).multiplyScalar(.5);
 m.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),d.normalize());
 m.castShadow=true;
 parent.add(m);
 return m;
}

function buildFallbackBridge(){
 bridgeGroup.clear();
 const L=300,W=28,Y=35;

 box(bridgeGroup,0,Y,0,L,2.4,W,roadMat);
 box(bridgeGroup,0,Y-1.5,0,L,1,W+2,steel);

 for(const z of [-W/2-1,W/2+1]){
  box(bridgeGroup,0,Y+2,z,L,.45,.65,white);
  box(bridgeGroup,0,Y+4,z,L,.22,.25,steel);

  for(let x=-L/2;x<=L/2;x+=12){
   box(bridgeGroup,x,Y+3,z,.25,1.4,.25,steel);
  }
 }

 for(let x=-L/2;x<=L/2;x+=12){
  box(bridgeGroup,x,Y+1.25,0,.16,.08,W,white);
 }

 for(const x of [-65,65]){
  const towerWidth=7;
  box(bridgeGroup,x,Y+42,0,towerWidth,84,5,concrete);
  box(bridgeGroup,x,Y+84,0,12,3,8,steel);
  box(bridgeGroup,x,Y+48,0,10,3,8,concrete);

  for(const z of [-3.5,3.5]){
   cylinder(
    bridgeGroup,
    new THREE.Vector3(x,Y+4,z),
    new THREE.Vector3(x,Y+85,z),
    .7,.7,concrete,16
   );
  }

  for(let side of [-1,1]){
   for(let i=0;i<10;i++){
    const dx=(i+1)*10;
    const anchorX=x+side*dx;
    const anchorY=Y+3;
    const towerY=Y+75-i*4.6;

    cylinder(
     bridgeGroup,
     new THREE.Vector3(x,Y+towerY-Y,0),
     new THREE.Vector3(anchorX,anchorY,side*8),
     .09,.09,cableMat,8
    );
   }
  }
 }

 for(let x=-140;x<=140;x+=20){
  for(const z of [-13,13]){
   box(bridgeGroup,x,Y+2.7,z,.4,.35,.4,steel);
  }
 }

 const supports=mat(0x586b75,.8,.1);
 for(const x of [-145,145]){
  box(bridgeGroup,x,Y-13,0,5,25,34,supports);
 }
}

function normalizeModel(model){
 const bounds=new THREE.Box3().setFromObject(model);
 const size=bounds.getSize(new THREE.Vector3());
 const center=bounds.getCenter(new THREE.Vector3());

 // Rotate the model so its longest horizontal dimension follows X.
 if(size.z>size.x && size.z>=size.y){
  model.rotation.y=Math.PI/2;
  model.updateMatrixWorld(true);
 }

 let b=new THREE.Box3().setFromObject(model);
 let s=b.getSize(new THREE.Vector3());
 let c=b.getCenter(new THREE.Vector3());

 const longest=Math.max(s.x,s.y,s.z);
 const scale=300/longest;
 model.scale.multiplyScalar(scale);
 model.updateMatrixWorld(true);

 b.setFromObject(model);
 s=b.getSize(new THREE.Vector3());
 c=b.getCenter(new THREE.Vector3());

 model.position.x-=c.x;
 model.position.z-=c.z;
 model.position.y-=b.min.y-0;
 model.updateMatrixWorld(true);

 // Estimate a useful deck-level sensor height from the model.
 deckY=Math.max(8,Math.min(65,s.y*.28));
}

function addFallback(){
 buildFallbackBridge();
 deckY=35;
 modelLoaded=false;
}

function loadBridge(){
 const url=
 'https://raw.githubusercontent.com/experimentscience/bridge-monitoring-stem/main/assets/cable-stayed-bridge.glb';

 const loader=new GLTFLoader();

 loader.load(
  url,
  gltf=>{
   bridgeGroup.clear();
   const model=gltf.scene;

   model.traverse(obj=>{
    if(obj.isMesh){
     obj.castShadow=true;
     obj.receiveShadow=true;
     if(obj.material){
      obj.material.side=THREE.DoubleSide;
     }
    }
   });

   normalizeModel(model);
   bridgeGroup.add(model);
   modelLoaded=true;
   createSensorNetwork();
   $('loading').style.display='none';
   toast('3D bridge model loaded');
  },
  undefined,
  error=>{
   console.error('Bridge model loading failed:',error);
   addFallback();
   createSensorNetwork();
   $('loading').style.display='none';
   toast('Using built-in bridge model: GLB could not load');
  }
 );
}

function createSensorNetwork(){
 sensors.clear();

 for(let i=0;i<11;i++){
  const x=-135+i*27;
  for(const z of [-10,10]){
   const base=new THREE.Mesh(
    new THREE.SphereGeometry(1.25,12,12),greenMat
   );
   base.position.set(x,deckY+2,z);
   base.userData.kind='primary';
   sensors.add(base);
  }
 }

 const extraPositions=[
  [-95,deckY+12,-8],[-65,deckY+15,8],
  [-30,deckY+8,-8],[0,deckY+12,8],
  [30,deckY+8,-8],[65,deckY+15,8],
  [95,deckY+12,-8]
 ];

 extraPositions.forEach(p=>{
  const s=new THREE.Mesh(
   new THREE.SphereGeometry(1.55,14,14),redMat
  );
  s.position.set(...p);
  s.userData.kind='extra';
  s.visible=false;
  sensors.add(s);
 });

 sensors.visible=showSensors;
}

function createVehicle(color=0x3d86c5){
 const group=new THREE.Group();
 const body=mat(color,.35,.35);
 const glass=mat(0x9ccbd8,.2,.45);
 const dark=mat(0x202a31,.7,.1);

 box(group,0,2,0,9,3.2,4.2,body);
 box(group,1,4.3,0,4.5,2.2,3.8,glass);

 for(const x of [-3,3]){
  for(const z of [-2.2,2.2]){
   const wheel=new THREE.Mesh(
    new THREE.CylinderGeometry(1,1,.55,16),
    dark
   );
   wheel.rotation.x=Math.PI/2;
   wheel.position.set(x,1,z);
   group.add(wheel);
  }
 }

 group.userData.progress=Math.random()*.45;
 group.userData.speed=.055+Math.random()*.025;
 vehicles.add(group);
 vehicleObjects.push(group);
 return group;
}

function addVehicle(){
 createVehicle([0x3d86c5,0xe1a24a,0x738d9c,0x4d9b82][
  Math.floor(Math.random()*4)
 ]);
 updateVehicleCount();
 toast('Vehicle added to simulation');
}

function updateVehicleCount(){
 $('count').textContent='Vehicles: '+vehicleObjects.length;
}

function toast(message){
 const el=$('toast');
 el.textContent=message;
 el.style.display='block';
 clearTimeout(toast.timer);
 toast.timer=setTimeout(()=>el.style.display='none',2400);
}

function resetCamera(){
 camera.position.copy(defaultCamera);
 controls.target.set(0,38,0);
 controls.update();
}

function value(id){
 return Number($(id).value);
}

function updateLabels(){
 $('weightV').textContent=value('weight')+' t';
 $('speedV').textContent=value('speed')+' km/h';
 $('axleV').textContent=value('axles');
 $('trafficV').textContent=value('traffic')+'%';
 $('stiffV').textContent=value('stiff')+'%';
 $('localV').textContent=value('local')+'%';
 $('triggerV').textContent=value('trigger')+'%';
 $('stepV').textContent=(value('step')/1).toFixed(1)+' s';
 $('trafficBig').textContent=value('traffic')+'%';
}

document.querySelectorAll('input[type=range],select').forEach(el=>{
 el.addEventListener('input',updateLabels);
 el.addEventListener('change',updateLabels);
});

function updateSensorState(event){
 const mode=$('monitor').value;
 const extraOn=
  mode==='all' ||
  (mode==='adaptive' && event);

 $('extra').textContent=extraOn?'66 ACTIVE':'66 STANDBY';
 $('extra').className=extraOn?'on':'off';

 ['tilt','acoustic','joint'].forEach(id=>{
  $(id).textContent=extraOn?'ACTIVE':'STANDBY';
  $(id).className=extraOn?'on':'off';
 });

 sensors.children.forEach(s=>{
  if(s.userData.kind==='extra'){
   s.visible=showSensors && extraOn;
  }
 });
}

function updateChart(){
 const points=history.slice(-70);
 if(points.length<2)return;

 const max=Math.max(1,...points);
 const min=0;
 const coords=points.map((v,i)=>{
  const x=i/(points.length-1)*400;
  const y=49-(v-min)/(max-min)*42;
  return `${x.toFixed(1)},${y.toFixed(1)}`;
 });

 $('line').setAttribute('points',coords.join(' '));
 $('fill').setAttribute(
  'points',
  `0,52 ${coords.join(' ')} 400,52`
 );
}

function recordRow(values){
 data.push({
  time:elapsed.toFixed(1),
  traffic:value('traffic'),
  vehicle_weight:value('weight'),
  vehicle_speed:value('speed'),
  deflection:values.deflection.toFixed(3),
  strain:values.strain.toFixed(2),
  vibration:values.vibration.toFixed(3),
  temperature:values.temperature.toFixed(2),
  deviation:values.deviation.toFixed(2),
  event:values.event?'1':'0',
  persistence:values.persistence
 });

 if(data.length>5000)data.shift();
}

function updateSimulation(dt){
 const traffic=value('traffic')/100;
 const weight=value('weight');
 const stiffness=value('stiff');
 const local=value('local');
 const sensitivity=value('trigger')/100;
 const mode=$('monitor').value;

 const load=traffic*(.35+weight/45);
 const wave=Math.sin(elapsed*2.1);
 const vibrationBase=.035+load*.13+Math.abs(wave)*.025;
 const deflectionBase=1.2+load*2.4;
 const strainBase=70+load*90;

 // A temporary vehicle-load response changes with traffic.
 // Structural-change controls add a persistent simulated signal.
 const structuralSignal=stiff*.075+local*.045;
 const deflection=deflectionBase+structuralSignal+
  Math.abs(wave)*load*.4;
 const strain=strainBase+stiff*2.4+local*.8+
  Math.sin(elapsed*1.8)*load*8;
 const vibration=vibrationBase+local*.002+
  Math.abs(Math.sin(elapsed*3.2))*.018;
 const temperature=27+Math.sin(elapsed*.025)*1.4;

 const deviation=Math.min(
  100,
  Math.max(0,structuralSignal*3.2+local*.16+stiff*.11)
 );

 const eventScore=
  (vibration-.08)*240+
  structuralSignal*.55+
  traffic*.22;

 const event=mode==='all' ||
  (mode==='adaptive' && eventScore>sensitivity);

 if(event)eventDuration+=dt;
 else eventDuration=Math.max(0,eventDuration-dt*.65);

 const persistence=
  deviation>12 && eventDuration>12?'HIGH':
  deviation>5 && eventDuration>5?'MODERATE':'LOW';

 updateSensorState(event);

 $('deflection').textContent=deflection.toFixed(2);
 $('strain').textContent=strain.toFixed(0);
 $('vibration').textContent=vibration.toFixed(3);
 $('temperature').textContent=temperature.toFixed(1);
 $('deviation').textContent=deviation.toFixed(1)+'%';
 $('persistence').textContent=persistence;

 $('tiltValue').textContent=(.02+local*.004).toFixed(2)+'°';
 $('corrosion').textContent=local>65?'Elevated proxy':'Low';
 $('crack').textContent=(local*.002).toFixed(2)+' mm';
 $('acousticValue').textContent=event?'Elevated':'Low';
 $('jointValue').textContent=(.30+local*.008).toFixed(2)+' mm';

 const alert=$('alert');
 if(persistence==='HIGH'){
  alert.className='alert warning';
  alert.textContent=
   'Persistent simulated deviation detected. Additional sensor attention remains active for investigation.';
 }else if(event){
  alert.className='alert';
  alert.textContent=
   'Event trigger activated. Additional sensor measurements are being collected.';
 }else{
  alert.className='alert';
  alert.textContent=
   'Normal simulated operating pattern. Primary monitoring active.';
 }

 $('mode').textContent=
  mode==='adaptive'?'ADAPTIVE ATTENTION':
  mode==='all'?'ALL SENSORS ACTIVE':'PRIMARY ONLY';

 $('response').textContent=
  persistence==='HIGH'?'PERSISTENT CHANGE':
  event?'EVENT DETECTED':'NORMAL';

 $('responseNote').textContent=
  persistence==='HIGH'?'Deviation remains elevated':
  event?'Additional sensors activated':'Within simulated baseline';

 history.push(deviation+load*1.8);
 if(history.length>70)history.shift();
 updateChart();

 const values={
  deflection,strain,vibration,temperature,deviation,
  event,persistence
 };

 lastValues=values;
 if(Math.floor(elapsed*2)!==Math.floor((elapsed-dt)*2)){
  recordRow(values);
 }
}

function animateVehicles(dt){
 const speed=value('speed');
 const speedFactor=speed/55;

 vehicleObjects.forEach(v=>{
  v.userData.progress+=dt*.035*speedFactor*v.userData.speed/.065;
  if(v.userData.progress>1.1){
   v.userData.progress=-.1;
  }

  const p=v.userData.progress;
  v.position.set(-145+p*290,deckY+2,0);
 });
}

function updateClock(){
 clockSeconds+=1;
 const h=String(Math.floor(clockSeconds/3600)).padStart(2,'0');
 const m=String(Math.floor(clockSeconds%3600/60)).padStart(2,'0');
 const s=String(clockSeconds%60).padStart(2,'0');
 $('clock').textContent=`${h}:${m}:${s}`;
}

let lastTime=performance.now();
let clockAccumulator=0;

function animate(now){
 requestAnimationFrame(animate);
 const realDt=Math.min((now-lastTime)/1000,.05);
 lastTime=now;

 if(active){
  const step=value('step');
  const dt=realDt*step;
  elapsed+=dt;
  animateVehicles(dt);
  updateSimulation(dt);
  clockAccumulator+=realDt;
  if(clockAccumulator>=1){
   updateClock();
   clockAccumulator=0;
  }
 }

 controls.update();
 renderer.render(scene,camera);
}

$('run').addEventListener('click',()=>{
 active=!active;
 $('run').textContent=active?'Ⅱ PAUSE':'▶ RESUME';
});

$('reset').addEventListener('click',()=>{
 elapsed=0;
 eventDuration=0;
 history=[];
 data=[];
 vehicleObjects.forEach(v=>vehicles.remove(v));
 vehicleObjects=[];
 createVehicle();
 updateVehicleCount();
 $('stiff').value=0;
 $('local').value=0;
 $('traffic').value=65;
 $('weight').value=18;
 $('speed').value=55;
 $('axles').value=3;
 $('trigger').value=65;
 $('step').value=1;
 $('monitor').value='adaptive';
 updateLabels();
 updateSensorState(false);
 toast('Simulation reset');
});

$('addVehicle').addEventListener('click',addVehicle);
$('camera').addEventListener('click',resetCamera);

$('sensorToggle').addEventListener('click',()=>{
 showSensors=!showSensors;
 sensors.visible=showSensors;
 $('sensorToggle').textContent=
  showSensors?'HIDE SENSORS':'SHOW SENSORS';
});

$('export').addEventListener('click',()=>{
 if(!data.length){
  toast('No measurements recorded yet');
  return;
 }

 const headers=Object.keys(data[0]);
 const rows=data.map(row=>
  headers.map(h=>JSON.stringify(row[h])).join(',')
 );
 const csv=[headers.join(','),...rows].join('\n');
 const blob=new Blob([csv],{type:'text/csv'});
 const url=URL.createObjectURL(blob);
 const a=document.createElement('a');
 a.href=url;
 a.download='bridge-monitoring-data.csv';
 a.click();
 URL.revokeObjectURL(url);
 $('exportStatus').textContent=data.length+' records exported';
});

window.addEventListener('resize',()=>{
 camera.aspect=innerWidth/innerHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(innerWidth,innerHeight);
});

updateLabels();
createVehicle();
updateVehicleCount();
loadBridge();
requestAnimationFrame(animate);
</script>
</body>
</html>
"""

components.html(html, height=1000, scrolling=False)
