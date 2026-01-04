from flask import Blueprint, request, jsonify
from app import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

# ===================== REGISTER =====================
@auth_bp.post("/register")
def register():
    data = request.get_json()

    user_id = str(data.get("user_id")).strip()
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "employee")

    if not user_id or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    if User.query.filter_by(user_id=user_id).first():
        return jsonify({"error": "User ID already exists"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    user = User(
        user_id=user_id,
        email=email,
        role=role,
        is_active=True if role == "admin" else False,
        status="approved" if role == "admin" else "pending"
    )

    user.password_hash = generate_password_hash(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message":
            "Admin registered successfully"
            if role == "admin"
            else "Registration successful. Waiting for admin approval"
    }), 200


# ===================== EMPLOYEE LOGIN =====================
@auth_bp.post("/employee-login")
def employee_login():
    data = request.get_json()

    user_id = str(data.get("user_id")).strip()
    password = data.get("password")

    user = User.query.filter_by(user_id=user_id, role="employee").first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    if not user.is_active:
        return jsonify({"error": "Account pending admin approval"}), 403

    token = create_access_token(
        identity=user.id,
        additional_claims={"role": user.role}
    )

    return jsonify({
        "token": token,
        "role": user.role,
        "user_id": user.user_id
    }), 200


# ===================== ADMIN LOGIN =====================
@auth_bp.post("/login")
def admin_login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email, role="admin").first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid admin credentials"}), 401

    if user.status == "pending":
        return jsonify({"error": "Admin approval pending"}), 403

    if user.status == "rejected":
        return jsonify({"error": "Admin account rejected"}), 403

    token = create_access_token(
        identity=user.id,
        additional_claims={"role": user.role}
    )

    return jsonify({
        "token": token,
        "role": user.role,
        "user_id": user.user_id
    }), 200
