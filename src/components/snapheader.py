# import streamlit as st
# def show_header():
#       logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    
#       st.markdown(f"""
#         <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:30px; margin-top:30px">
#             <img src='{logo_url}' style='height:100px;' />
#             <h1 style='text-align:center; color:#E0E3FF'>SNAP<br/>CLASS</h1>
#         </div>   
                
#                 """, unsafe_allow_html=True)
      

# def header_dashboard():
#      logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    
#      st.markdown(f"""
#         <div style="display:flex; align-items:center; justify-content:center; gap:10px">
#             <img src='{logo_url}' style='height:85px;' />
#             <h2 style='text-align:left; color:#5865F2'>SNAP<br/>CLASS</h1>
#         </div>   
                
#                 """, unsafe_allow_html=True)

import streamlit as st

def show_header():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    st.markdown(f"""
<style>
@keyframes pulsRing {{
    0%   {{ transform: scale(1);   opacity: 0.7; }}
    70%  {{ transform: scale(1.7); opacity: 0;   }}
    100% {{ transform: scale(1.7); opacity: 0;   }}
}}
@keyframes shimmerTitle {{
    0%   {{ background-position: -200% center; }}
    100% {{ background-position:  200% center; }}
}}
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(24px); }}
    to   {{ opacity: 1; transform: translateY(0);    }}
}}
@keyframes badgePop {{
    0%   {{ opacity: 0; transform: scale(0.7) translateY(10px); }}
    100% {{ opacity: 1; transform: scale(1)   translateY(0);    }}
}}

.hero-wrapper {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 1rem 1.5rem;
    text-align: center;
    animation: fadeUp 0.9s ease both;
}}

/* Pulse ring behind logo */
.logo-ring-wrap {{
    position: relative;
    width: 140px;
    height: 140px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
}}
.pulse-ring {{
    position: absolute;
    width: 140px;
    height: 140px;
    border-radius: 50%;
    border: 2px solid #6366f1;
    animation: pulsRing 2.4s ease-out infinite;
}}
.pulse-ring:nth-child(2) {{ animation-delay: 0.8s;  border-color: #38bdf8; }}
.pulse-ring:nth-child(3) {{ animation-delay: 1.6s;  border-color: #a5b4fc; }}
.hero-logo {{
    position: relative;
    height: 110px;
    filter: drop-shadow(0 0 20px rgba(99, 102, 241, 0.6)) drop-shadow(0 0 40px rgba(56, 189, 248, 0.45));
    z-index: 1;
}}

/* Gradient shimmer title */
.hero-title {{
    font-family: 'Climate Crisis', sans-serif;
    font-size: 4.2rem;
    font-weight: 900;
    letter-spacing: 8px;
    background: linear-gradient(90deg, #ffffff, #a5b4fc, #38bdf8, #818cf8, #ffffff);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmerTitle 4s linear infinite;
    margin: 0 0 0.4rem;
    text-shadow: none;
}}

.hero-subtitle {{
    font-family: 'Outfit', sans-serif;
    font-size: 1.1rem;
    color: #a5b4fc;
    font-style: italic;
    margin: 0 0 1.8rem;
    letter-spacing: 0.5px;
    animation: fadeUp 1.1s 0.3s ease both;
    opacity: 0;
    animation-fill-mode: forwards;
}}

/* Floating feature badges */
.badge-row {{
    display: flex;
    gap: 0.8rem;
    flex-wrap: wrap;
    justify-content: center;
    margin-bottom: 0.5rem;
}}
.feature-badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.4rem 1rem;
    border-radius: 2rem;
    font-family: 'Outfit', sans-serif;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.3px;
    border: 1px solid rgba(99, 102, 241, 0.3);
    background: rgba(99, 102, 241, 0.08);
    backdrop-filter: blur(10px);
    color: #e0e7ff;
    animation: badgePop 0.6s ease both;
    opacity: 0;
    animation-fill-mode: forwards;
}}
.feature-badge.b1 {{ animation-delay:0.5s; border-color:rgba(99,102,241,0.45); box-shadow:0 0 12px rgba(99,102,241,0.2); }}
.feature-badge.b2 {{ animation-delay:0.7s; border-color:rgba(56,189,248,0.45); box-shadow:0 0 12px rgba(56,189,248,0.25); }}
.feature-badge.b3 {{ animation-delay:0.9s; border-color:rgba(168,85,247,0.45); box-shadow:0 0 12px rgba(168,85,247,0.2); }}

.hero-divider {{
    width: 80px;
    height: 3px;
    background: linear-gradient(90deg, #6366f1, #38bdf8);
    border-radius: 2px;
    margin: 1.2rem auto 0.5rem;
    animation: fadeUp 1s 1s ease both;
    opacity: 0;
    animation-fill-mode: forwards;
}}

.portal-label {{
    font-family: 'Outfit', sans-serif;
    font-size: 0.95rem;
    color: #818cf8;
    letter-spacing: 2px;
    text-transform: uppercase;
    animation: fadeUp 1s 1.1s ease both;
    opacity: 0;
    animation-fill-mode: forwards;
    margin-bottom: 0.2rem;
}}
</style>
""", unsafe_allow_html=True)

    st.markdown(f"""<div class="hero-wrapper"><div class="logo-ring-wrap"><div class="pulse-ring"></div><div class="pulse-ring"></div><div class="pulse-ring"></div><img class="hero-logo" src="{logo_url}" /></div><h1 class="hero-title">VIBE ID</h1><p class="hero-subtitle">AI-Powered Attendance &amp; Class Management</p><div class="badge-row"><span class="feature-badge b1">🧠 Face Recognition</span><span class="feature-badge b2">⚡ AI Powered</span><span class="feature-badge b3">📸 Instant Attendance</span></div><div class="hero-divider"></div><p class="portal-label">Choose your portal below</p></div>""", unsafe_allow_html=True)

def header_dashboard():
    # Smaller version for the internal teacher/student dashboards
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    
    st.markdown(f"""
    <div style="display:flex; align-items:center; justify-content:flex-start; gap:15px; margin-bottom:20px;">
        <img src='{logo_url}' style='height:60px; filter: drop-shadow(0px 0px 4px #228BE6);' />
        <h2 style='text-align:left; color:#5865F2; font-family:sans-serif; margin:0;'>VIBE ID</h2>
    </div>
    """, unsafe_allow_html=True)