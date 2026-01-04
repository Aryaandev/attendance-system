from app import create_app, db
from models import Attendance
from datetime import date, datetime, timedelta

app = create_app()

with app.app_context():
    # Clear existing attendance
    Attendance.query.delete()

    today = date.today()

    records = [
        Attendance(
            user_id=1,
            date=today - timedelta(days=2),
            check_in=datetime.now() - timedelta(days=2, hours=8),
            check_out=datetime.now() - timedelta(days=2, hours=1),
        ),
        Attendance(
            user_id=1,
            date=today - timedelta(days=1),
            check_in=datetime.now() - timedelta(days=1, hours=8),
            check_out=datetime.now() - timedelta(days=1, hours=1),
        ),
        Attendance(
            user_id=1,
            date=today,
            check_in=datetime.now() - timedelta(hours=8),
            check_out=None,
        ),
    ]

    db.session.add_all(records)
    db.session.commit()

    print("✅ Dummy attendance data inserted successfully")
