#!/usr/bin/env python3
"""
Installation script for Dayflow HRMS
This script will help you set up the application quickly
"""

import os
import sys
import subprocess
import getpass

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install Python dependencies"""
    return run_command("pip install -r requirements.txt", "Installing Python dependencies")

def setup_environment():
    """Set up environment variables"""
    print("\n📝 Setting up environment configuration...")
    
    # Get database credentials
    print("\nDatabase Configuration (XAMPP MySQL):")
    print("💡 For XAMPP, typically use: host=localhost, port=3306, user=root, password='' (empty)")
    
    db_host = input("MySQL Host (default: localhost): ").strip() or "localhost"
    db_port = input("MySQL Port (default: 3306): ").strip() or "3306"
    db_user = input("MySQL Username (default: root): ").strip() or "root"
    
    # Handle empty password for XAMPP
    db_password = input("MySQL Password (press Enter for empty password): ").strip()
    
    db_name = input("Database Name (default: dayflow_hrms): ").strip() or "dayflow_hrms"
    
    # Generate secret key
    import secrets
    secret_key = secrets.token_hex(32)
    
    # Create DATABASE_URL with proper format
    if db_password:
        database_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    else:
        database_url = f"mysql+pymysql://{db_user}:@{db_host}:{db_port}/{db_name}"
    
    # Create .env file
    env_content = f"""SECRET_KEY={secret_key}
DATABASE_URL={database_url}
FLASK_ENV=development
FLASK_DEBUG=True"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✓ Environment configuration saved to .env")
    print(f"✓ Database URL: {database_url}")
    return True

def setup_database():
    """Set up the database"""
    print("\n🗄️  Setting up database...")
    
    try:
        # Import and run database setup
        from database_setup import create_database, create_sample_data
        create_database()
        create_sample_data()
        print("✓ Database setup completed successfully")
        return True
    except Exception as e:
        print(f"✗ Database setup failed: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        'static/uploads',
        'instance'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    return True

def main():
    """Main installation process"""
    print("🚀 Dayflow HRMS Installation Script")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies. Please check your internet connection and try again.")
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        print("\n❌ Database setup failed. Please check your MySQL configuration and try again.")
        sys.exit(1)
    
    print("\n🎉 Installation completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the application: python app.py")
    print("2. Open your browser and go to: http://localhost:5000")
    print("3. Use the following credentials to login:")
    print("   - Admin: ODJODO20240001 / admin123")
    print("   - HR: ODJASM20240002 / hr123")
    print("   - Employee: ODMIPR20240003 / emp123")
    print("\n📚 For more information, check the README.md file")

if __name__ == "__main__":
    main()