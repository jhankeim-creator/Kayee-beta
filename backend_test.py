#!/usr/bin/env python3
"""
Backend API Testing Suite for E-commerce Features
Tests shipping options, payment methods, and order functionality
"""

import requests
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any

# Get backend URL from frontend .env
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"❌ Error reading frontend .env: {e}")
        return None

class EcommerceTester:
    def __init__(self):
        self.backend_url = get_backend_url()
        if not self.backend_url:
            raise Exception("Could not get backend URL from frontend/.env")
        
        self.api_base = f"{self.backend_url}/api"
        self.session = requests.Session()
        self.test_results = []
        
        print(f"🔗 Backend URL: {self.backend_url}")
        print(f"🔗 API Base: {self.api_base}")
        print("=" * 60)

    def log_result(self, test_name: str, success: bool, message: str, details: Dict = None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
        self.test_results.append(result)
        
        if details:
            for key, value in details.items():
                print(f"    {key}: {value}")
        print()

    def test_backend_health(self):
        """Test if backend is accessible"""
        try:
            response = self.session.get(f"{self.api_base}/categories", timeout=10)
            if response.status_code == 200:
                self.log_result("Backend Health", True, "Backend is accessible")
                return True
            else:
                self.log_result("Backend Health", False, f"Backend returned {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Backend Health", False, f"Backend not accessible: {str(e)}")
            return False

    def create_test_order_with_plisio(self):
        """Create a test order with Plisio payment method"""
        test_order_payload = {
            "user_email": "test@example.com",
            "user_name": "Test User",
            "items": [
                {
                    "product_id": "test-123",
                    "name": "Test Product",
                    "price": 100.50,
                    "quantity": 1,
                    "image": "https://example.com/image.jpg"
                }
            ],
            "total": 100.50,
            "payment_method": "plisio",
            "shipping_address": {
                "address": "123 Test St",
                "city": "Test City",
                "postal_code": "12345",
                "country": "US"
            },
            "phone": "+1234567890",
            "notes": "Test order for Plisio"
        }

        try:
            response = self.session.post(
                f"{self.api_base}/orders",
                json=test_order_payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )

            if response.status_code == 200:
                order_data = response.json()
                
                # Check required Plisio fields
                required_fields = ["plisio_invoice_id", "plisio_invoice_url"]
                optional_fields = ["plisio_qr_code", "plisio_wallet_hash"]
                
                missing_required = []
                present_optional = []
                
                for field in required_fields:
                    if field not in order_data or order_data[field] is None:
                        missing_required.append(field)
                
                for field in optional_fields:
                    if field in order_data and order_data[field] is not None:
                        present_optional.append(field)

                details = {
                    "order_id": order_data.get("id"),
                    "order_number": order_data.get("order_number"),
                    "plisio_invoice_id": order_data.get("plisio_invoice_id"),
                    "plisio_invoice_url": order_data.get("plisio_invoice_url"),
                    "plisio_qr_code": order_data.get("plisio_qr_code"),
                    "plisio_wallet_hash": order_data.get("plisio_wallet_hash"),
                    "present_optional_fields": present_optional
                }

                if missing_required:
                    self.log_result(
                        "Create Plisio Order", 
                        False, 
                        f"Missing required Plisio fields: {missing_required}",
                        details
                    )
                    return None
                else:
                    # Check if URL indicates demo mode
                    invoice_url = order_data.get("plisio_invoice_url", "")
                    is_demo = "demo_" in invoice_url
                    
                    details["demo_mode"] = is_demo
                    details["url_format"] = "Demo URL" if is_demo else "Production URL"
                    
                    self.log_result(
                        "Create Plisio Order", 
                        True, 
                        f"Order created successfully ({'Demo' if is_demo else 'Production'} mode)",
                        details
                    )
                    return order_data
            else:
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f": {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f": {response.text}"
                
                self.log_result("Create Plisio Order", False, error_msg)
                return None

        except Exception as e:
            self.log_result("Create Plisio Order", False, f"Request failed: {str(e)}")
            return None

    def test_get_order_by_id(self, order_id: str):
        """Test retrieving order by ID and verify Plisio fields"""
        try:
            response = self.session.get(f"{self.api_base}/orders/{order_id}", timeout=10)
            
            if response.status_code == 200:
                order_data = response.json()
                
                # Check Plisio fields are still present
                plisio_fields = {
                    "plisio_invoice_id": order_data.get("plisio_invoice_id"),
                    "plisio_invoice_url": order_data.get("plisio_invoice_url"),
                    "plisio_qr_code": order_data.get("plisio_qr_code"),
                    "plisio_wallet_hash": order_data.get("plisio_wallet_hash")
                }
                
                present_fields = {k: v for k, v in plisio_fields.items() if v is not None}
                
                details = {
                    "order_id": order_id,
                    "plisio_fields_present": list(present_fields.keys()),
                    **present_fields
                }
                
                if "plisio_invoice_id" in present_fields and "plisio_invoice_url" in present_fields:
                    self.log_result(
                        "Get Order by ID", 
                        True, 
                        "Order retrieved with Plisio fields intact",
                        details
                    )
                    return order_data
                else:
                    self.log_result(
                        "Get Order by ID", 
                        False, 
                        "Missing required Plisio fields in retrieved order",
                        details
                    )
                    return None
            else:
                self.log_result("Get Order by ID", False, f"HTTP {response.status_code}")
                return None
                
        except Exception as e:
            self.log_result("Get Order by ID", False, f"Request failed: {str(e)}")
            return None

    def check_plisio_demo_mode(self):
        """Check backend logs to determine if Plisio is in demo mode"""
        try:
            # Check the Plisio API key from backend .env
            with open('/app/backend/.env', 'r') as f:
                for line in f:
                    if line.startswith('PLISIO_API_KEY='):
                        api_key = line.split('=', 1)[1].strip().strip('"')
                        is_demo = api_key == 'your_plisio_api_key'
                        
                        details = {
                            "api_key_prefix": api_key[:20] + "..." if len(api_key) > 20 else api_key,
                            "is_demo_key": is_demo
                        }
                        
                        self.log_result(
                            "Plisio Mode Check", 
                            True, 
                            f"Plisio is in {'Demo' if is_demo else 'Production'} mode",
                            details
                        )
                        return is_demo
            
            self.log_result("Plisio Mode Check", False, "Could not find PLISIO_API_KEY in backend .env")
            return None
            
        except Exception as e:
            self.log_result("Plisio Mode Check", False, f"Error checking Plisio mode: {str(e)}")
            return None

    def validate_plisio_url_format(self, invoice_url: str, is_demo: bool):
        """Validate that the Plisio URL format matches the expected mode"""
        if is_demo:
            expected_pattern = "https://plisio.net/invoice/demo_"
            is_valid = invoice_url.startswith(expected_pattern)
            expected_msg = "Demo URL should start with 'https://plisio.net/invoice/demo_'"
        else:
            # For production, just check it's a valid Plisio URL
            is_valid = "plisio.net" in invoice_url and invoice_url.startswith("https://")
            expected_msg = "Production URL should be a valid Plisio invoice URL"
        
        details = {
            "invoice_url": invoice_url,
            "expected_format": expected_msg,
            "is_valid": is_valid
        }
        
        self.log_result(
            "Plisio URL Format", 
            is_valid, 
            f"URL format {'matches' if is_valid else 'does not match'} expected pattern",
            details
        )
        
        return is_valid

    def run_complete_test(self):
        """Run the complete Plisio payment flow test"""
        print("🚀 Starting Plisio Payment Flow Test")
        print("=" * 60)
        
        # Test 1: Backend Health Check
        if not self.test_backend_health():
            print("❌ Backend health check failed. Stopping tests.")
            return False
        
        # Test 2: Check Plisio Mode
        is_demo = self.check_plisio_demo_mode()
        
        # Test 3: Create Order with Plisio
        order_data = self.create_test_order_with_plisio()
        if not order_data:
            print("❌ Order creation failed. Stopping tests.")
            return False
        
        # Test 4: Validate URL format
        invoice_url = order_data.get("plisio_invoice_url")
        if invoice_url and is_demo is not None:
            self.validate_plisio_url_format(invoice_url, is_demo)
        
        # Test 5: Retrieve Order by ID
        order_id = order_data.get("id")
        if order_id:
            retrieved_order = self.test_get_order_by_id(order_id)
        
        # Summary
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n🔍 FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  • {result['test']}: {result['message']}")
        
        return failed_tests == 0

def main():
    """Main test execution"""
    try:
        tester = PlisioPaymentTester()
        success = tester.run_complete_test()
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()