from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

from config import Config
from models import db, Teacher, Student, Attendance
from messaging import send_attendance_sms

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return Teacher.query.get(int(user_id))

    @app.before_first_request
    def create_tables():
        db.create_all()
        if Teacher.query.first() is None:
            t = Teacher(
                username="admin",
                password_hash=generate_password_hash("admin123")
            )
            db.session.add(t)
            db.session.commit()

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))
        return redirect(url_for("login"))

    # ---------- Login ----------
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            teacher = Teacher.query.filter_by(username=username).first()
            if teacher and check_password_hash(teacher.password_hash, password):
                login_user(teacher)
                return redirect(url_for("dashboard"))
            flash("Invalid username or password")
        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))

    # ---------- Dashboard ----------
    @app.route("/dashboard")
    @login_required
    def dashboard():
        classes = db.session.query(Student.class_name).distinct().all()
        classes = [c[0] for c in classes]
        current_date = date.today().strftime("%Y-%m-%d")
        return render_template("dashboard.html", classes=classes, current_date=current_date)

    # ---------- Attendance ----------
    @app.route("/attendance", methods=["GET", "POST"])
    @login_required
    def attendance():
        class_name = request.args.get("class") if request.method == "GET" else request.form.get("class_name")
        students = Student.query.filter_by(class_name=class_name).all() if class_name else []
        today = date.today().strftime("%Y-%m-%d")

        if request.method == "POST":
            attendance_date = date.today()
            present_ids = request.form.getlist("present")

            for student in students:
                existing = Attendance.query.filter_by(
                    student_id=student.id,
                    date=attendance_date
                ).first()
                if existing:
                    continue

                status = "Present" if str(student.id) in present_ids else "Absent"
                record = Attendance(
                    student_id=student.id,
                    date=attendance_date,
                    status=status
                )
                db.session.add(record)
                db.session.commit()

                if status == "Present":
                    send_attendance_sms(
                        student_name=student.name,
                        parent_phone=student.parent_phone,
                        date_str=attendance_date.strftime("%Y-%m-%d"),
                        center_name="Learning Center"
                    )

            flash("Attendance saved and notifications sent.")
            return redirect(url_for("dashboard"))

        return render_template("attendance.html", students=students, class_name=class_name, today=today)

    # ---------- Students Management (CRUD) ----------
    @app.route("/students")
    @login_required
    def students_page():
        students = Student.query.order_by(Student.class_name, Student.name).all()
        return render_template("students.html", students=students)

    @app.route("/students/add", methods=["POST"])
    @login_required
    def add_student():
        name = request.form.get("name")
        parent_phone = request.form.get("parent_phone")
        class_name = request.form.get("class_name")
        if not (name and parent_phone and class_name):
            flash("All fields are required.")
            return redirect(url_for("students_page"))

        s = Student(name=name, parent_phone=parent_phone, class_name=class_name)
        db.session.add(s)
        db.session.commit()
        flash("Student added successfully.")
        return redirect(url_for("students_page"))

    @app.route("/students/update/<int:student_id>", methods=["POST"])
    @login_required
    def update_student(student_id):
        student = Student.query.get_or_404(student_id)
        student.name = request.form.get("name")
        student.parent_phone = request.form.get("parent_phone")
        student.class_name = request.form.get("class_name")
        db.session.commit()
        flash("Student updated successfully.")
        return redirect(url_for("students_page"))

    @app.route("/students/delete/<int:student_id>", methods=["POST"])
    @login_required
    def delete_student(student_id):
        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        flash("Student deleted successfully.")
        return redirect(url_for("students_page"))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
