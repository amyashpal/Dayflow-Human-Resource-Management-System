#!/usr/bin/env python3
"""
Comprehensive test script for Dayflow HRMS
This script tests all functionality and pages
"""

import requests
import json
from datetime import datetime, date

# Base URL for the application
BASE_URL = "http://localhost:5000"

class HRMSTest:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
    
    def log_test(self, test_name, success, message=""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.test_results.append({
            'test': test_name,
            'status': status,
            'message': message
        })
        print(f"{status}: {test_name} {message}")
    
    def test_page_access(self, url, expected_status=200, test_name=""):
        """Test if a page is accessible"""
        try:
            response = self.session.get(f"{BASE_URL}{url}")
            success = response.status_code == expected_status
            self.log_test(test_name or f"Access {url}", success, 
                         f"Status: {response.status_code}")
            return response
        except Exception as e:
            self.log_test(test_name or f"Access {url}", False, f"Error: {e}")
            return None
    
    def test_login(self, login_id, password, expected_success=True):
        """Test login functionality"""
        try:
            # Get login page first
            login_page = self.session.get(f"{BASE_URL}/login")
            
            # Attempt login
            login_data = {
                'login_id': login_id,
                'password': password
            }
            
            response = self.session.post(f"{BASE_URL}/login", data=login_data, 
                                       allow_redirects=False)
            
            if expected_success:
                success = response.status_code in [302, 200] and 'dashboard' in response.headers.get('Location', '')
                self.log_test(f"Login as {login_id}", success, 
                             f"Redirect: {response.headers.get('Location', 'None')}")
            else:
                success = response.status_code == 200 and 'login' in response.url
                self.log_test(f"Invalid login {login_id}", success)
            
            return success
        except Exception as e:
            self.log_test(f"Login as {login_id}", False, f"Error: {e}")
            return False
    
    def test_logout(self):
        """Test logout functionality"""
        try:
            response = self.session.get(f"{BASE_URL}/logout", allow_redirects=False)
            success = response.status_code == 302 and 'login' in response.headers.get('Location', '')
            self.log_test("Logout", success)
            return success
        except Exception as e:
            self.log_test("Logout", False, f"Error: {e}")
            return False
    
    def test_check_in_out(self):
        """Test attendance check-in/out functionality"""
        try:
            # Test check-in
            checkin_response = self.session.post(f"{BASE_URL}/check_in")
            checkin_success = checkin_response.status_code == 200
            
            if checkin_success:
                checkin_data = checkin_response.json()
                checkin_success = checkin_data.get('success', False)
            
            self.log_test("Check-in functionality", checkin_success)
            
            # Test check-out
            checkout_response = self.session.post(f"{BASE_URL}/check_out")
            checkout_success = checkout_response.status_code == 200
            
            if checkout_success:
                checkout_data = checkout_response.json()
                checkout_success = checkout_data.get('success', False)
            
            self.log_test("Check-out functionality", checkout_success)
            
            return checkin_success and checkout_success
        except Exception as e:
            self.log_test("Check-in/out functionality", False, f"Error: {e}")
            return False
    
    def run_comprehensive_test(self):
        """Run all tests"""
        print("🚀 Starting Dayflow HRMS Comprehensive Test")
        print("=" * 50)
        
        # Test 1: Basic page accessibility (without login)
        print("\n📋 Testing Basic Page Access...")
        self.test_page_access("/", 302, "Home page redirect")
        self.test_page_access("/login", 200, "Login page")
        
        # Test 2: Admin Login and Dashboard
        print("\n👑 Testing Admin Functionality...")
        if self.test_login("ODJODO20240001", "admin123"):
            self.test_page_access("/dashboard", 200, "Admin dashboard")
            self.test_page_access("/profile", 200, "Admin profile")
            self.test_page_access("/attendance", 200, "Admin attendance view")
            self.test_page_access("/time_off", 200, "Admin time-off management")
            self.test_page_access("/salary", 200, "Admin salary view")
            self.test_page_access("/register", 200, "Employee registration (Admin)")
            
            # Test employee profile access (Admin viewing employee)
            self.test_page_access("/profile/3", 200, "View employee profile (Admin)")
            self.test_page_access("/salary/3", 200, "View employee salary (Admin)")
        
        self.test_logout()
        
        # Test 3: HR Login and Functionality
        print("\n👥 Testing HR Functionality...")
        if self.test_login("ODJASM20240002", "hr123"):
            self.test_page_access("/dashboard", 200, "HR dashboard")
            self.test_page_access("/profile", 200, "HR profile")
            self.test_page_access("/attendance", 200, "HR attendance view")
            self.test_page_access("/time_off", 200, "HR time-off management")
            self.test_page_access("/salary", 200, "HR salary view")
            self.test_page_access("/register", 200, "Employee registration (HR)")
        
        self.test_logout()
        
        # Test 4: Employee Login and Functionality
        print("\n👤 Testing Employee Functionality...")
        if self.test_login("ODMIPR20240003", "emp123"):
            self.test_page_access("/dashboard", 200, "Employee dashboard")
            self.test_page_access("/profile", 200, "Employee profile")
            self.test_page_access("/attendance", 200, "Employee attendance view")
            self.test_page_access("/time_off", 200, "Employee time-off view")
            self.test_page_access("/apply_leave", 200, "Leave application form")
            self.test_page_access("/salary", 200, "Employee salary view")
            
            # Test restricted access (Employee trying to access admin features)
            self.test_page_access("/register", 302, "Employee registration (should redirect)")
            self.test_page_access("/profile/1", 302, "View other profile (should redirect)")
            
            # Test attendance functionality
            self.test_check_in_out()
        
        self.test_logout()
        
        # Test 5: Invalid Login Attempts
        print("\n🔒 Testing Security...")
        self.test_login("INVALID123", "wrongpass", False)
        self.test_login("ODJODO20240001", "wrongpass", False)
        
        # Test 6: Unauthorized Access
        print("\n🚫 Testing Unauthorized Access...")
        self.test_page_access("/dashboard", 302, "Dashboard without login (should redirect)")
        self.test_page_access("/profile", 302, "Profile without login (should redirect)")
        
        # Print Summary
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        passed = sum(1 for result in self.test_results if "✅" in result['status'])
        failed = sum(1 for result in self.test_results if "❌" in result['status'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if failed > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if "❌" in result['status']:
                    print(f"   - {result['test']}: {result['message']}")
        
        print("\n🎉 Test completed!")
        return failed == 0

def main():
    """Main test function"""
    tester = HRMSTest()
    
    print("⚠️  Testing application at http://localhost:5000")
    print("Starting automated test...")
    
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n🎉 All tests passed! The HRMS system is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")

if __name__ == "__main__":
    main()