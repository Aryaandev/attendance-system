from flask import Blueprint, request, jsonify
from datetime import datetime, date
from app import db
from models import Attendance, LeaveRequest

attendance_bp = Blueprint("attendance", __name__)

# ======================
# CHECK IN
# ======================
@attendance_bp.post("/checkin")
def checkin():
    user_id = request.json.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID required"}), 400

    today = date.today()

    existing = Attendance.query.filter_by(
        user_id=user_id,
        date=today
    ).first()

    if existing:
        return jsonify({"message": "Already checked in today"})

    record = Attendance(
        user_id=user_id,
        date=today,
        check_in=datetime.now(),
        check_out=None
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "Checked in successfully"})


# ======================
# CHECK OUT
# ======================
@attendance_bp.post("/checkout")
def checkout():
    user_id = request.json.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID required"}), 400

    today = date.today()

    record = Attendance.query.filter_by(
        user_id=user_id,
        date=today
    ).first()

    if not record:
        return jsonify({"error": "No check-in found today"}), 400

    if record.check_out:
        return jsonify({"message": "Already checked out"})

    record.check_out = datetime.now()
    db.session.commit()

    return jsonify({"message": "Checked out successfully"})

from sqlalchemy import func

from datetime import date

@attendance_bp.get("/my-attendance")
def my_attendance():
    user_id = request.args.get("user_id")
    month = request.args.get("month")  # YYYY-MM

    if not user_id or not month:
        return jsonify([])

    year, month_num = map(int, month.split("-"))

    start_date = date(year, month_num, 1)
    end_date = (
        date(year + 1, 1, 1)
        if month_num == 12
        else date(year, month_num + 1, 1)
    )

    records = (
        Attendance.query
        .filter(
            Attendance.user_id == int(user_id),
            Attendance.date >= start_date,
            Attendance.date < end_date
        )
        .order_by(Attendance.date)
        .all()
    )

    return jsonify([
        {
            "date": r.date.strftime("%Y-%m-%d"),
            "check_in": str(r.check_in),
            "check_out": str(r.check_out) if r.check_out else "-"
        }
        for r in records
    ])


from datetime import timedelta
from sqlalchemy import func

@attendance_bp.get("/my-summary")
def my_monthly_summary():
    user_id = request.args.get("user_id")
    month = request.args.get("month")  # YYYY-MM

    if not user_id or not month:
        return jsonify({
            "working_days": 0,
            "present_days": 0,
            "percentage": 0
        })

    year, month_num = map(int, month.split("-"))

    start_date = date(year, month_num, 1)
    end_date = (
        date(year + 1, 1, 1)
        if month_num == 12
        else date(year, month_num + 1, 1)
    )

    # 🔹 Calculate working days (Mon–Fri)
    working_days = 0
    current = start_date
    while current < end_date:
        if current.weekday() < 5:
            working_days += 1
        current += timedelta(days=1)

    # 🔹 Present days for this user
    present_days = (
        Attendance.query
        .filter(
            Attendance.user_id == int(user_id),
            Attendance.date >= start_date,
            Attendance.date < end_date
        )
        .count()
    )

    percentage = (
        round((present_days / working_days) * 100, 2)
        if working_days > 0 else 0
    )

    return jsonify({
        "working_days": working_days,
        "present_days": present_days,
        "percentage": percentage
    })

