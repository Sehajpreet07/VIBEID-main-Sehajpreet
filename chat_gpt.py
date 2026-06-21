import streamlit as st
import numpy as np
from PIL import Image
import time

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.snapheader import header_dashboard
from src.components.footer import footer_dashboard
from src.pipelines.face_pipeline import get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student


def student_dashboard():
    st.header('🎓 Student Dashboard')
    # Add your dashboard content here later


def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    # Header
    c1, c2 = st.columns(2, vertical_alignment='center', gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace", use_container_width=True):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Login With your Face ID")
    st.markdown("### Position your face in the center")

    photo_source = st.camera_input("Take Photo", key="face_login")

    show_registration = False

    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner('🔍 AI is scanning your face...'):
            current_encodings = get_face_embeddings(img)

            if not current_encodings or len(current_encodings) == 0:
                st.warning('⚠️ Face not detected! Please try again.')
                return

            current_embedding = current_encodings[0]

            # === Direct Embedding Comparison (Most Reliable) ===
            all_students = get_all_students()
            best_match = None
            best_similarity = -1.0

            for student in all_students:
                stored = student.get('face_embedding')
                if not stored:
                    continue
                
                stored_emb = np.array(stored)
                # Cosine Similarity
                similarity = np.dot(current_embedding, stored_emb) / (
                    np.linalg.norm(current_embedding) * np.linalg.norm(stored_emb)
                )

                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = student

            if best_match and best_similarity > 0.68:        # ← Adjust this threshold if needed
                st.success(f"✅ Face Recognized! Welcome {best_match['name']}")
                st.session_state.is_logged_in = True
                st.session_state.user_role = 'student'
                st.session_state.student_data = best_match
                time.sleep(1)
                st.rerun()
            else:
                st.info('👤 Face not recognized! You might be a new student.')
                show_registration = True

    # ==================== REGISTRATION ====================
    if show_registration and photo_source:
        with st.container(border=True):
            st.header("Register New Profile")
            new_name = st.text_input("Enter your name", placeholder="E.g. SEHAJUUUU")

            st.subheader("Optional: Voice Enrollment")
            audio_data = st.audio_input('Record a short phrase (e.g. "I am present")')

            if st.button('Create Account', type='primary', use_container_width=True):
                if not new_name:
                    st.warning('Please enter your name!')
                    return

                with st.spinner('Creating your profile...'):
                    encodings = get_face_embeddings(img)
                    if not encodings:
                        st.error("Couldn't extract facial features. Try better lighting.")
                        return

                    face_emb = encodings[0].tolist()

                    voice_emb = None
                    if audio_data:
                        try:
                            voice_emb = get_voice_embedding(audio_data.read())
                        except:
                            voice_emb = None

                    response = create_student(
                        name=new_name, 
                        face_embedding=face_emb, 
                        voice_embedding=voice_emb
                    )

                    if response and len(response) > 0:
                        train_classifier()   # Retrain after new student
                        st.success(f"🎉 Profile Created! Welcome {new_name}")
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = response[0]
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error("Failed to create account. Try again.")

    footer_dashboard()
