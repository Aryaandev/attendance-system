from flask import Blueprint, jsonify, request
from sqlalchemy import func
from datetime import date

from app import db
from models import Attendance, LeaveRequest, User

admin_bp = Blueprint("admin", __name__)

# =========================
# GET ALL ATTENDANCE RECORDS
# =========================
@admin_bp.get("/records")
def get_all_records():
    records = Attendance.query.all()
    return jsonify([
        {
            "user_id": r.user_id,
            "date": r.date.strftime("%Y-%m-%d"),
            "check_in": str(r.check_in),
            "check_out": str(r.check_out)
        }
        for r in records
    ])

# =========================
# MONTHLY ATTENDANCE STATS
# =========================
from datetime import date, timedelta

@admin_bp.get("/monthly-stats")
def monthly_stats():
    month = request.args.get("month")      # YYYY-MM
    user_id = request.args.get("user_id")  # optional

    if not month:
        return jsonify({
            "labels": [],
            "counts": [],
            "total": 0,
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
        if current.weekday() < 5:  # Mon–Fri
            working_days += 1
        current += timedelta(days=1)

    query = db.session.query(
        Attendance.date,
        func.count(Attendance.id)
    ).filter(
        Attendance.date >= start_date,
        Attendance.date < end_date
    )

    if user_id:
        query = query.filter(Attendance.user_id == int(user_id))

    stats = (
        query
        .group_by(Attendance.date)
        .order_by(Attendance.date)
        .all()
    )

    present_days = len(stats)

    attendance_percentage = (
        round((present_days / working_days) * 100, 2)
        if working_days > 0 else 0
    )

    return jsonify({
    "labels": [str(d[0]) for d in stats],
    "counts": [d[1] for d in stats],
    "total_present": present_days,
    "total_working": working_days,
    "percentage": attendance_percentage
})



# =========================
# LEAVE REQUESTS
# =========================
@admin_bp.get("/leaves")
def get_leaves():
    leaves = LeaveRequest.query.all()
    return jsonify([
        {
            "id": l.id,
            "user_id": l.user_id,
            "start_date": str(l.start_date),
            "end_date": str(l.end_date),
            "reason": l.reason,
            "status": l.status
        }
        for l in leaves
    ])
    
@admin_bp.get("/pending-users")
def pending_users():
    users = User.query.filter_by(status="pending").all()
    return jsonify([
        {
            "id": u.id,
            "user_id": u.user_id,
            "email": u.email
        } for u in users
    ])

    
@admin_bp.post("/approve-user/<int:user_id>")
def approve_user(user_id):
    user = User.query.get(user_id)
    user.is_active = True
    user.status = "approved"
    db.session.commit()
    return jsonify({"message": "User approved"})

@admin_bp.post("/reject-user/<int:user_id>")
def reject_user(user_id):
    user = User.query.get(user_id)
    user.status = "rejected"
    user.is_active = False
    db.session.commit()
    return jsonify({"message": "User rejected"})

