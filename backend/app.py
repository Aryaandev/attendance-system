from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from settings import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # JWT (kept for learning/demo, not enforced everywhere)
    app.config["JWT_SECRET_KEY"] = "super-secret-jwt-key"
    JWTManager(app)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # 🔹 Import models so migrations & queries work
    from models import User, Attendance, LeaveRequest

    # 🔹 Register Blueprints (APIs)
    from routes.auth import auth_bp
    from routes.attendance import attendance_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(attendance_bp, url_prefix="/api/attendance")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    # =========================
    # PAGE ROUTES (HTML)
    # =========================

    @app.route("/")
    def home():
        return "Attendance System Backend is Running 🚀"

    @app.route("/login")
    def login_page():
        return render_template("login.html")

    @app.route("/register")
    def register_page():
        return render_template("register.html")

    @app.route("/dashboard")
    def dashboard_page():
        return render_template("dashboard.html")

    @app.route("/admin")
    def admin_page():
        return render_template("admin.html")

    @app.route("/chart")
    def chart_page():
        return render_template("chart.html")

    # ✅ STEP 3 — EMPLOYEE SELF-VIEW ATTENDANCE PAGE
    @app.route("/my-attendance")
    def my_attendance_page():
        return render_template("my_attendance.html")
    
    @app.route("/employee-login")
    def employee_login_page():
        return render_template("employee_login.html")
    
    @app.route("/forgot-password")
    def forgot_password_page():
        return render_template("forgot_password.html")
    
    @app.route("/admin-register")
    def admin_register_page():
        return render_template("admin_register.html")
    
    @app.route("/employee-register")
    def employee_register_page():
        return render_template("employee_register.html")

    return app
