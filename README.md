# Dayflow – Human Resource Management System

A comprehensive **Human Resource Management System (HRMS)** built using **Python Flask** and **MySQL**, designed for managing employees, attendance, leave workflows, and payroll in a single integrated platform.

---

## Quick Start

### Installation

```bash
git clone <repository-url>
cd Dayflow-Human-Resource-Management-System
pip install -r requirements.txt
python migrate_database.py
python app.py
```

---

## Default Login Credentials

**Admin**
Username: `DTAD20241001`
Password: `admin123`

**Employee**
Username: `DTEM20241001`
Password: `emp123`

---

## Features

### Employee Management

* Detailed employee profiles including personal information, skills, and certifications
* Role-based access control

  * Admin users can manage all employee records
  * Employees can view and update their own profiles
* Profile photo uploads and document storage

### Attendance System

* Real-time check-in and check-out
* Live attendance status tracking (Present, Absent, On Leave)
* Attendance reports and analytics

### Leave Management

* Leave application and approval workflow
* Multiple leave types such as Paid, Sick, and Unpaid
* Automated leave balance tracking

### Payroll System

* Salary structure and component management
* Automatic payroll calculation with deductions
* Salary reports and payroll analytics dashboard

### Reports and Analytics

* Employee, attendance, leave, and payroll reports
* CSV export functionality
* Custom date range filtering

---

## Tech Stack

<table>
<tr>
<td><strong>Backend</strong></td>
<td>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="20"/> Python  
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" width="20"/> Flask  
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlalchemy/sqlalchemy-original.svg" width="20"/> SQLAlchemy
</td>
</tr>
<tr>
<td><strong>Database</strong></td>
<td>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg" width="20"/> MySQL
</td>
</tr>
<tr>
<td><strong>Frontend</strong></td>
<td>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-original.svg" width="20"/> Bootstrap 5  
<img src="https://upload.wikimedia.org/wikipedia/commons/5/5f/Font_Awesome_logomark_blue.svg" width="20"/> Font Awesome 6.4.0
</td>
</tr>
<tr>
<td><strong>Theme</strong></td>
<td>Minimal Black and White UI</td>
</tr>
</table>

---

## Project Structure

* `app.py` – Main application entry point
* `migrate_database.py` – Database initialization and migrations
* `templates/` – HTML templates
* `.env` – Environment configuration
* `.env.example` – Sample environment file

---

## Configuration

Copy the example environment file and update it with your database credentials:

```bash
cp .env.example .env
```

---

## License

This project is developed as an **educational and demonstration project** for the **Odoo Hackathon**.
