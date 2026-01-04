# 📋 Attendance Management System

A full‑stack **Attendance Management System** designed to simplify employee/student attendance tracking with secure authentication, role‑based access, and a clean, responsive UI. This project is suitable for academic submissions, internships, and real‑world deployment demos.

---

## 🚀 Project Overview

The Attendance Management System allows organizations or institutions to:

* Securely log in users (Admin / Employee / Student)
* Mark and manage attendance digitally
* View attendance records in real time
* Store data centrally using a backend database
* Access the system from any device via a responsive interface

This project follows **modern web development practices** and can be deployed on cloud platforms such as **AWS**.

---

## 🛠️ Tech Stack

### Frontend

* HTML5
* CSS3 (Custom + Bootstrap 5)
* JavaScript

### Backend

* Python (Flask)
* REST APIs

### Database

* PostgreSQL (Recommended)
* SQLite (for local testing)

### Tools & Platforms

* Git & GitHub
* VS Code
* AWS (EC2, optional RDS)

---

## ✨ Features

* 🔐 Secure Login & Authentication
* 👨‍💼 Role‑Based Access (Admin / Employee)
* 🕒 Attendance Marking System
* 📊 Attendance Record Viewing
* 🌙 Light / Dark Mode Toggle
* 📱 Fully Responsive UI (Mobile Friendly)
* 🧩 Modular Code Structure
* ☁️ Cloud‑Deployable Architecture

---

## 📂 Project Structure

```
attendance-system/
│
├── backend/
│   ├── app.py
│   ├── routes/
│   ├── models/
│   ├── requirements.txt
│   └── db/
│
├── frontend/
│   ├── login.html
│   ├── dashboard.html
│   ├── css/
│   └── js/
│
├── static/
│   └── style.css
│
├── README.md
└── .gitignore
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Aryaandev/attendance-system.git
cd attendance-system
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4️⃣ Configure Database

* Install PostgreSQL
* Create a database
* Update database credentials in `app.py`

### 5️⃣ Run the Application

```bash
cd backend
flask run
```

Open browser:

```
http://127.0.0.1:5000
```

---

## ☁️ Deployment (AWS – Optional)

* Launch an EC2 instance (Ubuntu)
* Install Python, Git, and PostgreSQL
* Clone the repository
* Use **Gunicorn + Nginx** for production
* Configure security groups (Port 80 / 5000)

This project is suitable for **cloud deployment demonstrations**.

---

## 🧪 Testing

* Manual UI testing
* API endpoint testing using Postman
* Login validation and error handling checks

---

## 📌 Use Cases

* College Mini / Major Project
* Internship Assignments
* HR Attendance System Prototype
* Cloud & DevOps Practice Project

---

## 📈 Future Enhancements

* 📲 Biometric / QR‑based Attendance
* 📊 Analytics Dashboard
* 📧 Email Notifications
* 📱 Progressive Web App (PWA)
* 🔔 Push Notifications

---

## 👨‍💻 Author

**Aryaan Meensan Dev**
GitHub: [https://github.com/Aryaandev](https://github.com/Aryaandev)

---

## 📄 License

This project is licensed under the **MIT License**. You are free to use, modify, and distribute it for learning and development purposes.

---

⭐ If you found this project useful, don’t forget to **star the repository**!
