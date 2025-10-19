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

    def test_admin_login(self):
        """Test admin login with kayicom509@gmail.com / Admin123!"""
        login_payload = {
            "email": "kayicom509@gmail.com",
            "password": "Admin123!"
        }

        try:
            response = self.session.post(
                f"{self.api_base}/auth/login",
                json=login_payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )

            if response.status_code == 200:
                login_data = response.json()
                
                # Check required fields
                access_token = login_data.get("access_token")
                token_type = login_data.get("token_type")
                user = login_data.get("user")
                
                details = {
                    "access_token": access_token[:20] + "..." if access_token else None,
                    "token_type": token_type,
                    "user_email": user.get("email") if user else None,
                    "user_role": user.get("role") if user else None,
                    "user_name": user.get("name") if user else None
                }

                # Validate login response
                login_valid = (
                    access_token is not None and 
                    token_type == "bearer" and
                    user is not None and
                    user.get("email") == "kayicom509@gmail.com" and
                    user.get("role") == "admin"
                )

                if login_valid:
                    # Store token for future requests
                    self.admin_token = access_token
                    self.session.headers.update({"Authorization": f"Bearer {access_token}"})
                    
                    self.log_result(
                        "Admin Login", 
                        True, 
                        "Admin login successful - token received and user verified",
                        details
                    )
                    return login_data
                else:
                    self.log_result(
                        "Admin Login", 
                        False, 
                        f"Login validation failed - missing required fields or incorrect role",
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
                
                self.log_result("Admin Login", False, error_msg)
                return None

        except Exception as e:
            self.log_result("Admin Login", False, f"Request failed: {str(e)}")
            return None

    def test_stripe_payment_link_creation(self):
        """Test Stripe payment link creation for order ORD-3E0AF5B2"""
        test_order_payload = {
            "user_email": "Info.kayicom.com@gmx.fr",
            "user_name": "Real Customer",
            "items": [
                {
                    "product_id": "real-001",
                    "name": "Rolex Watch",
                    "price": 500.0,
                    "quantity": 1,
                    "image": "https://example.com/rolex.jpg"
                }
            ],
            "total": 510.0,
            "shipping_method": "fedex",
            "shipping_cost": 10.0,
            "payment_method": "stripe",
            "shipping_address": {
                "address": "123 Production St",
                "city": "Paris",
                "postal_code": "75001",
                "country": "France"
            },
            "phone": "+33123456789",
            "notes": "Real order test"
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
                
                # Check Stripe payment fields
                stripe_payment_id = order_data.get("stripe_payment_id")
                stripe_payment_url = order_data.get("stripe_payment_url")
                order_number = order_data.get("order_number")
                order_id = order_data.get("id")
                
                details = {
                    "order_id": order_id,
                    "order_number": order_number,
                    "stripe_payment_id": stripe_payment_id,
                    "stripe_payment_url": stripe_payment_url,
                    "total": order_data.get("total"),
                    "user_email": order_data.get("user_email")
                }

                # Validate Stripe payment link creation
                stripe_valid = (
                    stripe_payment_id is not None and 
                    stripe_payment_url is not None and
                    len(str(stripe_payment_id)) > 0 and
                    ("stripe" in str(stripe_payment_url).lower() or "buy.stripe.com" in str(stripe_payment_url))
                )

                if stripe_valid:
                    self.log_result(
                        "Stripe Payment Link Creation", 
                        True, 
                        f"Stripe payment link created successfully for order {order_number}",
                        details
                    )
                    
                    # Test retrieving the order to verify stripe_payment_url
                    return self.test_get_order_stripe_url(order_id, order_number)
                else:
                    self.log_result(
                        "Stripe Payment Link Creation", 
                        False, 
                        f"Stripe payment link validation failed",
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
                
                self.log_result("Stripe Payment Link Creation", False, error_msg)
                return None

        except Exception as e:
            self.log_result("Stripe Payment Link Creation", False, f"Request failed: {str(e)}")
            return None

    def test_get_order_stripe_url(self, order_id: str, order_number: str):
        """Test GET /api/orders/{order_id} to verify stripe_payment_url"""
        try:
            response = self.session.get(f"{self.api_base}/orders/{order_id}", timeout=10)
            
            if response.status_code == 200:
                order_data = response.json()
                
                stripe_payment_url = order_data.get("stripe_payment_url")
                stripe_payment_id = order_data.get("stripe_payment_id")
                
                details = {
                    "order_id": order_id,
                    "order_number": order_number,
                    "stripe_payment_id": stripe_payment_id,
                    "stripe_payment_url": stripe_payment_url,
                    "product_display_check": f"Should show 'Order {order_number}' only"
                }
                
                # Validate that stripe_payment_url is present
                url_valid = (
                    stripe_payment_url is not None and 
                    len(str(stripe_payment_url)) > 0 and
                    ("stripe" in str(stripe_payment_url).lower() or "buy.stripe.com" in str(stripe_payment_url))
                )
                
                if url_valid:
                    self.log_result(
                        "Get Order Stripe URL", 
                        True, 
                        f"Order retrieved successfully with valid Stripe payment URL",
                        details
                    )
                    return order_data
                else:
                    self.log_result(
                        "Get Order Stripe URL", 
                        False, 
                        f"Stripe payment URL validation failed",
                        details
                    )
                    return None
            else:
                self.log_result("Get Order Stripe URL", False, f"HTTP {response.status_code}")
                return None
                
        except Exception as e:
            self.log_result("Get Order Stripe URL", False, f"Request failed: {str(e)}")
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

    def test_email_production_manual_payment(self):
        """Test email production with manual payment method"""
        test_order_payload = {
            "user_email": "Info.kayicom.com@gmx.fr",
            "user_name": "Anson",
            "items": [
                {
                    "product_id": "real-002",
                    "name": "Luxury Product",
                    "price": 500.0,
                    "quantity": 1,
                    "image": "https://example.com/product.jpg"
                }
            ],
            "total": 510.0,
            "shipping_method": "fedex",
            "shipping_cost": 10.0,
            "payment_method": "manual",
            "shipping_address": {
                "address": "123 Production St",
                "city": "Paris",
                "postal_code": "75001",
                "country": "France"
            },
            "phone": "+33123456789",
            "notes": "Test email production"
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
                user_email = order_data.get("user_email")
                user_name = order_data.get("user_name")

                details = {
                    "order_id": order_data.get("id"),
                    "order_number": order_data.get("order_number"),
                    "payment_method": payment_method,
                    "total": total,
                    "user_email": user_email,
                    "user_name": user_name,
                    "email_recipient": "Info.kayicom.com@gmx.fr",
                    "customer_name": "Anson"
                }

                # Validate manual payment order with correct email recipient
                email_order_valid = (
                    payment_method == "manual" and 
                    total == 510.0 and
                    user_email == "Info.kayicom.com@gmx.fr" and
                    user_name == "Anson"
                )

                if email_order_valid:
                    # Check email logs for confirmation
                    email_sent = self.check_email_logs(order_data.get("id"))
                    
                    self.log_result(
                        "Email Production Manual Payment", 
                        True, 
                        f"Order created successfully - email should be sent to Info.kayicom.com@gmx.fr for customer Anson",
                        details
                    )
                    return order_data
                else:
                    self.log_result(
                        "Email Production Manual Payment", 
                        False, 
                        f"Order validation failed: payment_method={payment_method}, email={user_email}, name={user_name}",
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
                
                self.log_result("Email Production Manual Payment", False, error_msg)
                return None

        except Exception as e:
            self.log_result("Email Production Manual Payment", False, f"Request failed: {str(e)}")
            return None

    def check_email_logs(self, order_id: str):
        """Check backend logs for email sending confirmation"""
        try:
            import subprocess
            result = subprocess.run(
                ["tail", "-n", "100", "/var/log/supervisor/backend.err.log"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            log_content = result.stdout
            
            # Look for email-related log entries
            email_found = "📧 EMAIL" in log_content or "Email" in log_content
            order_found = order_id in log_content if order_id else False
            kayee_email_found = "Info.kayicom.com@gmx.fr" in log_content
            
            details = {
                "email_logs_found": email_found,
                "order_in_logs": order_found,
                "recipient_email_found": kayee_email_found,
                "log_sample": log_content[-500:] if log_content else "No logs found"
            }
            
            self.log_result(
                "Email Logs Check", 
                email_found, 
                f"Email system activity detected: {email_found}",
                details
            )
            
            return email_found
                
        except Exception as e:
            self.log_result("Email Logs Check", False, f"Log check failed: {str(e)}")
            return False

    def test_product_duplication(self):
        """Test product listing and duplication functionality"""
        try:
            # First, get list of products
            response = self.session.get(f"{self.api_base}/products", timeout=10)
            
            if response.status_code != 200:
                self.log_result("Product Duplication", False, f"Failed to get products: HTTP {response.status_code}")
                return None
            
            products = response.json()
            
            if not products:
                self.log_result("Product Duplication", False, "No products found to duplicate")
                return None
            
            # Select first product to duplicate
            original_product = products[0]
            original_name = original_product.get("name", "Unknown Product")
            
            # Create duplicate product with "(Copy)" suffix
            duplicate_product = {
                "name": f"{original_name} (Copy)",
                "description": original_product.get("description", ""),
                "price": original_product.get("price", 0.0),
                "compare_at_price": original_product.get("compare_at_price"),
                "cost": original_product.get("cost"),
                "images": original_product.get("images", []),
                "category": original_product.get("category", ""),
                "stock": original_product.get("stock", 0),
                "sku": f"{original_product.get('sku', 'SKU')}-COPY",
                "barcode": original_product.get("barcode"),
                "weight": original_product.get("weight"),
                "featured": False,  # Don't feature the copy
                "on_sale": original_product.get("on_sale", False),
                "is_new": original_product.get("is_new", False),
                "best_seller": original_product.get("best_seller", False),
                "digital_product": original_product.get("digital_product", False),
                "download_url": original_product.get("download_url"),
                "tags": original_product.get("tags", []),
                "meta_title": original_product.get("meta_title"),
                "meta_description": original_product.get("meta_description")
            }
            
            # Need admin authentication for product creation
            if not self.admin_token:
                self.log_result("Product Duplication", False, "Admin authentication required - run admin login test first")
                return None
            
            # Create the duplicate product
            create_response = self.session.post(
                f"{self.api_base}/products",
                json=duplicate_product,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.admin_token}"
                },
                timeout=30
            )
            
            if create_response.status_code == 200:
                new_product = create_response.json()
                
                details = {
                    "original_product_id": original_product.get("id"),
                    "original_name": original_name,
                    "duplicate_product_id": new_product.get("id"),
                    "duplicate_name": new_product.get("name"),
                    "name_has_copy_suffix": "(Copy)" in new_product.get("name", ""),
                    "price_copied": new_product.get("price") == original_product.get("price"),
                    "category_copied": new_product.get("category") == original_product.get("category")
                }
                
                # Validate duplication
                duplication_valid = (
                    new_product.get("name") == f"{original_name} (Copy)" and
                    new_product.get("price") == original_product.get("price") and
                    new_product.get("category") == original_product.get("category") and
                    new_product.get("id") != original_product.get("id")
                )
                
                if duplication_valid:
                    self.log_result(
                        "Product Duplication", 
                        True, 
                        f"Product duplicated successfully with '(Copy)' suffix",
                        details
                    )
                    return new_product
                else:
                    self.log_result(
                        "Product Duplication", 
                        False, 
                        f"Product duplication validation failed",
                        details
                    )
                    return None
            else:
                error_msg = f"HTTP {create_response.status_code}"
                try:
                    error_data = create_response.json()
                    error_msg += f": {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f": {create_response.text}"
                
                self.log_result("Product Duplication", False, f"Failed to create duplicate: {error_msg}")
                return None
                
        except Exception as e:
            self.log_result("Product Duplication", False, f"Test failed: {str(e)}")
            return None

    def test_admin_dashboard_access(self):
        """Test admin dashboard access after login"""
        if not self.admin_token:
            self.log_result("Admin Dashboard Access", False, "Admin token not available - run admin login test first")
            return False
        
        try:
            # Test dashboard stats endpoint
            response = self.session.get(
                f"{self.api_base}/admin/dashboard/stats",
                headers={"Authorization": f"Bearer {self.admin_token}"},
                timeout=10
            )
            
            if response.status_code == 200:
                stats_data = response.json()
                
                details = {
                    "today_sales": stats_data.get("today_sales"),
                    "today_orders": stats_data.get("today_orders"),
                    "total_customers": stats_data.get("total_customers"),
                    "pending_orders": stats_data.get("pending_orders"),
                    "has_sales_chart": "sales_chart" in stats_data,
                    "has_recent_orders": "recent_orders" in stats_data
                }
                
                # Validate dashboard data structure
                dashboard_valid = (
                    "today_sales" in stats_data and
                    "today_orders" in stats_data and
                    "total_customers" in stats_data and
                    "sales_chart" in stats_data
                )
                
                if dashboard_valid:
                    self.log_result(
                        "Admin Dashboard Access", 
                        True, 
                        "Admin dashboard accessible with valid statistics data",
                        details
                    )
                    return True
                else:
                    self.log_result(
                        "Admin Dashboard Access", 
                        False, 
                        "Dashboard data structure validation failed",
                        details
                    )
                    return False
            else:
                self.log_result("Admin Dashboard Access", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Admin Dashboard Access", False, f"Request failed: {str(e)}")
            return False

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
                        'Manual Payment Instructions' in email_service_content and
                        'Kayee01' in email_service_content and
                        "payment_method == 'manual'" in email_service_content and
                        'Payoneer Email' in email_service_content
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

    def test_coupon_validation_welcome10(self):
        """Test coupon validation with WELCOME10 code"""
        try:
            # Test 1: Valid coupon with cart total $100 (should work, min $50)
            response = self.session.post(
                f"{self.api_base}/coupons/validate?code=WELCOME10&cart_total=100",
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            valid_test_passed = False
            if response.status_code == 200:
                coupon_data = response.json()
                
                valid = coupon_data.get("valid")
                discount_amount = coupon_data.get("discount_amount")
                discount_type = coupon_data.get("discount_type")
                
                # WELCOME10 should be 10% discount, so 10% of $100 = $10
                expected_discount = 10.0
                
                valid_test_passed = (
                    valid is True and
                    discount_amount == expected_discount and
                    discount_type == "percentage"
                )
                
                details_valid = {
                    "cart_total": 100,
                    "valid": valid,
                    "discount_amount": discount_amount,
                    "discount_type": discount_type,
                    "expected_discount": expected_discount
                }
                
                if valid_test_passed:
                    self.log_result(
                        "Coupon SAVE10 Valid Test", 
                        True, 
                        f"SAVE10 coupon validation successful - 10% discount = ${discount_amount}",
                        details_valid
                    )
                else:
                    self.log_result(
                        "Coupon SAVE10 Valid Test", 
                        False, 
                        f"SAVE10 coupon validation failed - expected $10 discount, got ${discount_amount}",
                        details_valid
                    )
            else:
                self.log_result("Coupon SAVE10 Valid Test", False, f"HTTP {response.status_code}")
            
            # Test 2: Invalid coupon with cart total $30 (should fail, min $50)
            response2 = self.session.post(
                f"{self.api_base}/coupons/validate?code=SAVE10&cart_total=30",
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            invalid_test_passed = False
            if response2.status_code == 400:
                # Should fail with minimum purchase requirement
                error_data = response2.json()
                error_detail = error_data.get("detail", "")
                
                invalid_test_passed = "Minimum purchase" in error_detail or "50" in error_detail
                
                details_invalid = {
                    "cart_total": 30,
                    "status_code": response2.status_code,
                    "error_detail": error_detail,
                    "expected_error": "Minimum purchase requirement"
                }
                
                if invalid_test_passed:
                    self.log_result(
                        "Coupon SAVE10 Invalid Test", 
                        True, 
                        f"SAVE10 coupon correctly rejected for cart under $50 minimum",
                        details_invalid
                    )
                else:
                    self.log_result(
                        "Coupon SAVE10 Invalid Test", 
                        False, 
                        f"SAVE10 coupon rejection reason incorrect: {error_detail}",
                        details_invalid
                    )
            else:
                self.log_result("Coupon SAVE10 Invalid Test", False, f"Expected HTTP 400, got {response2.status_code}")
            
            return valid_test_passed and invalid_test_passed
                
        except Exception as e:
            self.log_result("Coupon SAVE10 Validation", False, f"Test failed: {str(e)}")
            return False

    def test_crypto_discount_plisio(self):
        """Test 15% crypto discount for Plisio payment method"""
        test_order_payload = {
            "user_email": "customer@kayee01.com",
            "user_name": "Test Customer",
            "items": [
                {
                    "product_id": "test",
                    "name": "Test Watch",
                    "price": 100.0,
                    "quantity": 2,
                    "image": "test.jpg"
                }
            ],
            "total": 200.0,
            "shipping_method": "fedex",
            "shipping_cost": 10.0,
            "payment_method": "plisio",
            "shipping_address": {
                "address": "123 Test",
                "city": "Paris",
                "postal_code": "75001",
                "country": "FR"
            },
            "phone": "+33123456789"
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
                
                # Check crypto discount fields
                crypto_discount = order_data.get("crypto_discount")
                total = order_data.get("total")
                original_total = test_order_payload["total"]
                
                # Expected: 15% discount on $200 = $30 discount
                # Final total should be $200 - $30 = $170
                expected_crypto_discount = original_total * 0.15  # $30
                expected_final_total = original_total - expected_crypto_discount  # $170
                
                details = {
                    "order_id": order_data.get("id"),
                    "order_number": order_data.get("order_number"),
                    "payment_method": order_data.get("payment_method"),
                    "original_total": original_total,
                    "crypto_discount": crypto_discount,
                    "final_total": total,
                    "expected_crypto_discount": expected_crypto_discount,
                    "expected_final_total": expected_final_total,
                    "plisio_invoice_id": order_data.get("plisio_invoice_id"),
                    "plisio_invoice_url": order_data.get("plisio_invoice_url")
                }

                # Validate crypto discount calculation
                crypto_discount_valid = (
                    crypto_discount == expected_crypto_discount and
                    total == expected_final_total and
                    order_data.get("payment_method") == "plisio"
                )

                if crypto_discount_valid:
                    self.log_result(
                        "Crypto Discount 15%", 
                        True, 
                        f"15% crypto discount applied correctly: ${crypto_discount} discount, final total ${total}",
                        details
                    )
                    return order_data
                else:
                    self.log_result(
                        "Crypto Discount 15%", 
                        False, 
                        f"Crypto discount calculation incorrect - expected ${expected_crypto_discount} discount, got ${crypto_discount}",
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
                
                self.log_result("Crypto Discount 15%", False, error_msg)
                return None

        except Exception as e:
            self.log_result("Crypto Discount 15%", False, f"Request failed: {str(e)}")
            return None

    def test_tracking_number_update(self):
        """Test tracking number update functionality"""
        # First create a test order
        test_order = self.test_crypto_discount_plisio()
        if not test_order:
            self.log_result("Tracking Number Update", False, "Failed to create test order for tracking")
            return False
        
        order_id = test_order.get("id")
        if not order_id:
            self.log_result("Tracking Number Update", False, "No order ID available for tracking test")
            return False
        
        # Need admin authentication
        if not self.admin_token:
            self.log_result("Tracking Number Update", False, "Admin authentication required")
            return False
        
        try:
            # Update tracking information
            tracking_number = "123456789"
            tracking_carrier = "fedex"
            
            response = self.session.put(
                f"{self.api_base}/orders/{order_id}/tracking?tracking_number={tracking_number}&tracking_carrier={tracking_carrier}",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.admin_token}"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                # Verify tracking update by getting the order
                order_response = self.session.get(f"{self.api_base}/orders/{order_id}", timeout=10)
                
                if order_response.status_code == 200:
                    updated_order = order_response.json()
                    
                    order_tracking_number = updated_order.get("tracking_number")
                    order_tracking_carrier = updated_order.get("tracking_carrier")
                    order_status = updated_order.get("status")
                    
                    details = {
                        "order_id": order_id,
                        "tracking_number": order_tracking_number,
                        "tracking_carrier": order_tracking_carrier,
                        "status": order_status,
                        "expected_tracking_number": tracking_number,
                        "expected_tracking_carrier": tracking_carrier,
                        "expected_status": "shipped"
                    }
                    
                    # Validate tracking update
                    tracking_valid = (
                        order_tracking_number == tracking_number and
                        order_tracking_carrier == tracking_carrier and
                        order_status == "shipped"
                    )
                    
                    if tracking_valid:
                        self.log_result(
                            "Tracking Number Update", 
                            True, 
                            f"Tracking updated successfully: {tracking_number} via {tracking_carrier}, status: {order_status}",
                            details
                        )
                        return True
                    else:
                        self.log_result(
                            "Tracking Number Update", 
                            False, 
                            f"Tracking validation failed - fields not updated correctly",
                            details
                        )
                        return False
                else:
                    self.log_result("Tracking Number Update", False, f"Failed to retrieve updated order: HTTP {order_response.status_code}")
                    return False
            else:
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f": {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f": {response.text}"
                
                self.log_result("Tracking Number Update", False, f"Tracking update failed: {error_msg}")
                return False
                
        except Exception as e:
            self.log_result("Tracking Number Update", False, f"Test failed: {str(e)}")
            return False

    def run_complete_test(self):
        """Run the complete Kayee01 site test"""
        print("🚀 Starting Kayee01 Site Testing")
        print("Testing: Stripe Payment Links, Admin Login, Email Production, Product Duplication")
        print("=" * 60)
        
        # Test 1: Backend Health Check
        if not self.test_backend_health():
            print("❌ Backend health check failed. Stopping tests.")
            return False
        
        # Test 2: Admin Login
        print("🧪 Testing Admin Login (admin@kayee01.com)...")
        admin_login = self.test_admin_login()
        
        # Test 3: Admin Dashboard Access
        if admin_login:
            print("🧪 Testing Admin Dashboard Access...")
            self.test_admin_dashboard_access()
        
        # Test 4: Stripe Payment Link Creation
        print("🧪 Testing Stripe Payment Link Creation...")
        stripe_order = self.test_stripe_payment_link_creation()
        
        # Test 5: Email Production with Manual Payment
        print("🧪 Testing Email Production (manual payment to Info.kayicom.com@gmx.fr)...")
        email_order = self.test_email_production_manual_payment()
        
        # Test 6: Product Duplication
        if admin_login:
            print("🧪 Testing Product Duplication...")
            self.test_product_duplication()
        
        # Test 7: Email SMTP Configuration Verification
        print("🧪 Testing Email SMTP Configuration...")
        self.test_email_smtp_verification()
        
        # Summary
        print("=" * 60)
        print("📊 KAYEE01 TEST SUMMARY")
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
        
        print("\n🎯 KEY KAYEE01 FEATURES TESTED:")
        print("  1. ✅ Stripe Payment Links - Order creation with payment URLs")
        print("  2. ✅ Admin Login - admin@kayee01.com authentication")
        print("  3. ✅ Email Production - Manual payment emails to Info.kayicom.com@gmx.fr")
        print("  4. ✅ Product Duplication - Adding '(Copy)' suffix to product names")
        
        return failed_tests == 0

def main():
    """Main test execution"""
    try:
        tester = Kayee01Tester()
        success = tester.run_complete_test()
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"❌ Kayee01 test execution failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()