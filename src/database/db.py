from src.database.config import supabase
import bcrypt
from postgrest.exceptions import APIError


def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


def check_teacher_exists(username):
    # Check for unique username, returns false when username is already taken
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0 


def create_teacher(username, password, name):
    data = { "username" : username, "password": hash_pass(password), "name": name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username, password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):
            return teacher
    return None


def get_all_students():
    response = supabase.table('students').select("*").execute()
    return response.data


def create_student(new_name, face_embedding=None, voice_embedding=None):
    # Convert NumPy arrays to standard Python lists so Supabase can parse them as JSON
    if hasattr(face_embedding, 'tolist'):
        face_embedding = face_embedding.tolist()
        
    if hasattr(voice_embedding, 'tolist'):
        voice_embedding = voice_embedding.tolist()

    data = {
        'name': new_name, 
        'face_embedding': face_embedding, 
        "voice_embedding": voice_embedding
    }
    
    # Try inserting and catch APIError to reveal hidden details in Streamlit Cloud logs
    try:
        response = supabase.table('students').insert(data).execute()
        return response.data
    except APIError as e:
        print(f"\n--- SUPABASE INSERT ERROR ---")
        print(f"Message: {e.message}")
        print(f"Details: {e.details}")
        print(f"Hint: {getattr(e, 'hint', 'None')}")
        print(f"-----------------------------\n")
        raise e


def create_subject(subject_code, name, section, teacher_id):
    data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
    response = supabase.table("subjects").insert(data).execute()
    return response.data


def get_teacher_subjects(teacher_id):
    response = supabase.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects = response.data

    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance_logs', [])
        unique_sessions = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_sessions

        sub.pop('subject_student', None)
        sub.pop('attendance_logs', None)

    return subjects


def enroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, "subject_id": subject_id}
    response = supabase.table('subject_students').insert(data).execute()
    return response.data


def unenroll_student_to_subject(student_id, subject_id):
    response = supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
    return response.data


def get_student_subjects(student_id):
    response = supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data


def get_student_attendance(student_id):
    response = supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data


def create_attendance(logs):
    response = supabase.table('attendance_logs').insert(logs).execute()
    return response.data


def get_attendance_for_teacher(teacher_id):
    # Added , students(*) to the select statement
    response = supabase.table('attendance_logs').select("*, subjects!inner(*), students(*)").eq('subjects.teacher_id', teacher_id).execute()
    return response.data


def get_subject_students(subject_id):
    result = (
        supabase.table("subject_students")
        .select("students(name)")
        .eq("subject_id", subject_id)
        .execute()
    )

    students = []

    for row in result.data:
        if row.get("students"):
            students.append(row["students"])

    return students


def calculate_particular_student_attendance(student_id, teacher_id=None):
    """
    Calculates attendance statistics and details for a particular student.
    If teacher_id is provided, filters for subjects belonging to that teacher.
    """
    query = supabase.table('attendance_logs').select('*, subjects!inner(*), students(*)').eq('student_id', student_id)
    if teacher_id:
        query = query.eq('subjects.teacher_id', teacher_id)
    
    response = query.execute()
    logs = response.data if response.data else []
    
    total_classes = len(logs)
    present_count = sum(1 for log in logs if log.get('is_present'))
    absent_count = total_classes - present_count
    percentage = round((present_count / total_classes * 100), 2) if total_classes > 0 else 0.0
    
    subject_map = {}
    detailed_logs = []
    
    for log in logs:
        sub = log.get('subjects', {}) or {}
        sub_id = sub.get('subject_id')
        sub_name = sub.get('name', 'Unknown Subject')
        sub_code = sub.get('subject_code', 'N/A')
        is_present = bool(log.get('is_present', False))
        ts = log.get('timestamp')
        
        if sub_id not in subject_map:
            subject_map[sub_id] = {
                'subject_id': sub_id,
                'name': sub_name,
                'code': sub_code,
                'total': 0,
                'present': 0,
                'absent': 0
            }
            
        subject_map[sub_id]['total'] += 1
        if is_present:
            subject_map[sub_id]['present'] += 1
        else:
            subject_map[sub_id]['absent'] += 1
            
        detailed_logs.append({
            'timestamp': ts,
            'subject_name': sub_name,
            'subject_code': sub_code,
            'is_present': is_present
        })
        
    subject_breakdown = []
    for s in subject_map.values():
        s_pct = round((s['present'] / s['total'] * 100), 2) if s['total'] > 0 else 0.0
        subject_breakdown.append({
            'Subject Code': s['code'],
            'Subject Name': s['name'],
            'Total Classes': s['total'],
            'Present': s['present'],
            'Absent': s['absent'],
            'Attendance (%)': f"{s_pct}%",
            'raw_pct': s_pct
        })
        
    return {
        'student_id': student_id,
        'total_classes': total_classes,
        'present_count': present_count,
        'absent_count': absent_count,
        'percentage': percentage,
        'subject_breakdown': subject_breakdown,
        'detailed_logs': detailed_logs
    }

