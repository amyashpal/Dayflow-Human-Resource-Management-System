#!/usr/bin/env python3
"""
XAMPP-specific setup script for Dayflow HRMS
This script is optimized for XAMPP MySQL configuration
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def test_xampp_connection():
    """Test connection to XAMPP MySQL"""
    print("🔍 Testing XAMPP MySQL connection...")
    
    try:
        # XAMPP default configuration
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password=''  # XAMPP default: empty password
        )
        
        if connection.is_connected():
            print("✅ Successfully connected to XAMPP MySQL!")
            
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            
            print("📋 Available databases:")
            for db in databases:
                print(f"   - {db[0]}")
            
            return True
            
    except Error as e:
        print(f"❌ Connection failed: {e}")
        print("\n🔧 XAMPP Troubleshooting:")
        print("1. Open XAMPP Control Panel")
        print("2. Start MySQL service (click 'Start' button)")
        print("3. Make sure MySQL is running on port 3306")
        print("4. Check if phpMyAdmin is accessible at http://localhost/phpmyadmin")
        return False
    
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def create_database_xampp():
    """Create database using XAMPP MySQL"""
    print("\n🗄️ Creating database for XAMPP...")
    
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password=''
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS dayflow_hrms")
            cursor.execute("USE dayflow_hrms")
            
            print("✅ Database 'dayflow_hrms' created successfully!")
            
            # Check if database was created
            cursor.execute("SHOW DATABASES LIKE 'dayflow_hrms'")
            result = cursor.fetchone()
            
            if result:
                print("✅ Database verification successful!")
                return True
            else:
                print("❌ Database creation verification failed!")
                return False
                
    except Error as e:
        print(f"❌ Database creation failed: {e}")
        return False
    
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def setup_sample_data():
    """Setup sample data using the main app"""
    print("\n👥 Setting up sample data...")
    
    try:
        # Import after ensuring database exists
        from app import app, db, User, Company, SalaryInfo
        from werkzeug.security import generate_password_hash
        from datetime import date
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ Database tables created!")
            
            # Create sample company
            company = Company.query.filter_by(code='OD').first()
            if not company:
                company = Company(name='Odoo India', code='OD')
                db.session.add(company)
                db.session.flush()
                print("✅ Sample company created!")
            
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
                print("✅ Admin user created!")
                
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
                print("✅ HR user created!")
                
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
                print("✅ Employee user created!")
                
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
            print("✅ Sample data created successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Sample data creation failed: {e}")
        return False

def main():
    """Main XAMPP setup process"""
    print("🚀 Dayflow HRMS - XAMPP Setup")
    print("=" * 40)
    
    # Test XAMPP connection
    if not test_xampp_connection():
        print("\n❌ Please start XAMPP MySQL service and try again.")
        return
    
    # Create database
    if not create_database_xampp():
        print("\n❌ Database creation failed.")
        return
    
    # Setup sample data
    if not setup_sample_data():
        print("\n❌ Sample data setup failed.")
        return
    
    print("\n🎉 XAMPP setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the application: python app.py")
    print("2. Open your browser and go to: http://localhost:5000")
    print("3. Use the following credentials to login:")
    print("   - Admin: ODJODO20240001 / admin123")
    print("   - HR: ODJASM20240002 / hr123")
    print("   - Employee: ODMIPR20240003 / emp123")
    print("\n🔗 You can also check the database at: http://localhost/phpmyadmin")

if __name__ == '__main__':
    main()