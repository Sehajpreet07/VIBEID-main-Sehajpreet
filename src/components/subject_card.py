import streamlit as st
def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
        <div style="background:white; border-left: 8px solid #4f46e5; padding:25px; border-radius: 20px; border: 1px solid rgba(15,23,42,0.08); box-shadow: 0 4px 20px rgba(0,0,0,0.03); margin-bottom:20px;">
        <h3 style="margin:0; color: #0f172a; font-size: 1.5rem; font-family:'Outfit', sans-serif;">{name}</h3>
        <p style="color:#475569; margin:10px 0; font-family:'Outfit', sans-serif;">Code : <span style="background:rgba(79,70,229,0.08); color:#4f46e5; padding:2px 8px; border-radius:5px; font-weight:600;">{code} </span> | Section : {section}</p>
        
        """
    
    if stats:
        html+= """
        <div style="display:flex; gap:8px; flex-wrap:wrap; margin-bottom: 5px;">
        """
        for icon, label, value in stats:
            html+= f'<div style="background: rgba(79,70,229,0.06); color: #4338ca; padding:6px 14px; border-radius:12px; font-size:0.88rem; font-family:\'Outfit\', sans-serif; font-weight: 500;">{icon} <b>{value}</b> {label} </div>'
        
        html+= "</div>"

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
         footer_callback()
        