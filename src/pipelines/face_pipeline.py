import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    detector=dlib.get_frontal_face_detector()



    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec=dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )


    return detector,sp,facerec

from PIL import Image

def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()
    
    # Resize image if it's too large to prevent OOM while allowing upsampling
    img = Image.fromarray(image_np)
    MAX_WIDTH = 1000
    if img.width > MAX_WIDTH:
        ratio = MAX_WIDTH / img.width
        new_height = int(img.height * ratio)
        # Use Image.BILINEAR for compatibility
        img = img.resize((MAX_WIDTH, new_height), Image.BILINEAR)
        
    process_img = np.array(img)

    # Now we can safely use upsample=2 to find small faces in the classroom
    faces = detector(process_img, 2)

    encodings = []

    for face in faces:
        shape = sp(process_img, face)
        face_descriptor = facerec.compute_face_descriptor(process_img, shape, 1)

        encodings.append(np.array(face_descriptor))

    return encodings
@st.cache_resource
def get_trained_model():
    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    # Collect ALL student embeddings first (was broken before — returned inside loop)
    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))

    # Check AFTER the loop, not inside it
    if len(X) == 0:
        return None

    clf = SVC(kernel='linear', probability=True, class_weight='balanced')

    try:
        clf.fit(X, y)
    except ValueError:
        return None

    return {'clf': clf, 'X': X, 'y': y}

def train_classifier():
    """Clear cached model and rebuild it with the latest students from DB."""
    get_trained_model.clear()   # only clears THIS function's cache, not all resources
    model_data = get_trained_model()
    return bool(model_data)


 
    
def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)

    detected_student = {}


    model_data = get_trained_model()

    if not model_data:
        if student_db_empty := (get_all_students() == []):
            st.error("⚠️ Cannot connect to database. Check your internet connection and try again.")
        return detected_student, [], len(encodings)
    
    clf = model_data['clf']
    X_train = model_data['X']
    y_train = model_data['y']

    THRESHOLD = 0.45  # Strict dlib euclidean threshold; 0.6 is too lenient

    all_students = sorted(list(set(y_train)))

    for encoding in encodings:
        # Find the closest known embedding regardless of how many students exist
        best_match_id = None
        best_match_score = float('inf')

        for stored_id, stored_emb in zip(y_train, X_train):
            dist = np.linalg.norm(stored_emb - encoding)
            if dist < best_match_score:
                best_match_score = dist
                best_match_id = stored_id

        # Only accept as known if close enough — otherwise it's a new person
        if best_match_id is not None and best_match_score <= THRESHOLD:
            detected_student[int(best_match_id)] = True

    return detected_student, all_students, len(encodings)

 