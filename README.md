# Dayflow - Human Resource Management System

**Every workday, perfectly aligned.**

A comprehensive Human Resource Management System built with Python Flask and MySQL, designed to streamline HR operations including employee management, attendance tracking, leave management, and payroll visibility.

## 🌟 Features

### 🔐 Authentication & Authorization
- Secure sign-up/sign-in system with auto-generated employee IDs
- Role-based access control (Admin, HR, Employee)
- Password change enforcement for new users
- Session management with Flask-Login

### 👥 Employee Management
- Comprehensive employee profiles with photo upload
- Role-based dashboard views (Admin/HR vs Employee)
- Company and department organization
- Manager-subordinate relationships

### ⏰ Attendance Tracking
- Real-time check-in/check-out functionality
- Live attendance status indicators (🟢 Present, ✈️ On Leave, 🟡 Absent)
- Daily, weekly, and monthly attendance views
- Automatic hours worked calculation

### 🏖️ Leave Management
- Multiple leave types (Paid Time Off, Sick Leave, Unpaid Leave)
- Complete leave application workflow
- Admin/HR approval system with comments
- Leave balance tracking and history

### 💰 Payroll Management
- Comprehensive salary structure with multiple components
- Automatic salary calculations (Basic, HRA, Allowances, Deductions)
- PF and Professional Tax management
- Read-only access for employees, full control for Admin/HR

## 🛠️ Technology Stack

- **Backend**: Python Flask 2.3.3
- **Database**: MySQL with SQLAlchemy ORM
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript/jQuery
- **Authentication**: Flask-Login with Werkzeug password hashing
- **File Upload**: Secure file handling with Werkzeug
- **Environment**: python-dotenv for configuration

## 🚀 Quick Installation

### Option 1: Automated Installation (Recommended)
```bash
git clone <repository-url>
cd Dayflow-Human-Resource-Management-System
python install.py
```

### Option 2: Manual Installation

#### Prerequisites
- Python 3.8+
- MySQL Server 5.7+
- pip (Python package manager)

#### Steps
1. **Clone and Setup**
```bash
git clone <repository-url>
cd Dayflow-Human-Resource-Management-System
pip install -r requirements.txt
```

2. **Database Configuration**
```bash
# Update .env file with your MySQL credentials
DATABASE_URL=mysql+pymysql://username:password@localhost/dayflow_hrms
```

3. **Initialize Database**
```bash
python database_setup.py
```

4. **Run Application**
```bash
python app.py
```

Access the application at `http://localhost:5000`

## 🔑 Default Login Credentials

| Role | Login ID | Password | Access Level |
|------|----------|----------|--------------|
| Admin | `ODJODO20240001` | `admin123` | Full system access |
| HR Manager | `ODJASM20240002` | `hr123` | Employee & leave management |
| Employee | `ODMIPR20240003` | `emp123` | Personal profile & attendance |

## 📋 Employee ID Format

Employee IDs are automatically generated using the format:
**`[Company Code][Employee Initials][Year][Serial Number]`**

**Example**: `ODJODO20240001`
- `OD` - Company code (Odoo)
- `JODO` - Employee initials (John Doe)
- `2024` - Year of joining
- `0001` - Serial number for that year

## 👤 User Roles & Permissions

### 🔴 Admin
- ✅ Full system access and configuration
- ✅ Employee management (create, edit, view all)
- ✅ Attendance oversight for entire organization
- ✅ Leave request approvals and management
- ✅ Salary management and payroll configuration
- ✅ Company and department management

### 🟡 HR Officer
- ✅ Employee profile management
- ✅ Attendance monitoring and reporting
- ✅ Leave request processing and approvals
- ✅ Salary information access and updates
- ✅ Employee onboarding and offboarding
- ❌ System configuration and admin settings

### 🟢 Employee
- ✅ Personal profile management (limited fields)
- ✅ Own attendance tracking and history
- ✅ Leave application and status tracking
- ✅ Salary information viewing (read-only)
- ✅ Check-in/check-out functionality
- ❌ Access to other employees' data

## 🎯 Key Features Implementation

### Real-time Attendance System
- **Live Status Indicators**: 🟢 Present, ✈️ On Leave, 🟡 Absent
- **Automatic Calculations**: Hours worked, overtime tracking
- **Integration**: Seamless integration with leave management
- **Reporting**: Daily, weekly, monthly attendance reports

### Advanced Leave Management
- **Multi-step Workflow**: Application → Review → Approval/Rejection
- **Leave Types**: Paid Time Off, Sick Leave, Unpaid Leave
- **Balance Tracking**: Automatic leave balance calculations
- **Notifications**: Email alerts for status changes (configurable)

### Comprehensive Payroll System
- **Salary Components**: Basic, HRA, Allowances, Bonuses
- **Automatic Calculations**: Tax deductions, PF contributions
- **Compliance**: Professional tax and statutory deductions
- **Reporting**: Salary slips and payroll reports

### Security Features
- **Password Security**: Werkzeug password hashing
- **Session Management**: Secure Flask-Login sessions
- **Role-based Access**: Route-level permission controls
- **Input Validation**: Comprehensive form validation and sanitization
- **File Upload Security**: Secure filename handling and validation

## 📁 Project Structure
```
Dayflow-Human-Resource-Management-System/
├── 📄 app.py                    # Main Flask application with all routes
├── 🗄️ database_setup.py         # Database initialization and sample data
├── ⚙️ install.py               # Automated installation script
├── 🚀 run.py                   # Application runner with checks
├── 📋 requirements.txt         # Python dependencies
├── 🔧 .env                     # Environment variables (create from install.py)
├── 📖 README.md               # Main documentation
├── 🚀 DEPLOYMENT.md           # Deployment and production guide
├── 🚫 .gitignore              # Git ignore rules
├── 📁 templates/               # Jinja2 HTML templates
│   ├── 🏠 base.html            # Base template with navigation
│   ├── 🔐 login.html           # Login page with company branding
│   ├── 📝 register.html        # Employee registration (HR/Admin only)
│   ├── 🔑 change_password.html # Mandatory password change
│   ├── 📊 admin_dashboard.html # Admin dashboard with employee grid
│   ├── 👤 employee_dashboard.html # Employee dashboard with quick actions
│   ├── 👤 profile.html         # Comprehensive profile management
│   ├── ⏰ employee_attendance.html # Employee attendance view
│   ├── ⏰ admin_attendance.html # Admin attendance management
│   ├── 🏖️ employee_time_off.html # Employee leave requests
│   ├── 🏖️ admin_time_off.html  # Admin leave management
│   ├── 📝 apply_leave.html     # Leave application form
│   ├── 💰 salary.html          # Salary information and management
│   ├── 🔄 leave_table.html     # Reusable leave table component
│   ├── ❌ 404.html             # Custom 404 error page
│   └── ⚠️ 500.html             # Custom 500 error page
├── 📁 static/
│   └── 📁 uploads/             # Profile pictures and documents
│       └── .gitkeep           # Ensures directory exists
└── 📊 Database Schema:
    ├── 🏢 Company              # Company information and branding
    ├── 👤 User                 # Employee profiles and authentication
    ├── ⏰ Attendance           # Daily attendance records
    ├── 🏖️ LeaveRequest         # Leave applications and approvals
    └── 💰 SalaryInfo           # Comprehensive salary structure
```

## 🔗 API Endpoints

### Authentication
- `GET/POST /login` - User authentication
- `GET/POST /register` - Employee registration (Admin/HR only)
- `GET /logout` - Session termination
- `GET/POST /change_password` - Password management

### Dashboard & Profile
- `GET /dashboard` - Role-based dashboard
- `GET/POST /profile` - User profile management
- `GET/POST /profile/<employee_id>` - Employee profile (Admin/HR)

### Attendance Management
- `GET /attendance` - Attendance records and history
- `POST /check_in` - Employee check-in (AJAX)
- `POST /check_out` - Employee check-out (AJAX)

### Leave Management
- `GET /time_off` - Leave requests list and management
- `GET/POST /apply_leave` - Leave application form
- `POST /approve_leave/<leave_id>` - Leave approval (Admin/HR)

### Payroll
- `GET/POST /salary` - Salary information and management
- `GET/POST /salary/<employee_id>` - Employee salary (Admin/HR)

## 🎨 UI/UX Features

### Modern Design
- **Bootstrap 5**: Responsive, mobile-first design
- **Font Awesome Icons**: Comprehensive icon library
- **Custom Styling**: Professional color scheme and layouts
- **Interactive Elements**: Hover effects, animations, and transitions

### User Experience
- **Intuitive Navigation**: Clear menu structure and breadcrumbs
- **Real-time Feedback**: AJAX-powered interactions
- **Form Validation**: Client and server-side validation
- **Responsive Design**: Works on desktop, tablet, and mobile

### Accessibility
- **Screen Reader Support**: Proper ARIA labels and semantic HTML
- **Keyboard Navigation**: Full keyboard accessibility
- **Color Contrast**: WCAG compliant color schemes
- **Alternative Text**: Images with descriptive alt text

## 🔧 Configuration

### Environment Variables (.env)
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://username:password@localhost/dayflow_hrms
FLASK_ENV=development
FLASK_DEBUG=True
```

### Database Configuration
- **MySQL 5.7+** recommended
- **UTF-8 encoding** for international character support
- **InnoDB engine** for transaction support
- **Regular backups** recommended for production

## 🚀 Deployment

### Development
```bash
python app.py
# Access at http://localhost:5000
```

### Production (Example with Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Docker Deployment
```dockerfile
# Dockerfile example
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🧪 Testing

### Manual Testing Checklist
- [ ] User authentication and authorization
- [ ] Employee registration and profile management
- [ ] Attendance check-in/check-out functionality
- [ ] Leave application and approval workflow
- [ ] Salary information display and updates
- [ ] Role-based access control
- [ ] File upload functionality
- [ ] Responsive design on different devices

### Test Data
The `database_setup.py` script creates sample data for testing:
- 1 Admin user with full permissions
- 1 HR user with management permissions  
- 1 Employee user with basic permissions
- Sample salary information for all users

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comments for complex logic
- Update documentation for new features
- Test thoroughly before submitting

## 📄 License

This project is developed for the **Odoo Hackathon** and is intended for educational and demonstration purposes. 

## 🆘 Support & Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check MySQL service status
sudo systemctl status mysql
# Verify credentials in .env file
```

**Module Import Error**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**File Upload Issues**
```bash
# Check directory permissions
chmod 755 static/uploads/
```

### Getting Help
- 📧 Contact the development team
- 🐛 Create an issue in the repository
- 📖 Check the documentation and README
- 💬 Join the project discussion forum

---

**Dayflow HRMS** - Streamlining human resource management for modern workplaces.

*Built with ❤️ for the Odoo Hackathon*