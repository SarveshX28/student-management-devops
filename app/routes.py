from flask import jsonify, request

from app.services import (
    add_student,
    get_student,
    get_all_students,
    add_course,
    enroll_student,
    add_marks,
    calculate_gpa
)


def register_routes(app):

    @app.route("/")
    def home():
        return jsonify({
            "application": "Enterprise Student Record & Academic Management Platform",
            "status": "running",
            "version": "1.0.0"
        })

    @app.route("/health")
    def health():
        return jsonify({
            "status": "healthy"
        })

    @app.route("/students", methods=["POST"])
    def create_student():
        data = request.get_json()

        try:
            student = add_student(
                data["id"],
                data["name"],
                data["email"]
            )

            return jsonify(student), 201

        except ValueError as error:
            return jsonify({"error": str(error)}), 400

    @app.route("/students", methods=["GET"])
    def students():
        return jsonify(get_all_students())

    @app.route("/students/<student_id>", methods=["GET"])
    def student(student_id):
        result = get_student(student_id)

        if result is None:
            return jsonify({"error": "Student not found"}), 404

        return jsonify(result)

    @app.route("/courses", methods=["POST"])
    def create_course():
        data = request.get_json()

        try:
            course = add_course(
                data["id"],
                data["name"],
                data["credits"]
            )

            return jsonify(course), 201

        except ValueError as error:
            return jsonify({"error": str(error)}), 400

    @app.route("/enrollments", methods=["POST"])
    def create_enrollment():
        data = request.get_json()

        try:
            enrollment = enroll_student(
                data["student_id"],
                data["course_id"]
            )

            return jsonify(enrollment), 201

        except ValueError as error:
            return jsonify({"error": str(error)}), 400

    @app.route("/marks", methods=["POST"])
    def create_marks():
        data = request.get_json()

        try:
            result = add_marks(
                data["student_id"],
                data["course_id"],
                data["marks"]
            )

            return jsonify({
                "student_id": data["student_id"],
                "course_id": data["course_id"],
                "marks": result
            }), 201

        except ValueError as error:
            return jsonify({"error": str(error)}), 400

    @app.route("/students/<student_id>/gpa", methods=["GET"])
    def student_gpa(student_id):
        if get_student(student_id) is None:
            return jsonify({"error": "Student not found"}), 404

        return jsonify({
            "student_id": student_id,
            "gpa": calculate_gpa(student_id)
        })
