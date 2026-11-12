import base64
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ASSET_DIR = Path(__file__).resolve().parent / "assets" / "weather"


@st.cache_data(show_spinner=False)
def image_uri(path_string: str) -> str:
    path = Path(path_string)
    if not path.is_file():
        return ""
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def render():
    """Weather World 6.0: interactive paper-cut scene."""
    st.header("☀️ Weather World")
    st.write("Drag paper-cut weather elements into the scene. Arrange them freely and discover magical combinations!")

    names = ["sun", "cloud", "rain", "snow", "wind", "background", "water", "lightning", "rainbow", "tornado"]
    assets = {name: image_uri(str(ASSET_DIR / f"{name}.png")) for name in names}
    missing = [f"{name}.png" for name in names if not assets[name]]
    if missing:
        st.warning("Missing weather assets: " + ", ".join(missing))

    asset_json = json.dumps(assets)
    html_code = r'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}body{margin:0;padding:15px;font-family:Arial,sans-serif;background:#fff9fc;color:#705b85;text-align:center}
h2{margin:3px 0 9px;font-size:24px}.hint{font-size:13px;margin:0 0 16px;line-height:1.6}
.toolbar{display:flex;justify-content:center;gap:11px;flex-wrap:wrap;margin-bottom:17px}
.tool{width:78px;height:86px;background:#fff;border:2px solid #ead3f0;border-radius:18px;box-shadow:0 4px 0 #ead9ed;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;cursor:grab;touch-action:none;user-select:none}
.tool:hover{background:#fffafc;transform:translateY(-2px)}.tool img{width:51px;height:51px;object-fit:contain;pointer-events:none}.tool .name{font-size:12px}
/* Keep the source artwork's aspect ratio; crop instead of stretching. */
.scene{height:390px;position:relative;overflow:hidden;border:4px solid #f1d6e9;border-radius:24px;background-color:#cfeaff;background-size:cover;background-position:center;touch-action:none;isolation:isolate}
.scene::before{content:"";position:absolute;inset:0;background:#71849a;opacity:0;transition:opacity 1.8s;z-index:1;pointer-events:none}
.scene[data-weather="snowcloud"]::before{background:#b7cee1;opacity:.25}
.scene[data-weather="water"]::before{background:#fff3bc;opacity:.18}
.scene[data-weather="storm"]::before{background:#34465e;opacity:.62}
.scene[data-weather="blizzard"]::before{background:#789ab8;opacity:.56}
.item{position:absolute;width:86px;height:86px;display:grid;place-items:center;z-index:6;transform:translate(-50%,-50%);touch-action:none;cursor:grab;user-select:none}
.item:active{cursor:grabbing}.item.selected{outline:2px dashed #b17dc4;border-radius:50%}
.item .symbol{width:100%;height:100%;object-fit:contain;pointer-events:none;filter:drop-shadow(2px 5px 3px #71627a30);animation:bob 3.5s ease-in-out infinite}
.item.sun .symbol{animation:spin 22s linear infinite}.item.cloud .symbol{animation:bob 4s ease-in-out infinite}.item.rain .symbol{animation:bob 3.1s ease-in-out infinite}.item.snow .symbol{animation:spin 13s linear infinite}.item.wind .symbol{animation:wind 2.4s ease-in-out infinite}
.item.water .symbol{width:60%;height:60%;animation:waterBounce 2.2s ease-in-out infinite}
.item.snow .symbol{width:55%;height:55%}
.item.snowcloud,.item.storm{width:125px;height:125px}
.combo{width:100%;height:100%;position:relative;pointer-events:none;animation:bob 4s ease-in-out infinite}
.combo .cloud-body{position:absolute;z-index:2;width:100%;height:67%;top:0;left:0;object-fit:contain;filter:drop-shadow(2px 4px 3px #52647733)}
.combo .hanger{position:absolute;z-index:1;top:48%;width:24%;height:49%;transform-origin:50% 0;animation:swing 2.7s ease-in-out infinite}
.combo .hanger:nth-of-type(2){animation-duration:3.5s;animation-direction:reverse}
.combo .hanger:nth-of-type(3){animation-duration:3.1s}
.combo .hanger::before{content:"";position:absolute;top:0;left:50%;width:2px;height:52%;background:#b5cddd;transform:translateX(-50%)}
.combo .hanger img{position:absolute;bottom:0;left:0;width:100%;height:57%;object-fit:contain}
.combo .hanger.left{left:13%;top:45%;height:43%}.combo .hanger.middle{left:39%;top:48%;height:55%}.combo .hanger.right{left:65%;top:45%;height:38%}
.combo .bolt{position:absolute;z-index:1;left:39%;top:48%;width:26%;height:53%;object-fit:contain;animation:boltFlash 3.5s steps(1) infinite}
.combo .storm-cloud{filter:brightness(.62) saturate(.65) sepia(.08) drop-shadow(2px 4px 3px #52647755)}
.rainbow{position:absolute;left:50%;top:42%;width:220px;height:140px;object-fit:contain;transform:translate(-50%,-50%) scale(.65);opacity:0;transition:opacity .7s,transform .7s;pointer-events:none;z-index:3}
.rainbow.visible{opacity:1;transform:translate(-50%,-50%) scale(1)}
#effects{position:absolute;inset:0;pointer-events:none;z-index:4;overflow:hidden}
.snow-particle{position:absolute;top:-12%;color:#fff;font-size:15px;opacity:.9;animation:snowFall linear infinite;text-shadow:0 1px 3px #7c9aaf}
.scene:not([data-weather="snowcloud"]):not([data-weather="blizzard"]) .snow-particle{display:none}
.scene[data-weather="blizzard"] .snow-particle{animation-name:blizzardFall;animation-duration:1.5s!important;font-size:20px!important}
.snow-ground{position:absolute;bottom:-6px;left:0;width:100%;height:12%;background:linear-gradient(0deg,#f9fcffeb,#e6f2ff99 60%,transparent);opacity:0;transition:opacity 1.6s}
.scene[data-weather="snowcloud"] .snow-ground{opacity:1}
.storm-flash{position:absolute;inset:0;background:#fffce2;opacity:0}
.scene[data-weather="storm"] .storm-flash{animation:skyFlash 5s infinite}
.water-ripple{position:absolute;bottom:8%;left:50%;width:35px;height:12px;border:2px solid #b0e1f6;border-radius:50%;opacity:0}
.scene[data-weather="water"] .water-ripple{animation:ripple 2.4s ease-out infinite}
.water-ripple.second{animation-delay:1.2s!important}
@keyframes blizzardFall{from{transform:translate(-50px,-30px) rotate(0)}to{transform:translate(270px,490px) rotate(540deg)}}
@keyframes snowFall{from{transform:translateY(-10px) rotate(0)}to{transform:translateY(500px) rotate(140deg)}}
@keyframes swing{0%,100%{transform:rotate(-10deg)}50%{transform:rotate(10deg)}}
@keyframes waterBounce{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-9px) scale(1.04,.97)}}
@keyframes boltFlash{0%,10%,14%,100%{opacity:1}11%,13%,65%{opacity:.12}}
@keyframes skyFlash{0%,67%,69%,72%,100%{opacity:0}68%,71%{opacity:.42}}
@keyframes ripple{0%{opacity:.75;transform:translateX(-50%) scale(.4)}100%{opacity:0;transform:translateX(-50%) scale(3.5)}}
#tornado{position:absolute;inset:0;z-index:12;pointer-events:none;display:none;align-items:center;justify-content:center}
#tornado.active{display:flex}
/* The tornado artwork stays upright; only a gentle sway and scale are animated. */
#tornado img{width:260px;height:310px;max-width:45%;max-height:90%;object-fit:contain;filter:drop-shadow(4px 8px 5px #4c759855);transform-origin:50% 65%;animation:tornadoGrow 5.4s ease-in-out forwards}
@keyframes tornadoGrow{0%{transform:translateY(15px) rotate(-3deg) scale(.05);opacity:0}20%{transform:translateY(0) rotate(2deg) scale(.85);opacity:1}42%{transform:translateY(-5px) rotate(-3deg) scale(1.08);opacity:1}62%{transform:translateY(0) rotate(3deg) scale(1.16);opacity:1}82%{transform:translateY(-4px) rotate(-2deg) scale(1);opacity:1}100%{transform:translateY(10px) rotate(0) scale(.05);opacity:0}}
#feedback{min-height:30px;font-size:15px;font-weight:bold;margin:13px auto 5px}#discoveries{font-size:12px;margin-bottom:11px}.controls{display:flex;justify-content:center;gap:10px;flex-wrap:wrap}
button.action{background:#eed0ef;color:#654a74;border:0;border-radius:25px;padding:10px 17px;cursor:pointer;font-weight:bold}button.action:hover{background:#e4bce9}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}@keyframes spin{to{transform:rotate(360deg)}}@keyframes wind{0%,100%{transform:translateX(-8px) rotate(-4deg)}50%{transform:translateX(9px) rotate(5deg)}}
@media(max-width:550px){.scene{height:320px}.tool{width:65px;height:75px}.tool img{width:43px;height:43px}.item{width:69px;height:69px}.item.snowcloud,.item.storm{width:108px;height:108px}}
@media(prefers-reduced-motion:reduce){.item .symbol,.combo,.hanger,.bolt,.snow-particle,.storm-flash,.water-ripple{animation:none!important}.rainbow,.scene::before{transition:none}}
</style></head><body>
<h2>🌈 Create Your Weather</h2><p class="hint">Drag or click to add. Move freely. Bring Sun near Rain for a rainbow; overlap and release to fuse!</p>
<div class="toolbar" id="toolbar"></div><div class="scene" id="scene" aria-label="Interactive weather scene"><div id="tornado" aria-hidden="true"><img id="tornado-art" alt="" draggable="false"/></div><div id="effects"><div class="snow-ground"></div><div class="storm-flash"></div><div class="water-ripple"></div><div class="water-ripple second"></div></div><img class="rainbow" id="rainbow" alt="Rainbow"/></div>
<div id="feedback" aria-live="polite">✨ Create your own sky!</div><div id="discoveries">Discoveries: 0 / 6</div>
<div class="controls"><button class="action" id="remove">🗑️ Remove selected</button><button class="action" id="reset">🔄 Reset World</button></div>
<script>
const ASSETS=__ASSET_JSON__;
(()=>{
'use strict';
const TYPES={sun:{emoji:'☀️',name:'Sun'},cloud:{emoji:'☁️',name:'Cloud'},rain:{emoji:'🌧️',name:'Rain'},snow:{emoji:'❄️',name:'Snow'},wind:{emoji:'🌬️',name:'Wind'},snowcloud:{emoji:'🌨️',name:'Snow Cloud'},water:{emoji:'💧',name:'Water'},storm:{emoji:'⛈️',name:'Storm'}};
const STARTERS=['sun','cloud','rain','snow','wind'];
const RECIPES={'cloud+snow':{result:'snowcloud',message:'🌨️ A snowy cloud is born!'},'snow+sun':{result:'water',message:'💧 Sunshine melts the snow!'},'cloud+rain':{result:'storm',message:'⛈️ A storm is brewing!'},'snow+wind':{result:'blizzard',message:'🌨️ A blizzard is sweeping through!'},'wind+wind':{result:'tornado',message:'🌪️ A tornado is sweeping the sky!'}};
const scene=document.getElementById('scene'),toolbar=document.getElementById('toolbar'),feedback=document.getElementById('feedback'),discoveries=document.getElementById('discoveries'),rainbow=document.getElementById('rainbow');
if(ASSETS.background)scene.style.backgroundImage=`url("${ASSETS.background}")`;
if(ASSETS.tornado)document.getElementById('tornado-art').src=ASSETS.tornado;
if(ASSETS.rainbow)rainbow.src=ASSETS.rainbow;
else {rainbow.style.fontSize='90px';rainbow.alt='🌈';}
const effects=document.getElementById('effects');
for(let i=0;i<24;i++){const flake=document.createElement('span');flake.className='snow-particle';flake.textContent='✳';flake.style.left=(i*43.7%100)+'%';flake.style.animationDuration=(4+(i%6)*.7)+'s';flake.style.animationDelay=(-i*.39)+'s';flake.style.fontSize=(9+(i%4)*3)+'px';effects.appendChild(flake);}
function setWeather(type){scene.dataset.weather=(blizzardActive && type!=='normal' && type!=='blizzard')?'blizzard':(type||'normal');}
let items=[],selected=null,drag=null,seq=0,locked=false,eventTimer=null,blizzardActive=false;const discovered=new Set();
function updateDiscoveries(){discoveries.textContent=`Discoveries: ${discovered.size} / 6`;}
function blizzard(){if(eventTimer)clearTimeout(eventTimer);blizzardActive=true;setWeather('blizzard');feedback.textContent='🌨️ Blizzard! Snow sweeps across the sky.';eventTimer=setTimeout(()=>{blizzardActive=false;setWeather('normal');feedback.textContent='✨ The blizzard has passed!';draw();eventTimer=null;},8000);}
function tornado(){
 if(eventTimer)clearTimeout(eventTimer);eventTimer=null;blizzardActive=false;locked=true;drag=null;setWeather('normal');rainbow.classList.remove('visible');
 const funnel=document.getElementById('tornado');funnel.classList.add('active');
 feedback.textContent='🌪️ Tornado! The weather is being swept away!';
 const nodes=[...scene.querySelectorAll('.item')];
 const r=scene.getBoundingClientRect();
 nodes.forEach((node,i)=>{
  const b=node.getBoundingClientRect(),x=b.left+b.width/2-r.left,y=b.top+b.height/2-r.top;
  const cx=r.width/2-x,cy=r.height/2-y;
  const angle=(i*137.5)*Math.PI/180;
  const exitX=Math.cos(angle)*r.width*1.5,exitY=Math.sin(angle)*r.height*1.8;
  node.style.zIndex='13';
  node.animate([{transform:'translate(-50%,-50%) rotate(0deg)',opacity:1,offset:0},
   {transform:`translate(calc(-50% + ${cx}px),calc(-50% + ${cy}px)) rotate(540deg) scale(.65)`,opacity:1,offset:.52},
   {transform:`translate(calc(-50% + ${exitX}px),calc(-50% + ${exitY}px)) rotate(1080deg) scale(.25)`,opacity:0,offset:1}],
   {duration:4600,delay:i*110,fill:'forwards',easing:'ease-in-out'});
 });
 eventTimer=setTimeout(()=>{items=[];selected=null;funnel.classList.remove('active');locked=false;setWeather('normal');feedback.textContent='✨ The sky is clear again!';draw();},5600);
}
const clamp=(n,min,max)=>Math.max(min,Math.min(max,n));
const recipeKey=(a,b)=>[a,b].sort().join('+');
function coords(event){const r=scene.getBoundingClientRect();return{x:clamp((event.clientX-r.left)/r.width,.055,.945),y:clamp((event.clientY-r.top)/r.height,.12,.88)};}
function distance(a,b){return Math.hypot((a.x-b.x)*scene.clientWidth,(a.y-b.y)*scene.clientHeight);}
function place(type,x,y){const item={id:++seq,type,x,y};items.push(item);draw();return item;}
function symbol(type){
if(type==='snowcloud'||type==='storm'){
 const group=document.createElement('div');group.className='combo';
 const cloud=document.createElement('img');cloud.className='cloud-body'+(type==='storm'?' storm-cloud':'');cloud.src=ASSETS.cloud||'';cloud.alt=type;group.appendChild(cloud);
 if(type==='snowcloud'){
  for(const pos of ['left','middle','right']){const hanger=document.createElement('div');hanger.className='hanger '+pos;const flake=document.createElement('img');flake.src=ASSETS.snow||'';flake.alt='';hanger.appendChild(flake);group.appendChild(hanger);}
 }else{const bolt=document.createElement('img');bolt.className='bolt';bolt.src=ASSETS.lightning||'';bolt.alt='';group.appendChild(bolt);}
 return group;
}
const asset=ASSETS[type];if(asset){const img=document.createElement('img');img.className='symbol';img.src=asset;img.alt=TYPES[type].name;img.draggable=false;return img;}const span=document.createElement('span');span.className='symbol';span.textContent=TYPES[type].emoji;return span;}
function react(){let near=false;for(let i=0;i<items.length;i++)for(let j=i+1;j<items.length;j++){const a=items[i],b=items[j];if(recipeKey(a.type,b.type)==='rain+sun'&&distance(a,b)<83)near=true;}
rainbow.classList.toggle('visible',near);if(near){const pair=[];for(const a of items)for(const b of items){if(a.id!==b.id&&recipeKey(a.type,b.type)==='rain+sun'&&distance(a,b)<83){pair.push(a,b);break;}if(pair.length)break;}if(pair.length){rainbow.style.left=((pair[0].x+pair[1].x)/2*100)+'%';rainbow.style.top=((pair[0].y+pair[1].y)/2*100-16)+'%';}}if(near){discovered.add('rainbow');feedback.textContent='🌈 A rainbow blooms when Sun meets Rain!';}else if(feedback.textContent.startsWith('🌈'))feedback.textContent='✨ Move elements together to discover magic!';updateDiscoveries();}
function finishDrag(item){if(locked)return;const target=items.find(other=>other.id!==item.id&&distance(item,other)<47&&RECIPES[recipeKey(item.type,other.type)]);if(target){const key=recipeKey(item.type,target.type),recipe=RECIPES[key];const x=(item.x+target.x)/2,y=(item.y+target.y)/2;items=items.filter(v=>v.id!==item.id&&v.id!==target.id);discovered.add(key);selected=null;if(recipe.result==='blizzard'){draw();blizzard();}else if(recipe.result==='tornado'){draw();tornado();}else{place(recipe.result,x,y);setWeather(recipe.result);feedback.textContent=recipe.message;}}else draw();react();}
function draw(){scene.querySelectorAll('.item').forEach(n=>n.remove());for(const item of items){const node=document.createElement('div');node.className='item '+item.type+(selected===item.id?' selected':'');node.dataset.id=item.id;node.style.left=item.x*100+'%';node.style.top=item.y*100+'%';node.appendChild(symbol(item.type));
node.addEventListener('pointerdown',e=>{if(locked)return;e.preventDefault();e.stopPropagation();selected=item.id;drag={kind:'item',id:item.id,pointer:e.pointerId};node.setPointerCapture(e.pointerId);scene.querySelectorAll('.item').forEach(n=>n.classList.toggle('selected',n===node));});
node.addEventListener('pointermove',e=>{if(!drag||drag.kind!=='item'||drag.id!==item.id||drag.pointer!==e.pointerId)return;const p=coords(e);item.x=p.x;item.y=p.y;node.style.left=p.x*100+'%';node.style.top=p.y*100+'%';react();});
node.addEventListener('pointerup',e=>{if(!drag||drag.kind!=='item'||drag.id!==item.id||drag.pointer!==e.pointerId)return;drag=null;finishDrag(item);});
node.addEventListener('pointercancel',()=>{drag=null;draw();react();});scene.appendChild(node);}react();}
for(const type of STARTERS){const t=document.createElement('div');t.className='tool';t.appendChild(symbol(type));const name=document.createElement('span');name.className='name';name.textContent=TYPES[type].name;t.appendChild(name);
t.addEventListener('pointerdown',e=>{if(locked)return;e.preventDefault();drag={kind:'tool',type,pointer:e.pointerId};t.setPointerCapture(e.pointerId);});
t.addEventListener('pointerup',e=>{if(!drag||drag.kind!=='tool'||drag.pointer!==e.pointerId)return;const r=scene.getBoundingClientRect();const inside=e.clientX>=r.left&&e.clientX<=r.right&&e.clientY>=r.top&&e.clientY<=r.bottom;const p=inside?coords(e):{x:.25+Math.random()*.5,y:.25+Math.random()*.35};place(type,p.x,p.y);feedback.textContent=inside?'✨ Element placed!':'✨ Element added — drag to arrange!';drag=null;});
t.addEventListener('pointercancel',()=>drag=null);toolbar.appendChild(t);}
scene.addEventListener('pointerdown',e=>{if(e.target===scene){selected=null;draw();}});
document.getElementById('remove').addEventListener('click',()=>{if(locked)return;if(selected===null){feedback.textContent='Select an element first.';return;}items=items.filter(i=>i.id!==selected);selected=null;feedback.textContent='🗑️ Element removed.';draw();});
document.getElementById('reset').addEventListener('click',()=>{if(eventTimer)clearTimeout(eventTimer);eventTimer=null;locked=false;blizzardActive=false;document.getElementById('tornado').classList.remove('active');items=[];selected=null;discovered.clear();setWeather('normal');feedback.textContent='✨ A fresh sky awaits!';draw();});
window.addEventListener('resize',react);setWeather('normal');draw();
})();
</script></body></html>'''
    html_code = html_code.replace("__ASSET_JSON__", asset_json)
    components.html(html_code, height=720, scrolling=True)
