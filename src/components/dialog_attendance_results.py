import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
import time


from src.database.db import create_attendance

# def show_attendance_result(df, logs):
#     st.write('Please review attendance before confirming.')
#     st.dataframe(df, hide_index=True, width='stretch')

#     col1, col2 = st.columns(2)

#     with col1:
#         if st.button('Discard', width='stretch'):
#             st.session_state.voice_attendance_results = None
#             st.session_state.attendance_images = []
#             st.rerun()

#     with col2:
#         if st.button('Confirm & Save', width='stretch', type='primary'):
#             try:
#                 create_attendance(logs)
#                 st.toast("Attendance taken")
#                 st.session_state.attendance_images = []
#                 st.session_state.voice_attendance_results = None
#                 st.rerun()
#             except Exception as e:
#                 st.error('Sync failed!')


def show_attendance_result(df, logs):
    # 1. Force the 'Source' column to strings so st.dataframe never has a type conflict
    if 'Source' in df.columns:
        df['Source'] = df['Source'].fillna('-').astype(str)
        
    st.write('Please review attendance before confirming.')
    st.dataframe(df, hide_index=True, width='stretch')
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button('Discard', use_container_width=True):
            st.session_state.voice_attendance_results = None
            st.session_state.attendance_images = []
            st.rerun()
            
    with col2:
        if st.button('Confirm & Save', use_container_width=True, type='primary'):
            try:
                # 2. Sanitize database logs to ensure clean data formatting types
                sanitized_logs = []
                for log in logs:
                    sanitized_logs.append({
                        'student_id': int(log['student_id']),
                        'subject_id': str(log['subject_id']),
                        'timestamp': str(log['timestamp']),
                        'is_present': bool(log['is_present'])
                    })
                
                # Send the clean data to your Supabase engine
                create_attendance(sanitized_logs)
                st.toast("Attendance taken")
                st.session_state.attendance_images = []
                st.session_state.voice_attendance_results = None
                st.rerun()
            except Exception as e:
                # Displays the actual system error so we know EXACTLY what Supabase disliked
                st.error(f"Sync failed! Database Error: {e}")
@st.dialog("Attendance Reports")
def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)