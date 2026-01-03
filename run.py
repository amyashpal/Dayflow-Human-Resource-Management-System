#!/usr/bin/env python3
"""
Simple run script for Dayflow HRMS
This script provides a convenient way to start the application
"""

import os
import sys
from app import app, db

def check_environment():
    """Check if environment is properly configured"""
    if not os.path.exists('.env'):
        print("❌ .env file not found. Please run install.py first or create .env manually.")
        return False
    
    required_vars = ['SECRET_KEY', 'DATABASE_URL']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    return True

def check_database():
    """Check if database is accessible"""
    try:
        with app.app_context():
            # Use text() for raw SQL in newer SQLAlchemy versions
            from sqlalchemy import text
            db.engine.execute(text('SELECT 1'))
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("💡 XAMPP MySQL Troubleshooting:")
        print("   1. Start XAMPP Control Panel")
        print("   2. Start MySQL service")
        print("   3. Check if MySQL is running on port 3306")
        print("   4. Try running: python database_setup.py")
        return False

def main():
    """Main function to start the application"""
    print("🚀 Starting Dayflow HRMS...")
    print("=" * 40)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Check database
    if not check_database():
        sys.exit(1)
    
    # Start the application
    print("🌐 Starting Flask development server...")
    print("📍 Application will be available at: http://localhost:5000")
    print("🔑 Default credentials:")
    print("   Admin: ODJODO20240001 / admin123")
    print("   HR: ODJASM20240002 / hr123")
    print("   Employee: ODMIPR20240003 / emp123")
    print("\n⏹️  Press Ctrl+C to stop the server")
    print("=" * 40)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Shutting down Dayflow HRMS. Goodbye!")

if __name__ == "__main__":
    main()