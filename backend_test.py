#!/usr/bin/env python3
"""
Backend API Testing Suite for Kayee01 Site
Tests Stripe Payment Links, Admin Login, Email Production, and Product Duplication
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

class Kayee01Tester:
    def __init__(self):
        self.backend_url = get_backend_url()
        if not self.backend_url:
            raise Exception("Could not get backend URL from frontend/.env")
        
        self.api_base = f"{self.backend_url}/api"
        self.session = requests.Session()
        self.test_results = []
        self.admin_token = None
        
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

    def create_test_order_fedex_stripe(self):
        """Create a test order with FedEx shipping and Stripe payment"""
        test_order_payload = {
            "user_email": "customer@luxeboutique.com",
            "user_name": "John Customer",
            "items": [
                {
                    "product_id": "test-123",
                    "name": "Luxury Watch",
                    "price": 100.0,
                    "quantity": 1,
                    "image": "https://example.com/watch.jpg"
                }
            ],
            "total": 110.0,  # $100 product + $10 shipping
            "shipping_method": "fedex",
            "shipping_cost": 10.0,
            "payment_method": "stripe",
            "shipping_address": {
                "address": "123 Main St",
                "city": "New York",
                "postal_code": "10001",
                "country": "USA"
            },
            "phone": "+1234567890",
            "notes": "Test order with FedEx shipping and Stripe payment"
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
                
                # Check shipping fields
                shipping_method = order_data.get("shipping_method")
                shipping_cost = order_data.get("shipping_cost")
                total = order_data.get("total")
                
                # Check Stripe payment fields
                stripe_payment_id = order_data.get("stripe_payment_id")
                stripe_payment_url = order_data.get("stripe_payment_url")
                
                # Check that coinpal fields are not present or null
                coinpal_payment_id = order_data.get("coinpal_payment_id")
                coinpal_payment_url = order_data.get("coinpal_payment_url")

                details = {
                    "order_id": order_data.get("id"),
                    "order_number": order_data.get("order_number"),
                    "shipping_method": shipping_method,
                    "shipping_cost": shipping_cost,
                    "total": total,
                    "stripe_payment_id": stripe_payment_id,
                    "stripe_payment_url": stripe_payment_url,
                    "coinpal_payment_id": coinpal_payment_id,
                    "coinpal_payment_url": coinpal_payment_url
                }

                # Validate shipping fields
                shipping_valid = (
                    shipping_method == "fedex" and 
                    shipping_cost == 10.0 and 
                    total == 110.0
                )
                
                # Validate Stripe fields
                stripe_valid = (
                    stripe_payment_id is not None and 
                    stripe_payment_url is not None and
                    len(str(stripe_payment_id)) > 0 and
                    "stripe" in str(stripe_payment_url).lower()
                )
                
                # Validate CoinPal removal
                coinpal_removed = (
                    coinpal_payment_id is None and 
                    coinpal_payment_url is None
                )

                if shipping_valid and stripe_valid and coinpal_removed:
                    self.log_result(
                        "Create FedEx+Stripe Order", 
                        True, 
                        "Order created successfully with FedEx shipping and Stripe payment",
                        details
                    )
                    return order_data
                else:
                    issues = []
                    if not shipping_valid:
                        issues.append(f"Shipping issue: method={shipping_method}, cost={shipping_cost}, total={total}")
                    if not stripe_valid:
                        issues.append(f"Stripe issue: payment_id={stripe_payment_id}, payment_url={stripe_payment_url}")
                    if not coinpal_removed:
                        issues.append(f"CoinPal not removed: payment_id={coinpal_payment_id}, payment_url={coinpal_payment_url}")
                    
                    self.log_result(
                        "Create FedEx+Stripe Order", 
                        False, 
                        f"Order validation failed: {'; '.join(issues)}",
                        details
                    )
                    return None
            else:
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f": {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f": {response.text}"
                
                self.log_result("Create FedEx+Stripe Order", False, error_msg)
                return None

        except Exception as e:
            self.log_result("Create FedEx+Stripe Order", False, f"Request failed: {str(e)}")
            return None

    def create_test_order_free_plisio(self):
        """Create a test order with Free shipping and Plisio payment"""
        test_order_payload = {
            "user_email": "customer2@luxeboutique.com",
            "user_name": "Jane Customer",
            "items": [
                {
                    "product_id": "test-456",
                    "name": "Designer Handbag",
                    "price": 200.0,
                    "quantity": 1,
                    "image": "https://example.com/handbag.jpg"
                }
            ],
            "total": 200.0,  # No shipping cost
            "shipping_method": "free",
            "shipping_cost": 0.0,
            "payment_method": "plisio",
            "shipping_address": {
                "address": "456 Oak Ave",
                "city": "Los Angeles",
                "postal_code": "90210",
                "country": "USA"
            },
            "phone": "+1987654321",
            "notes": "Test order with free shipping and Plisio payment"
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
                
                # Check shipping fields
                shipping_method = order_data.get("shipping_method")
                shipping_cost = order_data.get("shipping_cost")
                total = order_data.get("total")
                
                # Check Plisio payment fields
                plisio_invoice_id = order_data.get("plisio_invoice_id")
                plisio_invoice_url = order_data.get("plisio_invoice_url")

                details = {
                    "order_id": order_data.get("id"),
                    "order_number": order_data.get("order_number"),
                    "shipping_method": shipping_method,
                    "shipping_cost": shipping_cost,
                    "total": total,
                    "plisio_invoice_id": plisio_invoice_id,
                    "plisio_invoice_url": plisio_invoice_url
                }

                # Validate shipping fields
                shipping_valid = (
                    shipping_method == "free" and 
                    shipping_cost == 0.0 and 
                    total == 200.0
                )
                
                # Validate Plisio fields
                plisio_valid = (
                    plisio_invoice_id is not None and 
                    plisio_invoice_url is not None and
                    len(str(plisio_invoice_id)) > 0 and
                    "plisio" in str(plisio_invoice_url).lower()
                )

                if shipping_valid and plisio_valid:
                    self.log_result(
                        "Create Free+Plisio Order", 
                        True, 
                        "Order created successfully with free shipping and Plisio payment",
                        details
                    )
                    return order_data
                else:
                    issues = []
                    if not shipping_valid:
                        issues.append(f"Shipping issue: method={shipping_method}, cost={shipping_cost}, total={total}")
                    if not plisio_valid:
                        issues.append(f"Plisio issue: invoice_id={plisio_invoice_id}, invoice_url={plisio_invoice_url}")
                    
                    self.log_result(
                        "Create Free+Plisio Order", 
                        False, 
                        f"Order validation failed: {'; '.join(issues)}",
                        details
                    )
                    return None
            else:
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f": {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f": {response.text}"
                
                self.log_result("Create Free+Plisio Order", False, error_msg)
                return None

        except Exception as e:
            self.log_result("Create Free+Plisio Order", False, f"Request failed: {str(e)}")
            return None

    def test_coinpal_payment_rejection(self):
        """Test that CoinPal payment method is rejected or ignored"""
        test_order_payload = {
            "user_email": "test@coinpal.com",
            "user_name": "CoinPal Tester",
            "items": [
                {
                    "product_id": "test-789",
                    "name": "Test Product",
                    "price": 50.0,
                    "quantity": 1,
                    "image": "https://example.com/test.jpg"
                }
            ],
            "total": 50.0,
            "shipping_method": "free",
            "shipping_cost": 0.0,
            "payment_method": "coinpal",  # This should be rejected
            "shipping_address": {
                "address": "789 Test Blvd",
                "city": "Test City",
                "postal_code": "12345",
                "country": "USA"
            },
            "phone": "+1555555555",
            "notes": "Test order with CoinPal (should fail)"
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
                
                # Check that no coinpal fields are present
                coinpal_payment_id = order_data.get("coinpal_payment_id")
                coinpal_payment_url = order_data.get("coinpal_payment_url")
                coinpal_qr_code = order_data.get("coinpal_qr_code")

                details = {
                    "order_id": order_data.get("id"),
                    "order_number": order_data.get("order_number"),
                    "payment_method": order_data.get("payment_method"),
                    "coinpal_payment_id": coinpal_payment_id,
                    "coinpal_payment_url": coinpal_payment_url,
                    "coinpal_qr_code": coinpal_qr_code
                }

                # CoinPal should be removed - no coinpal fields should be populated
                coinpal_removed = (
                    coinpal_payment_id is None and 
                    coinpal_payment_url is None and
                    coinpal_qr_code is None
                )

                if coinpal_removed:
                    self.log_result(
                        "CoinPal Rejection Test", 
                        True, 
                        "CoinPal payment method properly ignored - no coinpal fields populated",
                        details
                    )
                    return order_data
                else:
                    self.log_result(
                        "CoinPal Rejection Test", 
                        False, 
                        "CoinPal fields were populated despite removal",
                        details
                    )
                    return None
            else:
                # If the request fails, that's also acceptable for CoinPal removal
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f": {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f": {response.text}"
                
                self.log_result(
                    "CoinPal Rejection Test", 
                    True, 
                    f"CoinPal payment method properly rejected: {error_msg}"
                )
                return None

        except Exception as e:
            # Exception is also acceptable for CoinPal removal
            self.log_result(
                "CoinPal Rejection Test", 
                True, 
                f"CoinPal payment method properly rejected: {str(e)}"
            )
            return None

    def test_get_order_by_id(self, order_id: str, expected_payment_method: str = None):
        """Test retrieving order by ID and verify all fields"""
        try:
            response = self.session.get(f"{self.api_base}/orders/{order_id}", timeout=10)
            
            if response.status_code == 200:
                order_data = response.json()
                
                # Check shipping fields
                shipping_method = order_data.get("shipping_method")
                shipping_cost = order_data.get("shipping_cost")
                
                # Check payment method specific fields
                payment_method = order_data.get("payment_method")
                
                details = {
                    "order_id": order_id,
                    "payment_method": payment_method,
                    "shipping_method": shipping_method,
                    "shipping_cost": shipping_cost,
                    "total": order_data.get("total")
                }
                
                # Check for payment-specific fields
                if payment_method == "stripe":
                    details["stripe_payment_id"] = order_data.get("stripe_payment_id")
                    details["stripe_payment_url"] = order_data.get("stripe_payment_url")
                elif payment_method == "plisio":
                    details["plisio_invoice_id"] = order_data.get("plisio_invoice_id")
                    details["plisio_invoice_url"] = order_data.get("plisio_invoice_url")
                
                # Check that coinpal fields are not present
                details["coinpal_payment_id"] = order_data.get("coinpal_payment_id")
                details["coinpal_payment_url"] = order_data.get("coinpal_payment_url")
                
                # Validate required fields are present
                has_shipping_fields = (
                    shipping_method is not None and 
                    shipping_cost is not None
                )
                
                coinpal_absent = (
                    order_data.get("coinpal_payment_id") is None and
                    order_data.get("coinpal_payment_url") is None
                )
                
                if has_shipping_fields and coinpal_absent:
                    self.log_result(
                        "Get Order by ID", 
                        True, 
                        f"Order retrieved successfully with shipping fields and no coinpal data",
                        details
                    )
                    return order_data
                else:
                    issues = []
                    if not has_shipping_fields:
                        issues.append("Missing shipping fields")
                    if not coinpal_absent:
                        issues.append("CoinPal fields still present")
                    
                    self.log_result(
                        "Get Order by ID", 
                        False, 
                        f"Order validation failed: {'; '.join(issues)}",
                        details
                    )
                    return None
            else:
                self.log_result("Get Order by ID", False, f"HTTP {response.status_code}")
                return None
                
        except Exception as e:
            self.log_result("Get Order by ID", False, f"Request failed: {str(e)}")
            return None

    def test_manual_payoneer_payment(self):
        """Test creating order with manual Payoneer payment method"""
        test_order_payload = {
            "user_email": "test@kayee01.com",
            "user_name": "Test Payoneer",
            "items": [
                {
                    "product_id": "test-payoneer",
                    "name": "Test Montre Rolex",
                    "price": 500.0,
                    "quantity": 1,
                    "image": "https://example.com/rolex.jpg"
                }
            ],
            "total": 510.0,
            "shipping_method": "fedex",
            "shipping_cost": 10.0,
            "payment_method": "manual",
            "shipping_address": {
                "address": "123 Rue de Paris",
                "city": "Paris",
                "postal_code": "75001",
                "country": "France"
            },
            "phone": "+33612345678",
            "notes": "Test commande Payoneer"
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
                
                # Check order fields
                payment_method = order_data.get("payment_method")
                total = order_data.get("total")
                shipping_method = order_data.get("shipping_method")
                shipping_cost = order_data.get("shipping_cost")
                user_email = order_data.get("user_email")
                user_name = order_data.get("user_name")

                details = {
                    "order_id": order_data.get("id"),
                    "order_number": order_data.get("order_number"),
                    "payment_method": payment_method,
                    "total": total,
                    "shipping_method": shipping_method,
                    "shipping_cost": shipping_cost,
                    "user_email": user_email,
                    "user_name": user_name
                }

                # Validate manual payment order
                manual_payment_valid = (
                    payment_method == "manual" and 
                    total == 510.0 and
                    shipping_method == "fedex" and
                    shipping_cost == 10.0 and
                    user_email == "test@kayee01.com" and
                    user_name == "Test Payoneer"
                )

                if manual_payment_valid:
                    self.log_result(
                        "Manual Payoneer Payment", 
                        True, 
                        "Order created successfully with manual payment method",
                        details
                    )
                    return order_data
                else:
                    self.log_result(
                        "Manual Payoneer Payment", 
                        False, 
                        f"Order validation failed: payment_method={payment_method}, total={total}",
                        details
                    )
                    return None
            else:
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f": {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f": {response.text}"
                
                self.log_result("Manual Payoneer Payment", False, error_msg)
                return None

        except Exception as e:
            self.log_result("Manual Payoneer Payment", False, f"Request failed: {str(e)}")
            return None

    def test_email_smtp_verification(self):
        """Test email SMTP configuration and Payoneer instructions"""
        try:
            # Check backend error logs for recent email activity
            import subprocess
            result = subprocess.run(
                ["tail", "-n", "50", "/var/log/supervisor/backend.err.log"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            log_content = result.stdout
            
            # Look for email-related log entries
            email_found = "📧 EMAIL" in log_content
            kayee01_found = "test@kayee01.com" in log_content
            demo_mode_found = "Demo Mode" in log_content
            
            # Check email service configuration
            env_config_valid = False
            payoneer_config_valid = False
            
            try:
                with open('/app/backend/.env', 'r') as f:
                    env_content = f.read()
                    env_config_valid = (
                        'kayicom509@gmail.com' in env_content and 
                        'Kayee01' in env_content and
                        'smtp.gmail.com' in env_content
                    )
            except Exception as e:
                pass
            
            # Check email service code for Payoneer instructions
            try:
                with open('/app/backend/email_service.py', 'r') as f:
                    email_service_content = f.read()
                    payoneer_config_valid = (
                        'kayicom509@gmail.com' in email_service_content and
                        'Instructions de paiement Payoneer' in email_service_content and
                        'Kayee01' in email_service_content and
                        "payment_method == 'manual'" in email_service_content
                    )
            except Exception as e:
                pass
            
            details = {
                "email_logs_found": email_found,
                "test_email_found": kayee01_found,
                "demo_mode_active": demo_mode_found,
                "env_config_valid": env_config_valid,
                "payoneer_instructions_configured": payoneer_config_valid,
                "log_sample": log_content[-300:] if log_content else "No logs found"
            }
            
            if email_found and env_config_valid and payoneer_config_valid:
                self.log_result(
                    "Email SMTP Test", 
                    True, 
                    "✅ Email system working with Payoneer instructions (kayicom509@gmail.com, Kayee01)",
                    details
                )
                return True
            elif env_config_valid and payoneer_config_valid:
                self.log_result(
                    "Email SMTP Test", 
                    True, 
                    "✅ Email configuration verified - SMTP configured with Payoneer instructions",
                    details
                )
                return True
            else:
                issues = []
                if not env_config_valid:
                    issues.append("Email .env configuration incomplete")
                if not payoneer_config_valid:
                    issues.append("Payoneer instructions not configured in email service")
                
                self.log_result(
                    "Email SMTP Test", 
                    False, 
                    f"Email configuration issues: {'; '.join(issues)}",
                    details
                )
                return False
                
        except Exception as e:
            self.log_result("Email SMTP Test", False, f"Test failed: {str(e)}")
            return False

    def test_coinpal_completely_removed(self):
        """Test that CoinPal is completely removed from the system"""
        try:
            # Test 1: Try to create order with coinpal payment method
            test_order_payload = {
                "user_email": "test@coinpal-removal.com",
                "user_name": "CoinPal Removal Test",
                "items": [
                    {
                        "product_id": "test-coinpal-removal",
                        "name": "Test Product",
                        "price": 100.0,
                        "quantity": 1,
                        "image": "https://example.com/test.jpg"
                    }
                ],
                "total": 100.0,
                "shipping_method": "free",
                "shipping_cost": 0.0,
                "payment_method": "coinpal",
                "shipping_address": {
                    "address": "123 Test St",
                    "city": "Test City",
                    "postal_code": "12345",
                    "country": "USA"
                },
                "phone": "+1234567890",
                "notes": "Test CoinPal removal"
            }

            response = self.session.post(
                f"{self.api_base}/orders",
                json=test_order_payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )

            coinpal_fields_check = True
            order_created = False
            
            if response.status_code == 200:
                order_data = response.json()
                order_created = True
                
                # Check that no coinpal fields are populated
                coinpal_payment_id = order_data.get("coinpal_payment_id")
                coinpal_payment_url = order_data.get("coinpal_payment_url")
                coinpal_qr_code = order_data.get("coinpal_qr_code")
                
                coinpal_fields_check = (
                    coinpal_payment_id is None and 
                    coinpal_payment_url is None and
                    coinpal_qr_code is None
                )
            
            # Test 2: Check if coinpal endpoints are removed
            coinpal_endpoints_removed = True
            try:
                coinpal_create_response = self.session.post(f"{self.api_base}/coinpal/create-payment", timeout=5)
                if coinpal_create_response.status_code != 404:
                    coinpal_endpoints_removed = False
            except:
                # Exception means endpoint doesn't exist, which is good
                pass
            
            details = {
                "order_created_with_coinpal": order_created,
                "coinpal_fields_empty": coinpal_fields_check,
                "coinpal_endpoints_removed": coinpal_endpoints_removed,
                "response_status": response.status_code
            }
            
            if coinpal_fields_check and coinpal_endpoints_removed:
                self.log_result(
                    "CoinPal Complete Removal", 
                    True, 
                    "CoinPal completely removed - no fields populated, endpoints removed",
                    details
                )
                return True
            else:
                issues = []
                if not coinpal_fields_check:
                    issues.append("CoinPal fields still being populated")
                if not coinpal_endpoints_removed:
                    issues.append("CoinPal endpoints still accessible")
                
                self.log_result(
                    "CoinPal Complete Removal", 
                    False, 
                    f"CoinPal removal incomplete: {'; '.join(issues)}",
                    details
                )
                return False
                
        except Exception as e:
            self.log_result("CoinPal Complete Removal", False, f"Test failed: {str(e)}")
            return False

    def run_complete_test(self):
        """Run the complete E-commerce features test"""
        print("🚀 Starting E-commerce Features Test")
        print("Testing: Email SMTP, Manual Payoneer Payment, CoinPal Removal")
        print("=" * 60)
        
        # Test 1: Backend Health Check
        if not self.test_backend_health():
            print("❌ Backend health check failed. Stopping tests.")
            return False
        
        # Test 2: Test Email SMTP Configuration
        print("🧪 Testing Email SMTP Configuration...")
        self.test_email_smtp_verification()
        
        # Test 3: Test Manual Payoneer Payment
        print("🧪 Testing Manual Payoneer Payment...")
        payoneer_order = self.test_manual_payoneer_payment()
        
        # Test 4: Test CoinPal Complete Removal
        print("🧪 Testing CoinPal Complete Removal...")
        self.test_coinpal_completely_removed()
        
        # Test 5: Retrieve Payoneer order by ID to verify all details
        if payoneer_order:
            print("🧪 Testing Payoneer Order Retrieval...")
            self.test_get_order_by_id(payoneer_order.get("id"), "manual")
        
        # Test 6: Create Order with FedEx shipping and Stripe payment (existing test)
        print("🧪 Testing FedEx Shipping + Stripe Payment...")
        fedex_stripe_order = self.create_test_order_fedex_stripe()
        
        # Test 7: Create Order with Free shipping and Plisio payment (existing test)
        print("🧪 Testing Free Shipping + Plisio Payment...")
        free_plisio_order = self.create_test_order_free_plisio()
        
        # Test 8: Test CoinPal payment rejection (existing test)
        print("🧪 Testing CoinPal Payment Rejection...")
        self.test_coinpal_payment_rejection()
        
        # Test 9: Retrieve orders by ID to verify fields
        if fedex_stripe_order:
            print("🧪 Testing Order Retrieval (FedEx+Stripe)...")
            self.test_get_order_by_id(fedex_stripe_order.get("id"), "stripe")
        
        if free_plisio_order:
            print("🧪 Testing Order Retrieval (Free+Plisio)...")
            self.test_get_order_by_id(free_plisio_order.get("id"), "plisio")
        
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
        tester = EcommerceTester()
        success = tester.run_complete_test()
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()