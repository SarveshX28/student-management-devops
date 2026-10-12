students = {}
courses = {}
faculty = {}
enrollments = []
marks = {}


def add_student(student_id, name, email):
    if student_id in students:
        raise ValueError("Student already exists")

    students[student_id] = {
        "id": student_id,
        "name": name,
        "email": email
    }

    return students[student_id]


def get_student(student_id):
    return students.get(student_id)


def get_all_students():
    return list(students.values())


def add_course(course_id, name, credits):
    if course_id in courses:
        raise ValueError("Course already exists")

    courses[course_id] = {
        "id": course_id,
        "name": name,
        "credits": credits
    }

    return courses[course_id]


def enroll_student(student_id, course_id):
    if student_id not in students:
        raise ValueError("Student not found")

    if course_id not in courses:
        raise ValueError("Course not found")

    enrollment = {
        "student_id": student_id,
        "course_id": course_id
    }

    enrollments.append(enrollment)

    return enrollment


def add_marks(student_id, course_id, marks_value):
    if student_id not in students:
        raise ValueError("Student not found")

    if course_id not in courses:
        raise ValueError("Course not found")

    if not 0 <= marks_value <= 100:
        raise ValueError("Marks must be between 0 and 100")

    marks[(student_id, course_id)] = marks_value

    return marks_value


def calculate_gpa(student_id):
    student_marks = [
        value
        for (sid, _), value in marks.items()
        if sid == student_id
    ]

    if not student_marks:
        return 0.0

    total = sum(student_marks)
    average = total / len(student_marks)

    # Simple academic GPA conversion
    gpa = (average / 100) * 10

    return round(gpa, 2)
