"""
Database setup script for Dayflow HRMS
Run this script to create the database and initial data
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Create the database if it doesn't exist"""
    connection = None
    try:
        # Parse DATABASE_URL from .env to get connection details
        database_url = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost:3306/dayflow_hrms')
        
        # Extract connection details from DATABASE_URL
        # Format: mysql+pymysql://user:password@host:port/database
        import re
        match = re.match(r'mysql\+pymysql://([^:]*):([^@]*)@([^:/]*):?(\d*)/(.+)', database_url)
        
        if match:
            user, password, host, port, database = match.groups()
            port = int(port) if port else 3306
        else:
            # Fallback for XAMPP defaults
            user, password, host, port, database = 'root', '', 'localhost', 3306, 'dayflow_hrms'
        
        print(f"Connecting to MySQL at {host}:{port} as user '{user}'...")
        
        # Connect to MySQL server (without specifying database)
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password if password else ''  # Handle empty password for XAMPP
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            print(f"Database '{database}' created successfully!")
            
            # For XAMPP, we typically don't need to create additional users
            # Just use the root user with empty password
            print("Using existing MySQL user (XAMPP default configuration)")
            
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print("\n💡 XAMPP MySQL Troubleshooting:")
        print("1. Make sure XAMPP MySQL service is running")
        print("2. Check if MySQL is running on port 3306")
        print("3. Default XAMPP MySQL: user='root', password='' (empty)")
        print("4. Try accessing MySQL via phpMyAdmin first")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
    
    return True

def create_sample_data():
    """Create sample data for testing"""
    from app import app, db, User, Company, SalaryInfo
    from werkzeug.security import generate_password_hash
    from datetime import date
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create sample company
        company = Company.query.filter_by(code='OD').first()
        if not company:
            company = Company(name='Odoo India', code='OD')
            db.session.add(company)
            db.session.flush()
        
        # Create admin user
        admin = User.query.filter_by(login_id='ODJODO20240001').first()
        if not admin:
            admin = User(
                login_id='ODJODO20240001',
                email='admin@dayflow.com',
                password_hash=generate_password_hash('admin123'),
                first_name='John',
                last_name='Doe',
                phone='+91-9876543210',
                role='admin',
                department='Administration',
                position='System Administrator',
                company_id=company.id,
                must_change_password=False
            )
            db.session.add(admin)
            db.session.flush()
            
            # Add salary info for admin
            admin_salary = SalaryInfo(
                employee_id=admin.id,
                basic_salary=80000.00,
                hra=24000.00,
                standard_allowance=5000.00,
                performance_bonus=10000.00,
                lta=2000.00,
                fixed_allowance=3000.00,
                pf_employee=9600.00,
                pf_employer=9600.00,
                professional_tax=200.00
            )
            db.session.add(admin_salary)
        
        # Create HR user
        hr_user = User.query.filter_by(login_id='ODJASM20240002').first()
        if not hr_user:
            hr_user = User(
                login_id='ODJASM20240002',
                email='hr@dayflow.com',
                password_hash=generate_password_hash('hr123'),
                first_name='Jane',
                last_name='Smith',
                phone='+91-9876543211',
                role='hr',
                department='Human Resources',
                position='HR Manager',
                company_id=company.id,
                manager_id=admin.id,
                must_change_password=False
            )
            db.session.add(hr_user)
            db.session.flush()
            
            # Add salary info for HR
            hr_salary = SalaryInfo(
                employee_id=hr_user.id,
                basic_salary=60000.00,
                hra=18000.00,
                standard_allowance=4000.00,
                performance_bonus=8000.00,
                lta=1500.00,
                fixed_allowance=2500.00,
                pf_employee=7200.00,
                pf_employer=7200.00,
                professional_tax=200.00
            )
            db.session.add(hr_salary)
        
        # Create sample employee
        employee = User.query.filter_by(login_id='ODMIPR20240003').first()
        if not employee:
            employee = User(
                login_id='ODMIPR20240003',
                email='employee@dayflow.com',
                password_hash=generate_password_hash('emp123'),
                first_name='Mike',
                last_name='Patel',
                phone='+91-9876543212',
                role='employee',
                department='Development',
                position='Software Developer',
                company_id=company.id,
                manager_id=hr_user.id,
                must_change_password=False
            )
            db.session.add(employee)
            db.session.flush()
            
            # Add salary info for employee
            emp_salary = SalaryInfo(
                employee_id=employee.id,
                basic_salary=45000.00,
                hra=13500.00,
                standard_allowance=3000.00,
                performance_bonus=5000.00,
                lta=1000.00,
                fixed_allowance=2000.00,
                pf_employee=5400.00,
                pf_employer=5400.00,
                professional_tax=200.00
            )
            db.session.add(emp_salary)
        
        db.session.commit()
        print("Sample data created successfully!")
        print("\nLogin Credentials:")
        print("Admin: ODJODO20240001 / admin123")
        print("HR: ODJASM20240002 / hr123")
        print("Employee: ODMIPR20240003 / emp123")

if __name__ == '__main__':
    print("Setting up Dayflow HRMS Database...")
    create_database()
    create_sample_data()
    print("Database setup completed!")