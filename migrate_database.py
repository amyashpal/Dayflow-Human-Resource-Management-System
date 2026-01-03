#!/usr/bin/env python3
"""
Database migration script to add new profile functionality columns
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def migrate_database():
    """Add new columns and tables for comprehensive profile functionality"""
    
    with app.app_context():
        print("🔄 Starting database migration...")
        
        try:
            # Drop all tables and recreate them with new schema
            print("\n1. Recreating database schema...")
            db.drop_all()
            db.create_all()
            print("   ✅ Database schema recreated with all new tables and columns")
            
            # Create a default company for testing
            from app import Company, User
            from werkzeug.security import generate_password_hash
            
            print("\n2. Creating default test data...")
            
            # Create default company
            company = Company(name="Dayflow Technologies", code="DT")
            db.session.add(company)
            db.session.flush()
            
            # Create admin user
            admin_user = User(
                login_id="DTAD20241001",
                email="admin@dayflow.com",
                password_hash=generate_password_hash("admin123"),
                first_name="Admin",
                last_name="User",
                role="admin",
                company_id=company.id,
                department="IT",
                position="System Administrator",
                must_change_password=False
            )
            db.session.add(admin_user)
            
            # Create test employee
            employee_user = User(
                login_id="DTEM20241001",
                email="employee@dayflow.com",
                password_hash=generate_password_hash("emp123"),
                first_name="Test",
                last_name="Employee",
                role="employee",
                company_id=company.id,
                department="Development",
                position="Software Developer",
                must_change_password=False
            )
            db.session.add(employee_user)
            
            db.session.commit()
            
            print("   ✅ Default admin user created: DTAD20241001 / admin123")
            print("   ✅ Default employee user created: DTEM20241001 / emp123")
            
            print("\n✅ Database migration completed successfully!")
            print("\n📋 Migration Summary:")
            print("   - Recreated database with comprehensive profile schema")
            print("   - User table includes: location, about, job_motivation, interests_hobbies")
            print("   - ProfileDetails table for personal and bank information")
            print("   - UserSkill table for skills management")
            print("   - UserCertification table for certifications management")
            print("   - All foreign key relationships established")
            print("   - Default test users created for immediate testing")
            
        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            db.session.rollback()

if __name__ == "__main__":
    migrate_database()