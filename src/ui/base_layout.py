import streamlit as st
import streamlit.components.v1 as components


# ──────────────────────────────────────────────────────────────
#  HOME PAGE BACKGROUND + CURSOR-REACTIVE PARTICLE CANVAS
# ──────────────────────────────────────────────────────────────
def style_background_home():

    # ── 1. CSS (no JS) — aurora background + glassmorphism cards ──
    st.markdown(
        """
<style>
.stApp {
    background: radial-gradient(circle at center, #0a0f1d 0%, #030408 100%) !important;
    overflow: hidden;
}
.stApp > div               { position: relative; z-index: 2; }
.block-container           { position: relative; z-index: 2; }

/* Style text/headers on home screen for high visibility */
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    color: #ffffff !important;
}
.stApp p:not(button *), .stApp span:not(button *), .stApp label:not(button *) {
    color: #c7d2fe !important;
}

.stApp [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:has(h2) {
    background: rgba(15, 23, 42, 0.45) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
    border: 1px solid rgba(99, 102, 241, 0.25) !important;
    border-radius: 2.5rem !important;
    padding: 2.5rem !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4), 0 0 15px rgba(99, 102, 241, 0.08) !important;
    transition: transform 0.4s cubic-bezier(.25,.8,.25,1), box-shadow 0.4s ease, border-color 0.4s ease !important;
    animation: cardSlideIn 0.9s cubic-bezier(.25,.8,.25,1) both;
}
.stApp [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:has(h2):hover {
    transform: translateY(-8px) scale(1.015) !important;
    border-color: rgba(99, 102, 241, 0.6) !important;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.55), 0 0 25px rgba(99, 102, 241, 0.25) !important;
}
@keyframes cardSlideIn {
    from { opacity:0; transform:translateY(50px) scale(0.93); }
    to   { opacity:1; transform:translateY(0) scale(1); }
}
.stApp [data-testid="stHorizontalBlock"] { gap: 2.5rem !important; }
.stApp h2 { color: #ffffff !important; text-shadow: 0 0 20px rgba(99, 102, 241, 0.35); }
.stApp p  { color: #c7d2fe !important; }

.aurora-orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(90px);
    pointer-events: none;
    z-index: 0;
    animation: driftOrb ease-in-out infinite alternate;
}
.ao1 { width:500px; height:500px; background:rgba(99, 102, 241, 0.12);  top:-15%; left:-10%; animation-duration:12s; }
.ao2 { width:380px; height:380px; background:rgba(59, 130, 246, 0.10);  bottom:-10%; right:-5%; animation-duration:16s; animation-delay:-5s; }
.ao3 { width:280px; height:280px; background:rgba(168, 85, 247, 0.08);  top:40%; left:55%; animation-duration:10s; animation-delay:-3s; }
.ao4 { width:220px; height:220px; background:rgba(56, 189, 248, 0.06);  top:60%; left:10%; animation-duration:14s; animation-delay:-8s; }
@keyframes driftOrb {
    from { transform: translate(0,0) scale(1); }
    to   { transform: translate(40px,35px) scale(1.12); }
}
</style>
<div class="aurora-orb ao1"></div>
<div class="aurora-orb ao2"></div>
<div class="aurora-orb ao3"></div>
<div class="aurora-orb ao4"></div>
        <div class="aurora-orb ao4"></div>
        """,
        unsafe_allow_html=True,
    )

    # ── 2. Cursor-reactive canvas injected into parent doc ──
    components.html(
        """<!DOCTYPE html><html><head>
        <style>* { margin:0;padding:0; } html,body { background:transparent;overflow:hidden; }</style>
        </head><body><script>
        (function(){
          var pd=window.parent.document, pb=window.parent.document.body;
          var old=pd.getElementById('sc-cv'); if(old) old.remove();
          var cv=pd.createElement('canvas'); cv.id='sc-cv';
          cv.style.cssText='position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:1;';
          pb.appendChild(cv);
          var ctx=cv.getContext('2d');
          function resize(){ cv.width=window.parent.innerWidth; cv.height=window.parent.innerHeight; }
          resize(); window.parent.addEventListener('resize',resize);

          var PAL=['#ffffff','#e0f2fe','#bae6fd','#7dd3fc','#c7d2fe','#e0e7ff','#a5b4fc','#f0f9ff'];
          var mouse={x:cv.width/2, y:cv.height/2};
          var active=false;
          window.parent.addEventListener('mousemove',function(e){ 
            mouse.x=e.clientX; 
            mouse.y=e.clientY; 
            active=true;
          });
          window.parent.addEventListener('mouseleave',function(){ 
            active=false; 
          });

          function Particle(x,y,fc){
            this.fc=!!fc;
            this.x=x!=null?x:Math.random()*cv.width;
            this.y=y!=null?y:Math.random()*cv.height;
            this.ox=this.x; this.oy=this.y;
            this.vx=(Math.random()-0.5)*0.8; this.vy=(Math.random()-0.5)*0.8;
            this.r=fc?Math.random()*2+1.5:Math.random()*1.5+0.8;
            this.life=fc?Math.random()*50+30:Infinity;
            this.age=0;
            this.col=PAL[Math.floor(Math.random()*PAL.length)];
          }
          Particle.prototype.update=function(){
            if(active){
              var dx=mouse.x-this.x,dy=mouse.y-this.y,d=Math.sqrt(dx*dx+dy*dy)||1;
              if(d<250){
                var force=(250-d)/250;
                // Antigravity orbit/attraction physics
                this.vx+=(dx/d)*force*0.18;
                this.vy+=(dy/d)*force*0.18;
                if(d<50){
                  this.vx-= (dx/d)*0.5;
                  this.vy-= (dy/d)*0.5;
                }
              } else {
                if(!this.fc){
                  this.vx+=(this.ox-this.x)*0.003;
                  this.vy+=(this.oy-this.y)*0.003;
                }
              }
            } else {
              if(!this.fc){
                this.vx+=(this.ox-this.x)*0.003;
                this.vy+=(this.oy-this.y)*0.003;
              }
            }

            // Drag
            this.vx*=0.94; this.vy*=0.94;
            this.x+=this.vx; this.y+=this.vy; 
            this.age++;
          };
          Particle.prototype.alpha=function(){ return this.fc?Math.max(0,1-this.age/this.life):0.7; };
          Particle.prototype.dead=function(){ return this.fc&&this.age>=this.life; };
          Particle.prototype.draw=function(){
            var a=this.alpha(); if(a<=0)return;
            var g=ctx.createRadialGradient(this.x,this.y,0,this.x,this.y,this.r*5);
            g.addColorStop(0,this.col+'cc');g.addColorStop(0.4,this.col+'44');g.addColorStop(1,this.col+'00');
            ctx.globalAlpha=a*0.5;ctx.beginPath();ctx.arc(this.x,this.y,this.r*5,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
            ctx.globalAlpha=a;ctx.beginPath();ctx.arc(this.x,this.y,this.r,0,Math.PI*2);
            ctx.fillStyle=this.col;ctx.fill();
          };

          var parts=[]; for(var i=0;i<80;i++) parts.push(new Particle());
          var tick=0;
          window.parent.addEventListener('mousemove',function(){
            tick++;
            if(tick%2===0){ 
              for(var i=0;i<2;i++) parts.push(new Particle(mouse.x+(Math.random()-0.5)*8,mouse.y+(Math.random()-0.5)*8,true)); 
            }
          });

          function edges(){
            var am=parts.filter(function(p){return !p.fc;});
            for(var i=0;i<am.length;i++){for(var j=i+1;j<am.length;j++){
              var a=am[i],b=am[j],dx=a.x-b.x,dy=a.y-b.y,d=Math.sqrt(dx*dx+dy*dy);
              if(d<110){
                var t=1-d/110;
                ctx.globalAlpha=t*0.12;
                ctx.lineWidth=0.5;
                ctx.strokeStyle='rgba(224,242,254,0.35)'; // Crisp light ice-blue lines
                ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();
              }
            }}
          }
          function ring(){
            if(!active) return;
            var rs=[{r:22,w:1.2,a:0.4},{r:38,w:0.8,a:0.2},{r:58,w:0.4,a:0.08}];
            rs.forEach(function(r){
              ctx.globalAlpha=r.a;ctx.lineWidth=r.w;ctx.strokeStyle='#38bdf8';
              ctx.beginPath();ctx.arc(mouse.x,mouse.y,r.r,0,Math.PI*2);ctx.stroke();
            });
            ctx.globalAlpha=1;
          }
          function loop(){
            ctx.clearRect(0,0,cv.width,cv.height);
            parts=parts.filter(function(p){return !p.dead();});
            var cp=parts.filter(function(p){return p.fc;});
            if(cp.length>200) parts=parts.filter(function(p){return !p.fc;}).concat(cp.slice(-200));
            edges();
            parts.forEach(function(p){p.update();p.draw();});
            ring();
            requestAnimationFrame(loop);
          }
          loop();
        })();
        </script></body></html>""",
        height=0,
        scrolling=False,
    )


# ──────────────────────────────────────────────────────────────
#  DASHBOARD BACKGROUND  (unchanged)
# ──────────────────────────────────────────────────────────────
def style_background_dashboard():
    st.markdown(
        """
<style>
.stApp {
    background: #E0E3FF !important;
}
/* Style text/headers for dashboard page to be dark navy for perfect readability */
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    color: #0f172a !important;
}
.stApp p:not(button *), .stApp span:not(button *), .stApp label:not(button *), .stApp div[data-testid="stMarkdownContainer"] p:not(button *) {
    color: #334155 !important;
}

/* Reset column styles in dashboard to prevent them from acting as home-screen cards */
.stApp div[data-testid="stColumn"],
.stApp [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    animation: none !important;
    transform: none !important;
}

/* Overrides for secondary and tertiary buttons in light mode dashboard to ensure legibility */
.stApp button[kind="secondary"], .stApp button[kind="secondary"] * {
  
    border: 1px solid rgba(15, 23, 42, 0.12) !important;
}
.stApp button[kind="secondary"]:hover, .stApp button[kind="secondary"]:hover * {

    S
}
.stApp button[kind="tertiary"], .stApp button[kind="tertiary"] * {
    background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%) !important;
    color: #ffffff !important; 
}
.stApp button[kind="tertiary"]:hover, .stApp button[kind="tertiary"]:hover * {
    background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%) !important;
    color: #b91c1c !important;
}
</style>
""",
        unsafe_allow_html=True
    )


# ──────────────────────────────────────────────────────────────
#  BASE LAYOUT / TYPOGRAPHY
# ──────────────────────────────────────────────────────────────
def style_base_layout():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

/* Hide Streamlit chrome */
MainMenu, footer, header { visibility: hidden; }

.block-container { padding-top:1.5rem !important; }

h1 {
    font-family: 'Climate Crisis', sans-serif !important;
    font-size: 3.5rem !important;
    line-height: 1.1 !important;
    margin-bottom: 0rem !important;
}
h2 {
    font-family: 'Climate Crisis', sans-serif !important;
    font-size: 2rem !important;
    line-height: 0.9 !important;
    margin-bottom: 0rem !important;
}
h3, h4, p { font-family: 'Outfit', sans-serif; }

/* Force button children to inherit color correctly */
button, button * {
    color: #ffffff !important;
}

/* Global Primary Buttons styling */
button, button[kind="primary"] {
    border-radius: 1.5rem !important;
    background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%) !important;
    color: #ffffff !important;
    padding: 10px 22px !important;
    border: none !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25) !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
button:hover, button[kind="primary"]:hover {
    box-shadow: 0 6px 18px rgba(79, 70, 229, 0.45) !important;
    transform: translateY(-2px) scale(1.02) !important;
    background: linear-gradient(135deg, #4338ca 0%, #2563eb 100%) !important;
    color: #ffffff !important;
}

/* Global Secondary Buttons styling */
button[kind="secondary"], button[kind="secondary"] * {
    border-radius: 1.5rem !important;
    color: #ffffff !important;
    
    font-weight: 600 !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
button[kind="secondary"]:hover, button[kind="secondary"]:hover * {
    background-color: rgba(255, 255, 255, 0.15) !important;
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 4px 12px rgba(255, 255, 255, 0.1) !important;
    color: #ffffff !important;
}

/* Global Tertiary Buttons styling */
button[kind="tertiary"], button[kind="tertiary"] * {
    border-radius: 1.5rem !important;
    background-color: rgba(239, 68, 68, 0.1) !important;
    color: #f87171 !important;
    
    font-weight: 600 !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
button[kind="tertiary"]:hover, button[kind="tertiary"]:hover * {
    background-color: rgba(239, 68, 68, 0.2) !important;
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.15) !important;
    color: #fca5a5 !important;
}
</style>
""",
        unsafe_allow_html=True
    )
