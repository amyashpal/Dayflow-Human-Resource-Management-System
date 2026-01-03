from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, date, timedelta
import os
from dotenv import load_dotenv
import secrets
import string

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:password@localhost/dayflow_hrms')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Database Models
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    logo = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    employees = db.relationship('User', backref='company', lazy=True)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15))
    role = db.Column(db.String(20), nullable=False, default='employee')  # 'admin', 'hr', 'employee'
    department = db.Column(db.String(50))
    position = db.Column(db.String(50))
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    profile_picture = db.Column(db.String(200))
    date_joined = db.Column(db.Date, default=date.today)
    is_active = db.Column(db.Boolean, default=True)
    must_change_password = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Additional profile fields
    location = db.Column(db.String(100))
    about = db.Column(db.Text)
    job_motivation = db.Column(db.Text)
    interests_hobbies = db.Column(db.Text)
    
    # Relationships
    manager = db.relationship('User', remote_side=[id], backref='subordinates')
    attendance_records = db.relationship('Attendance', backref='employee', lazy=True)
    leave_requests = db.relationship('LeaveRequest', foreign_keys='LeaveRequest.employee_id', backref='employee', lazy=True)
    salary_info = db.relationship('SalaryInfo', backref='employee', uselist=False)
    profile_details = db.relationship('ProfileDetails', backref='user', uselist=False)
    skills = db.relationship('UserSkill', backref='user', lazy=True)
    certifications = db.relationship('UserCertification', backref='user', lazy=True)

class ProfileDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Private Information
    date_of_birth = db.Column(db.Date)
    residential_address = db.Column(db.Text)
    nationality = db.Column(db.String(50))
    personal_email = db.Column(db.String(120))
    gender = db.Column(db.String(10))
    marital_status = db.Column(db.String(20))
    
    # Bank Information
    account_number = db.Column(db.String(20))
    bank_name = db.Column(db.String(100))
    ifsc_code = db.Column(db.String(15))
    pan_number = db.Column(db.String(15))
    uan_number = db.Column(db.String(15))
    employee_code = db.Column(db.String(20))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    proficiency_level = db.Column(db.String(20))  # 'Beginner', 'Intermediate', 'Advanced', 'Expert'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserCertification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    certification_name = db.Column(db.String(200), nullable=False)
    issuing_organization = db.Column(db.String(200))
    issue_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)
    credential_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    check_in = db.Column(db.DateTime)
    check_out = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='absent')  # 'present', 'absent', 'half_day', 'leave'
    hours_worked = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LeaveRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    leave_type = db.Column(db.String(20), nullable=False)  # 'paid', 'sick', 'unpaid'
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.String(10), nullable=False)  # 'full_day', 'half_day'
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'approved', 'rejected'
    approved_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    approved_at = db.Column(db.DateTime)
    admin_comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    approver = db.relationship('User', foreign_keys=[approved_by])

class SalaryInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    basic_salary = db.Column(db.Float, nullable=False)
    hra = db.Column(db.Float, default=0.0)
    standard_allowance = db.Column(db.Float, default=0.0)
    performance_bonus = db.Column(db.Float, default=0.0)
    lta = db.Column(db.Float, default=0.0)
    fixed_allowance = db.Column(db.Float, default=0.0)
    pf_employee = db.Column(db.Float, default=0.0)
    pf_employer = db.Column(db.Float, default=0.0)
    professional_tax = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def generate_login_id(company_code, first_name, last_name, year):
    """Generate login ID in format: [Company Code][Employee Initials][Year][Serial Number]"""
    initials = (first_name[:2] + last_name[:2]).upper()
    
    # Find the next serial number for this year
    existing_count = User.query.filter(
        User.login_id.like(f'{company_code}{initials}{year}%')
    ).count()
    
    serial_number = str(existing_count + 1).zfill(4)
    return f'{company_code}{initials}{year}{serial_number}'

def generate_random_password(length=8):
    """Generate a random password"""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_id = request.form['login_id']
        password = request.form['password']
        
        user = User.query.filter_by(login_id=login_id).first()
        
        if user and check_password_hash(user.password_hash, password):
            if user.is_active:
                login_user(user)
                if user.must_change_password:
                    return redirect(url_for('change_password'))
                return redirect(url_for('dashboard'))
            else:
                flash('Account is deactivated. Contact HR.', 'error')
        else:
            flash('Invalid login credentials', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    # Only admin/HR can register new employees
    if current_user.role not in ['admin', 'hr']:
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        # Only admin/HR can register new employees
        company_name = request.form['company_name']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        role = request.form.get('role', 'employee')
        
        # Check if company exists or create new one
        company = Company.query.filter_by(name=company_name).first()
        if not company:
            company_code = company_name[:2].upper()
            company = Company(name=company_name, code=company_code)
            db.session.add(company)
            db.session.flush()
        
        # Generate login ID and password
        year = str(datetime.now().year)
        login_id = generate_login_id(company.code, first_name, last_name, year)
        temp_password = generate_random_password()
        
        # Create user
        user = User(
            login_id=login_id,
            email=email,
            password_hash=generate_password_hash(temp_password),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=role,
            company_id=company.id,
            must_change_password=True
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Employee created successfully! Login ID: {login_id}, Temporary Password: {temp_password}', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if not check_password_hash(current_user.password_hash, current_password):
            flash('Current password is incorrect', 'error')
        elif new_password != confirm_password:
            flash('New passwords do not match', 'error')
        elif len(new_password) < 6:
            flash('Password must be at least 6 characters long', 'error')
        else:
            current_user.password_hash = generate_password_hash(new_password)
            current_user.must_change_password = False
            db.session.commit()
            flash('Password changed successfully', 'success')
            return redirect(url_for('dashboard'))
    
    return render_template('change_password.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role in ['admin', 'hr']:
        employees = User.query.filter_by(company_id=current_user.company_id).all()
        # Get attendance status for each employee
        today = date.today()
        for employee in employees:
            attendance = Attendance.query.filter_by(
                employee_id=employee.id, 
                date=today
            ).first()
            
            # Check for leave requests
            leave_request = LeaveRequest.query.filter(
                LeaveRequest.employee_id == employee.id,
                LeaveRequest.start_date <= today,
                LeaveRequest.end_date >= today,
                LeaveRequest.status == 'approved'
            ).first()
            
            if leave_request:
                employee.status = 'leave'
            elif attendance and attendance.check_in:
                employee.status = 'present'
            else:
                employee.status = 'absent'
        
        return render_template('admin_dashboard.html', employees=employees)
    else:
        # Employee dashboard - show own info
        today = date.today()
        attendance = Attendance.query.filter_by(
            employee_id=current_user.id, 
            date=today
        ).first()
        
        recent_leaves = LeaveRequest.query.filter_by(
            employee_id=current_user.id
        ).order_by(LeaveRequest.created_at.desc()).limit(5).all()
        
        return render_template('employee_dashboard.html', 
                             attendance=attendance, 
                             recent_leaves=recent_leaves)

@app.route('/profile', methods=['GET', 'POST'])
@app.route('/profile/<int:employee_id>', methods=['GET', 'POST'])
@login_required
def profile(employee_id=None):
    if employee_id and current_user.role in ['admin', 'hr']:
        user = User.query.get_or_404(employee_id)
    elif employee_id and current_user.role == 'employee':
        # Employees can only view their own profile
        flash('Unauthorized access', 'error')
        return redirect(url_for('profile'))
    else:
        user = current_user
    
    # Get or create profile details
    if not user.profile_details:
        profile_details = ProfileDetails(user_id=user.id)
        db.session.add(profile_details)
        db.session.commit()
    else:
        profile_details = user.profile_details
    
    if request.method == 'POST':
        tab = request.form.get('tab', 'overview')
        
        if tab == 'overview':
            # Handle basic profile updates
            if current_user.role in ['admin', 'hr'] or user.id == current_user.id:
                user.phone = request.form.get('phone', user.phone)
                user.location = request.form.get('location', user.location)
                user.about = request.form.get('about', user.about)
                user.job_motivation = request.form.get('job_motivation', user.job_motivation)
                user.interests_hobbies = request.form.get('interests_hobbies', user.interests_hobbies)
                
                # Handle profile picture upload
                if 'profile_picture' in request.files:
                    file = request.files['profile_picture']
                    if file and file.filename:
                        filename = secure_filename(f"{user.login_id}_{file.filename}")
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        user.profile_picture = filename
                
                db.session.commit()
                flash('Profile updated successfully', 'success')
        
        elif tab == 'private' and (current_user.role in ['admin', 'hr'] or user.id == current_user.id):
            # Handle private information updates
            profile_details.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date() if request.form.get('date_of_birth') else profile_details.date_of_birth
            profile_details.residential_address = request.form.get('residential_address', profile_details.residential_address)
            profile_details.nationality = request.form.get('nationality', profile_details.nationality)
            profile_details.personal_email = request.form.get('personal_email', profile_details.personal_email)
            profile_details.gender = request.form.get('gender', profile_details.gender)
            profile_details.marital_status = request.form.get('marital_status', profile_details.marital_status)
            
            # Bank information
            profile_details.account_number = request.form.get('account_number', profile_details.account_number)
            profile_details.bank_name = request.form.get('bank_name', profile_details.bank_name)
            profile_details.ifsc_code = request.form.get('ifsc_code', profile_details.ifsc_code)
            profile_details.pan_number = request.form.get('pan_number', profile_details.pan_number)
            profile_details.uan_number = request.form.get('uan_number', profile_details.uan_number)
            profile_details.employee_code = request.form.get('employee_code', profile_details.employee_code)
            
            profile_details.updated_at = datetime.utcnow()
            db.session.commit()
            flash('Private information updated successfully', 'success')
        
        elif tab == 'skills' and (current_user.role in ['admin', 'hr'] or user.id == current_user.id):
            # Handle skills update
            skill_name = request.form.get('skill_name')
            proficiency = request.form.get('proficiency_level')
            if skill_name:
                skill = UserSkill(user_id=user.id, skill_name=skill_name, proficiency_level=proficiency)
                db.session.add(skill)
                db.session.commit()
                flash('Skill added successfully', 'success')
        
        elif tab == 'certifications' and (current_user.role in ['admin', 'hr'] or user.id == current_user.id):
            # Handle certifications update
            cert_name = request.form.get('certification_name')
            issuing_org = request.form.get('issuing_organization')
            issue_date = request.form.get('issue_date')
            expiry_date = request.form.get('expiry_date')
            credential_id = request.form.get('credential_id')
            
            if cert_name:
                cert = UserCertification(
                    user_id=user.id,
                    certification_name=cert_name,
                    issuing_organization=issuing_org,
                    issue_date=datetime.strptime(issue_date, '%Y-%m-%d').date() if issue_date else None,
                    expiry_date=datetime.strptime(expiry_date, '%Y-%m-%d').date() if expiry_date else None,
                    credential_id=credential_id
                )
                db.session.add(cert)
                db.session.commit()
                flash('Certification added successfully', 'success')
        
        return redirect(url_for('profile', employee_id=employee_id))
    
    return render_template('profile.html', user=user, profile_details=profile_details)

@app.route('/profile/delete_skill/<int:skill_id>', methods=['POST'])
@login_required
def delete_skill(skill_id):
    skill = UserSkill.query.get_or_404(skill_id)
    if skill.user_id == current_user.id or current_user.role in ['admin', 'hr']:
        db.session.delete(skill)
        db.session.commit()
        flash('Skill deleted successfully', 'success')
    else:
        flash('Unauthorized access', 'error')
    return redirect(url_for('profile'))

@app.route('/profile/delete_certification/<int:cert_id>', methods=['POST'])
@login_required
def delete_certification(cert_id):
    cert = UserCertification.query.get_or_404(cert_id)
    if cert.user_id == current_user.id or current_user.role in ['admin', 'hr']:
        db.session.delete(cert)
        db.session.commit()
        flash('Certification deleted successfully', 'success')
    else:
        flash('Unauthorized access', 'error')
    return redirect(url_for('profile'))

@app.route('/attendance')
@login_required
def attendance():
    if current_user.role in ['admin', 'hr']:
        # Admin can see all attendance
        page = request.args.get('page', 1, type=int)
        attendance_records = Attendance.query.join(User, Attendance.employee_id == User.id).filter(
            User.company_id == current_user.company_id
        ).order_by(Attendance.date.desc()).paginate(
            page=page, per_page=20, error_out=False
        )
        return render_template('admin_attendance.html', attendance_records=attendance_records)
    else:
        # Employee can see only their attendance
        page = request.args.get('page', 1, type=int)
        attendance_records = Attendance.query.filter_by(
            employee_id=current_user.id
        ).order_by(Attendance.date.desc()).paginate(
            page=page, per_page=20, error_out=False
        )
        return render_template('employee_attendance.html', attendance_records=attendance_records)

@app.route('/check_in', methods=['POST'])
@login_required
def check_in():
    today = date.today()
    existing_attendance = Attendance.query.filter_by(
        employee_id=current_user.id,
        date=today
    ).first()
    
    if existing_attendance and existing_attendance.check_in:
        return jsonify({'success': False, 'message': 'Already checked in today'})
    
    if existing_attendance:
        existing_attendance.check_in = datetime.now()
        existing_attendance.status = 'present'
    else:
        attendance = Attendance(
            employee_id=current_user.id,
            date=today,
            check_in=datetime.now(),
            status='present'
        )
        db.session.add(attendance)
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Checked in successfully'})

@app.route('/check_out', methods=['POST'])
@login_required
def check_out():
    today = date.today()
    attendance = Attendance.query.filter_by(
        employee_id=current_user.id,
        date=today
    ).first()
    
    if not attendance or not attendance.check_in:
        return jsonify({'success': False, 'message': 'Must check in first'})
    
    if attendance.check_out:
        return jsonify({'success': False, 'message': 'Already checked out today'})
    
    attendance.check_out = datetime.now()
    # Calculate hours worked
    time_diff = attendance.check_out - attendance.check_in
    attendance.hours_worked = time_diff.total_seconds() / 3600
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Checked out successfully'})

@app.route('/time_off')
@login_required
def time_off():
    if current_user.role in ['admin', 'hr']:
        # Admin can see all leave requests
        leave_requests = LeaveRequest.query.join(User, LeaveRequest.employee_id == User.id).filter(
            User.company_id == current_user.company_id
        ).order_by(LeaveRequest.created_at.desc()).all()
        return render_template('admin_time_off.html', leave_requests=leave_requests)
    else:
        # Employee can see only their leave requests
        leave_requests = LeaveRequest.query.filter_by(
            employee_id=current_user.id
        ).order_by(LeaveRequest.created_at.desc()).all()
        return render_template('employee_time_off.html', leave_requests=leave_requests)

@app.route('/apply_leave', methods=['GET', 'POST'])
@login_required
def apply_leave():
    if request.method == 'POST':
        leave_type = request.form['leave_type']
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        duration = request.form['duration']
        reason = request.form.get('reason', '')
        
        # Validation
        if start_date > end_date:
            flash('Start date cannot be after end date', 'error')
            return render_template('apply_leave.html')
        
        if start_date < date.today():
            flash('Cannot apply for past dates', 'error')
            return render_template('apply_leave.html')
        
        leave_request = LeaveRequest(
            employee_id=current_user.id,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            duration=duration,
            reason=reason
        )
        
        db.session.add(leave_request)
        db.session.commit()
        
        flash('Leave request submitted successfully', 'success')
        return redirect(url_for('time_off'))
    
    return render_template('apply_leave.html')

@app.route('/approve_leave/<int:leave_id>', methods=['POST'])
@login_required
def approve_leave(leave_id):
    if current_user.role not in ['admin', 'hr']:
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
    
    leave_request = LeaveRequest.query.get_or_404(leave_id)
    action = request.form['action']
    comments = request.form.get('comments', '')
    
    if action == 'approve':
        leave_request.status = 'approved'
        # Update attendance records for approved leave days
        current_date = leave_request.start_date
        while current_date <= leave_request.end_date:
            attendance = Attendance.query.filter_by(
                employee_id=leave_request.employee_id,
                date=current_date
            ).first()
            
            if not attendance:
                attendance = Attendance(
                    employee_id=leave_request.employee_id,
                    date=current_date,
                    status='leave'
                )
                db.session.add(attendance)
            else:
                attendance.status = 'leave'
            
            current_date += timedelta(days=1)
    else:
        leave_request.status = 'rejected'
    
    leave_request.approved_by = current_user.id
    leave_request.approved_at = datetime.now()
    leave_request.admin_comments = comments
    
    db.session.commit()
    flash(f'Leave request {action}d successfully', 'success')
    return redirect(url_for('time_off'))

@app.route('/salary', methods=['GET', 'POST'])
@app.route('/salary/<int:employee_id>', methods=['GET', 'POST'])
@login_required
def salary(employee_id=None):
    if employee_id and current_user.role in ['admin', 'hr']:
        user = User.query.get_or_404(employee_id)
    elif employee_id and current_user.role == 'employee':
        # Employees can only view their own salary
        flash('Unauthorized access', 'error')
        return redirect(url_for('salary'))
    else:
        user = current_user
    
    if request.method == 'POST' and current_user.role in ['admin', 'hr']:
        # Handle salary updates (admin/HR only)
        salary_info = SalaryInfo.query.filter_by(employee_id=user.id).first()
        
        if not salary_info:
            salary_info = SalaryInfo(employee_id=user.id)
            db.session.add(salary_info)
        
        # Update salary components
        salary_info.basic_salary = float(request.form.get('basic_salary', 0))
        salary_info.hra = float(request.form.get('hra', 0))
        salary_info.standard_allowance = float(request.form.get('standard_allowance', 0))
        salary_info.performance_bonus = float(request.form.get('performance_bonus', 0))
        salary_info.lta = float(request.form.get('lta', 0))
        salary_info.fixed_allowance = float(request.form.get('fixed_allowance', 0))
        salary_info.pf_employee = float(request.form.get('pf_employee', 0))
        salary_info.pf_employer = float(request.form.get('pf_employer', 0))
        salary_info.professional_tax = float(request.form.get('professional_tax', 0))
        salary_info.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Salary information updated successfully', 'success')
        return redirect(url_for('salary', employee_id=user.id if employee_id else None))
    
    salary_info = SalaryInfo.query.filter_by(employee_id=user.id).first()
    return render_template('salary.html', user=user, salary_info=salary_info)

@app.route('/admin/payroll')
@login_required
def admin_payroll():
    if current_user.role not in ['admin', 'hr']:
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
    
    # Get all employees in the company
    employees = User.query.filter_by(company_id=current_user.company_id).all()
    
    # Get employees with salary configured
    employees_with_salary = [emp for emp in employees if emp.salary_info]
    
    # Calculate total payroll
    total_payroll = 0
    for emp in employees_with_salary:
        if emp.salary_info:
            gross = (emp.salary_info.basic_salary + emp.salary_info.hra + 
                    emp.salary_info.standard_allowance + emp.salary_info.performance_bonus + 
                    emp.salary_info.lta + emp.salary_info.fixed_allowance)
            deductions = emp.salary_info.pf_employee + emp.salary_info.professional_tax
            total_payroll += (gross - deductions)
    
    return render_template('admin_payroll.html', 
                         employees=employees, 
                         employees_with_salary=employees_with_salary,
                         total_payroll=total_payroll)

@app.route('/admin/payroll/bulk-update', methods=['POST'])
@login_required
def bulk_salary_update():
    if current_user.role not in ['admin', 'hr']:
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
    
    action = request.form.get('action')
    
    if action == 'increment':
        increment_percentage = float(request.form.get('increment_percentage', 0))
        reason = request.form.get('reason', '')
        
        # Apply increment to all employees with salary info
        employees = User.query.filter_by(company_id=current_user.company_id).all()
        updated_count = 0
        
        for employee in employees:
            if employee.salary_info:
                # Apply increment to basic salary
                old_basic = employee.salary_info.basic_salary
                new_basic = old_basic * (1 + increment_percentage / 100)
                employee.salary_info.basic_salary = new_basic
                employee.salary_info.updated_at = datetime.utcnow()
                updated_count += 1
        
        db.session.commit()
        flash(f'Salary increment of {increment_percentage}% applied to {updated_count} employees', 'success')
        
    elif action == 'bonus':
        bonus_amount = float(request.form.get('bonus_amount', 0))
        reason = request.form.get('reason', '')
        
        # Apply bonus to all employees with salary info
        employees = User.query.filter_by(company_id=current_user.company_id).all()
        updated_count = 0
        
        for employee in employees:
            if employee.salary_info:
                employee.salary_info.performance_bonus += bonus_amount
                employee.salary_info.updated_at = datetime.utcnow()
                updated_count += 1
        
        db.session.commit()
        flash(f'Bonus of ₹{bonus_amount:,.2f} applied to {updated_count} employees', 'success')
    
    return redirect(url_for('admin_payroll'))

@app.route('/reports')
@login_required
def reports_dashboard():
    if current_user.role not in ['admin', 'hr']:
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
    
    # Get statistics for dashboard
    total_employees = User.query.filter_by(company_id=current_user.company_id).count()
    
    # Get today's attendance stats
    today = date.today()
    present_today = Attendance.query.join(User).filter(
        User.company_id == current_user.company_id,
        Attendance.date == today,
        Attendance.status == 'present'
    ).count()
    
    on_leave_today = LeaveRequest.query.join(User, LeaveRequest.employee_id == User.id).filter(
        User.company_id == current_user.company_id,
        LeaveRequest.start_date <= today,
        LeaveRequest.end_date >= today,
        LeaveRequest.status == 'approved'
    ).count()
    
    # Calculate total payroll
    employees = User.query.filter_by(company_id=current_user.company_id).all()
    total_payroll = 0
    for emp in employees:
        if emp.salary_info:
            gross = (emp.salary_info.basic_salary + emp.salary_info.hra + 
                    emp.salary_info.standard_allowance + emp.salary_info.performance_bonus + 
                    emp.salary_info.lta + emp.salary_info.fixed_allowance)
            deductions = emp.salary_info.pf_employee + emp.salary_info.professional_tax
            total_payroll += (gross - deductions)
    
    return render_template('reports_dashboard.html',
                         total_employees=total_employees,
                         present_today=present_today,
                         on_leave_today=on_leave_today,
                         total_payroll=total_payroll)

@app.route('/reports/view')
@login_required
def view_report():
    if current_user.role not in ['admin', 'hr']:
        return "Unauthorized", 403
    
    report_type = request.args.get('type')
    subtype = request.args.get('subtype')
    
    if report_type == 'attendance':
        return generate_attendance_report_view(subtype)
    elif report_type == 'payroll':
        return generate_payroll_report_view(subtype)
    elif report_type == 'leave':
        return generate_leave_report_view(subtype)
    elif report_type == 'employee':
        return generate_employee_report_view(subtype)
    
    return "Invalid report type", 400

@app.route('/reports/export')
@login_required
def export_report():
    if current_user.role not in ['admin', 'hr']:
        return "Unauthorized", 403
    
    report_type = request.args.get('type')
    subtype = request.args.get('subtype')
    
    if report_type == 'attendance':
        return export_attendance_report(subtype)
    elif report_type == 'payroll':
        return export_payroll_report(subtype)
    elif report_type == 'leave':
        return export_leave_report(subtype)
    elif report_type == 'employee':
        return export_employee_report(subtype)
    
    return "Invalid report type", 400

@app.route('/reports/custom')
@login_required
def custom_report():
    if current_user.role not in ['admin', 'hr']:
        return "Unauthorized", 403
    
    report_type = request.args.get('type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    format_type = request.args.get('format', 'view')
    
    if format_type == 'csv':
        return export_custom_report(report_type, start_date, end_date)
    else:
        return generate_custom_report_view(report_type, start_date, end_date)

def generate_attendance_report_view(subtype):
    """Generate attendance report HTML view"""
    today = date.today()
    
    try:
        if subtype == 'daily':
            records = Attendance.query.join(User).filter(
                User.company_id == current_user.company_id,
                Attendance.date == today
            ).all()
            title = f"Daily Attendance Report - {today.strftime('%B %d, %Y')}"
        elif subtype == 'weekly':
            week_start = today - timedelta(days=today.weekday())
            records = Attendance.query.join(User).filter(
                User.company_id == current_user.company_id,
                Attendance.date >= week_start,
                Attendance.date <= today
            ).all()
            title = f"Weekly Attendance Report - {week_start.strftime('%B %d')} to {today.strftime('%B %d, %Y')}"
        elif subtype == 'monthly':
            month_start = today.replace(day=1)
            records = Attendance.query.join(User).filter(
                User.company_id == current_user.company_id,
                Attendance.date >= month_start,
                Attendance.date <= today
            ).all()
            title = f"Monthly Attendance Report - {today.strftime('%B %Y')}"
        else:
            return "<div class='alert alert-danger'>Invalid report subtype</div>"
    except Exception as e:
        return f"<div class='alert alert-danger'>Error generating report: {str(e)}</div>"
    
    html = f"""
    <div class="report-content">
        <h4>{title}</h4>
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Employee</th>
                        <th>Date</th>
                        <th>Check In</th>
                        <th>Check Out</th>
                        <th>Hours</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    if not records:
        html += """
                    <tr>
                        <td colspan="6" class="text-center text-muted">No attendance records found</td>
                    </tr>
        """
    else:
        for record in records:
            check_in = record.check_in.strftime('%I:%M %p') if record.check_in else '-'
            check_out = record.check_out.strftime('%I:%M %p') if record.check_out else '-'
            hours = f"{record.hours_worked:.2f}" if record.hours_worked > 0 else '-'
            
            html += f"""
                        <tr>
                            <td>{record.employee.first_name} {record.employee.last_name}</td>
                            <td>{record.date.strftime('%Y-%m-%d')}</td>
                            <td>{check_in}</td>
                            <td>{check_out}</td>
                            <td>{hours}</td>
                            <td><span class="badge bg-{'success' if record.status == 'present' else 'info' if record.status == 'leave' else 'warning' if record.status == 'half_day' else 'danger'}">{record.status.replace('_', ' ').title()}</span></td>
                        </tr>
            """
    
    html += """
                </tbody>
            </table>
        </div>
    </div>
    """
    
    return html

def generate_payroll_report_view(subtype):
    """Generate payroll report HTML view"""
    employees = User.query.filter_by(company_id=current_user.company_id).all()
    
    if subtype == 'salary_slips':
        title = "Individual Salary Slips"
        html = f"""
        <div class="report-content">
            <h4>{title}</h4>
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Employee</th>
                            <th>Basic Salary</th>
                            <th>HRA</th>
                            <th>Allowances</th>
                            <th>Gross Salary</th>
                            <th>Deductions</th>
                            <th>Net Salary</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for emp in employees:
            if emp.salary_info:
                basic = emp.salary_info.basic_salary
                hra = emp.salary_info.hra
                allowances = (emp.salary_info.standard_allowance + emp.salary_info.performance_bonus + 
                            emp.salary_info.lta + emp.salary_info.fixed_allowance)
                gross = basic + hra + allowances
                deductions = emp.salary_info.pf_employee + emp.salary_info.professional_tax
                net = gross - deductions
                
                html += f"""
                        <tr>
                            <td>{emp.first_name} {emp.last_name}</td>
                            <td>₹{basic:,.2f}</td>
                            <td>₹{hra:,.2f}</td>
                            <td>₹{allowances:,.2f}</td>
                            <td>₹{gross:,.2f}</td>
                            <td>₹{deductions:,.2f}</td>
                            <td><strong>₹{net:,.2f}</strong></td>
                        </tr>
                """
        
        html += """
                    </tbody>
                </table>
            </div>
        </div>
        """
    
    elif subtype == 'summary':
        total_employees = len([emp for emp in employees if emp.salary_info])
        total_basic = sum(emp.salary_info.basic_salary for emp in employees if emp.salary_info)
        total_gross = sum((emp.salary_info.basic_salary + emp.salary_info.hra + 
                          emp.salary_info.standard_allowance + emp.salary_info.performance_bonus + 
                          emp.salary_info.lta + emp.salary_info.fixed_allowance) 
                         for emp in employees if emp.salary_info)
        total_deductions = sum((emp.salary_info.pf_employee + emp.salary_info.professional_tax) 
                              for emp in employees if emp.salary_info)
        total_net = total_gross - total_deductions
        
        html = f"""
        <div class="report-content">
            <h4>Payroll Summary Report</h4>
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card bg-primary text-white">
                        <div class="card-body text-center">
                            <h3>{total_employees}</h3>
                            <p class="mb-0">Employees</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-info text-white">
                        <div class="card-body text-center">
                            <h3>₹{total_basic:,.0f}</h3>
                            <p class="mb-0">Total Basic</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-success text-white">
                        <div class="card-body text-center">
                            <h3>₹{total_gross:,.0f}</h3>
                            <p class="mb-0">Total Gross</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-warning text-white">
                        <div class="card-body text-center">
                            <h3>₹{total_net:,.0f}</h3>
                            <p class="mb-0">Total Net</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
    
    return html

def generate_leave_report_view(subtype):
    """Generate leave report HTML view"""
    if subtype == 'balance':
        employees = User.query.filter_by(company_id=current_user.company_id).all()
        html = """
        <div class="report-content">
            <h4>Leave Balance Report</h4>
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Employee</th>
                            <th>Department</th>
                            <th>Paid Leave</th>
                            <th>Sick Leave</th>
                            <th>Used This Year</th>
                            <th>Remaining</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for emp in employees:
            used_leaves = LeaveRequest.query.filter(
                LeaveRequest.employee_id == emp.id,
                LeaveRequest.status == 'approved',
                LeaveRequest.start_date >= date(date.today().year, 1, 1)
            ).count()
            
            html += f"""
                    <tr>
                        <td>{emp.first_name} {emp.last_name}</td>
                        <td>{emp.department or 'Not Assigned'}</td>
                        <td>15</td>
                        <td>7</td>
                        <td>{used_leaves}</td>
                        <td>{22 - used_leaves}</td>
                    </tr>
            """
        
        html += """
                </tbody>
            </table>
        </div>
    </div>
        """
    
    return html

def generate_employee_report_view(subtype):
    """Generate employee report HTML view"""
    employees = User.query.filter_by(company_id=current_user.company_id).all()
    
    if subtype == 'directory':
        html = """
        <div class="report-content">
            <h4>Employee Directory Report</h4>
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Employee ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Phone</th>
                            <th>Department</th>
                            <th>Position</th>
                            <th>Role</th>
                            <th>Date Joined</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for emp in employees:
            html += f"""
                    <tr>
                        <td>{emp.login_id}</td>
                        <td>{emp.first_name} {emp.last_name}</td>
                        <td>{emp.email}</td>
                        <td>{emp.phone or 'Not Provided'}</td>
                        <td>{emp.department or 'Not Assigned'}</td>
                        <td>{emp.position or 'Not Assigned'}</td>
                        <td><span class="badge bg-{'success' if emp.role == 'admin' else 'info' if emp.role == 'hr' else 'secondary'}">{emp.role.title()}</span></td>
                        <td>{emp.date_joined.strftime('%Y-%m-%d') if emp.date_joined else 'Not Available'}</td>
                    </tr>
            """
        
        html += """
                </tbody>
            </table>
        </div>
    </div>
        """
    
    return html

def export_attendance_report(subtype):
    """Export attendance report as CSV"""
    from flask import Response
    import csv
    from io import StringIO
    
    today = date.today()
    
    if subtype == 'daily':
        records = Attendance.query.join(User).filter(
            User.company_id == current_user.company_id,
            Attendance.date == today
        ).all()
        filename = f"daily_attendance_{today.strftime('%Y%m%d')}.csv"
    elif subtype == 'weekly':
        week_start = today - timedelta(days=today.weekday())
        records = Attendance.query.join(User).filter(
            User.company_id == current_user.company_id,
            Attendance.date >= week_start,
            Attendance.date <= today
        ).all()
        filename = f"weekly_attendance_{week_start.strftime('%Y%m%d')}_to_{today.strftime('%Y%m%d')}.csv"
    elif subtype == 'monthly':
        month_start = today.replace(day=1)
        records = Attendance.query.join(User).filter(
            User.company_id == current_user.company_id,
            Attendance.date >= month_start,
            Attendance.date <= today
        ).all()
        filename = f"monthly_attendance_{today.strftime('%Y%m')}.csv"
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Employee ID', 'Employee Name', 'Date', 'Check In', 'Check Out', 'Hours Worked', 'Status'])
    
    # Write data
    for record in records:
        check_in = record.check_in.strftime('%H:%M:%S') if record.check_in else ''
        check_out = record.check_out.strftime('%H:%M:%S') if record.check_out else ''
        hours = f"{record.hours_worked:.2f}" if record.hours_worked > 0 else '0'
        
        writer.writerow([
            record.employee.login_id,
            f"{record.employee.first_name} {record.employee.last_name}",
            record.date.strftime('%Y-%m-%d'),
            check_in,
            check_out,
            hours,
            record.status
        ])
    
    output.seek(0)
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )

def export_payroll_report(subtype):
    """Export payroll report as CSV"""
    from flask import Response
    import csv
    from io import StringIO
    
    employees = User.query.filter_by(company_id=current_user.company_id).all()
    
    output = StringIO()
    writer = csv.writer(output)
    
    if subtype == 'salary_slips':
        filename = f"salary_slips_{date.today().strftime('%Y%m')}.csv"
        writer.writerow(['Employee ID', 'Employee Name', 'Department', 'Basic Salary', 'HRA', 'Standard Allowance', 
                        'Performance Bonus', 'LTA', 'Fixed Allowance', 'Gross Salary', 'PF Employee', 
                        'Professional Tax', 'Total Deductions', 'Net Salary'])
        
        for emp in employees:
            if emp.salary_info:
                s = emp.salary_info
                gross = s.basic_salary + s.hra + s.standard_allowance + s.performance_bonus + s.lta + s.fixed_allowance
                deductions = s.pf_employee + s.professional_tax
                net = gross - deductions
                
                writer.writerow([
                    emp.login_id,
                    f"{emp.first_name} {emp.last_name}",
                    emp.department or 'Not Assigned',
                    s.basic_salary,
                    s.hra,
                    s.standard_allowance,
                    s.performance_bonus,
                    s.lta,
                    s.fixed_allowance,
                    gross,
                    s.pf_employee,
                    s.professional_tax,
                    deductions,
                    net
                ])
    
    elif subtype == 'summary':
        filename = f"payroll_summary_{date.today().strftime('%Y%m')}.csv"
        writer.writerow(['Metric', 'Value'])
        
        employees_with_salary = [emp for emp in employees if emp.salary_info]
        total_basic = sum(emp.salary_info.basic_salary for emp in employees_with_salary)
        total_gross = sum((emp.salary_info.basic_salary + emp.salary_info.hra + 
                          emp.salary_info.standard_allowance + emp.salary_info.performance_bonus + 
                          emp.salary_info.lta + emp.salary_info.fixed_allowance) 
                         for emp in employees_with_salary)
        total_deductions = sum((emp.salary_info.pf_employee + emp.salary_info.professional_tax) 
                              for emp in employees_with_salary)
        total_net = total_gross - total_deductions
        
        writer.writerow(['Total Employees', len(employees_with_salary)])
        writer.writerow(['Total Basic Salary', total_basic])
        writer.writerow(['Total Gross Salary', total_gross])
        writer.writerow(['Total Deductions', total_deductions])
        writer.writerow(['Total Net Salary', total_net])
    
    output.seek(0)
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )

def export_leave_report(subtype):
    """Export leave report as CSV"""
    from flask import Response
    import csv
    from io import StringIO
    
    employees = User.query.filter_by(company_id=current_user.company_id).all()
    
    output = StringIO()
    writer = csv.writer(output)
    
    if subtype == 'balance':
        filename = f"leave_balance_{date.today().strftime('%Y%m%d')}.csv"
        writer.writerow(['Employee ID', 'Employee Name', 'Department', 'Paid Leave Quota', 'Sick Leave Quota', 
                        'Used This Year', 'Remaining Balance'])
        
        for emp in employees:
            used_leaves = LeaveRequest.query.filter(
                LeaveRequest.employee_id == emp.id,
                LeaveRequest.status == 'approved',
                LeaveRequest.start_date >= date(date.today().year, 1, 1)
            ).count()
            
            writer.writerow([
                emp.login_id,
                f"{emp.first_name} {emp.last_name}",
                emp.department or 'Not Assigned',
                15,  # Paid leave quota
                7,   # Sick leave quota
                used_leaves,
                22 - used_leaves  # Total quota - used
            ])
    
    output.seek(0)
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )

def export_employee_report(subtype):
    """Export employee report as CSV"""
    from flask import Response
    import csv
    from io import StringIO
    
    employees = User.query.filter_by(company_id=current_user.company_id).all()
    
    output = StringIO()
    writer = csv.writer(output)
    
    if subtype == 'directory':
        filename = f"employee_directory_{date.today().strftime('%Y%m%d')}.csv"
        writer.writerow(['Employee ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Department', 
                        'Position', 'Role', 'Date Joined', 'Status'])
        
        for emp in employees:
            writer.writerow([
                emp.login_id,
                emp.first_name,
                emp.last_name,
                emp.email,
                emp.phone or '',
                emp.department or '',
                emp.position or '',
                emp.role,
                emp.date_joined.strftime('%Y-%m-%d') if emp.date_joined else '',
                'Active' if emp.is_active else 'Inactive'
            ])
    
    output.seek(0)
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )

def export_custom_report(report_type, start_date, end_date):
    """Export custom date range report as CSV"""
    from flask import Response
    import csv
    from io import StringIO
    from datetime import datetime
    
    start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    output = StringIO()
    writer = csv.writer(output)
    
    if report_type == 'attendance':
        records = Attendance.query.join(User).filter(
            User.company_id == current_user.company_id,
            Attendance.date >= start_dt,
            Attendance.date <= end_dt
        ).all()
        
        filename = f"custom_attendance_{start_date}_to_{end_date}.csv"
        writer.writerow(['Employee ID', 'Employee Name', 'Date', 'Check In', 'Check Out', 'Hours Worked', 'Status'])
        
        for record in records:
            check_in = record.check_in.strftime('%H:%M:%S') if record.check_in else ''
            check_out = record.check_out.strftime('%H:%M:%S') if record.check_out else ''
            hours = f"{record.hours_worked:.2f}" if record.hours_worked > 0 else '0'
            
            writer.writerow([
                record.employee.login_id,
                f"{record.employee.first_name} {record.employee.last_name}",
                record.date.strftime('%Y-%m-%d'),
                check_in,
                check_out,
                hours,
                record.status
            ])
    
    output.seek(0)
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )

def generate_custom_report_view(report_type, start_date, end_date):
    """Generate custom report HTML view"""
    from datetime import datetime
    
    start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    if report_type == 'attendance':
        records = Attendance.query.join(User).filter(
            User.company_id == current_user.company_id,
            Attendance.date >= start_dt,
            Attendance.date <= end_dt
        ).all()
        
        html = f"""
        <div class="report-content">
            <h4>Custom Attendance Report ({start_date} to {end_date})</h4>
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Employee</th>
                            <th>Date</th>
                            <th>Check In</th>
                            <th>Check Out</th>
                            <th>Hours</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for record in records:
            check_in = record.check_in.strftime('%I:%M %p') if record.check_in else '-'
            check_out = record.check_out.strftime('%I:%M %p') if record.check_out else '-'
            hours = f"{record.hours_worked:.2f}" if record.hours_worked > 0 else '-'
            
            html += f"""
                        <tr>
                            <td>{record.employee.first_name} {record.employee.last_name}</td>
                            <td>{record.date.strftime('%Y-%m-%d')}</td>
                            <td>{check_in}</td>
                            <td>{check_out}</td>
                            <td>{hours}</td>
                            <td><span class="badge bg-{'success' if record.status == 'present' else 'info' if record.status == 'leave' else 'warning' if record.status == 'half_day' else 'danger'}">{record.status.replace('_', ' ').title()}</span></td>
                        </tr>
            """
        
        html += """
                    </tbody>
                </table>
            </div>
        </div>
        """
        
        return html
    
    return "Report type not supported for custom date range"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)