#!/usr/bin/env python3
"""
Backend API Testing Suite for Ecwid-style Admin API Endpoints
Tests the complete admin dashboard functionality
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

class AdminAPITester:
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

    def test_dashboard_stats(self):
        """Test GET /api/admin/dashboard/stats"""
        try:
            response = self.session.get(f"{self.api_base}/admin/dashboard/stats", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required fields
                required_fields = [
                    "today_sales", "today_orders", "week_sales", "week_orders",
                    "month_sales", "month_orders", "total_sales", "total_orders",
                    "total_customers", "low_stock_products", "pending_orders",
                    "top_products", "recent_orders", "sales_chart"
                ]
                
                missing_fields = []
                for field in required_fields:
                    if field not in data:
                        missing_fields.append(field)
                
                details = {
                    "today_sales": data.get("today_sales", "N/A"),
                    "today_orders": data.get("today_orders", "N/A"),
                    "week_sales": data.get("week_sales", "N/A"),
                    "total_customers": data.get("total_customers", "N/A"),
                    "low_stock_products": data.get("low_stock_products", "N/A"),
                    "sales_chart_entries": len(data.get("sales_chart", [])),
                    "recent_orders_count": len(data.get("recent_orders", [])),
                    "top_products_count": len(data.get("top_products", []))
                }
                
                if missing_fields:
                    self.log_result(
                        "Dashboard Stats", 
                        False, 
                        f"Missing required fields: {missing_fields}",
                        details
                    )
                    return False
                else:
                    self.log_result(
                        "Dashboard Stats", 
                        True, 
                        "Dashboard stats retrieved successfully",
                        details
                    )
                    return True
            else:
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f": {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f": {response.text}"
                
                self.log_result("Dashboard Stats", False, error_msg)
                return False
                
        except Exception as e:
            self.log_result("Dashboard Stats", False, f"Request failed: {str(e)}")
            return False

    def test_get_coupons(self):
        """Test GET /api/admin/coupons"""
        try:
            response = self.session.get(f"{self.api_base}/admin/coupons", timeout=10)
            
            if response.status_code == 200:
                coupons = response.json()
                
                # Check if it's a list
                if not isinstance(coupons, list):
                    self.log_result("Get Coupons", False, "Response is not a list")
                    return False
                
                # Look for expected coupons (WELCOME10, SUMMER20, FREESHIP, VIP50)
                expected_codes = ["WELCOME10", "SUMMER20", "FREESHIP", "VIP50"]
                found_codes = [coupon.get("code") for coupon in coupons if coupon.get("code")]
                
                details = {
                    "total_coupons": len(coupons),
                    "found_codes": found_codes,
                    "expected_codes": expected_codes,
                    "sample_coupon": coupons[0] if coupons else "No coupons found"
                }
                
                self.log_result(
                    "Get Coupons", 
                    True, 
                    f"Retrieved {len(coupons)} coupons",
                    details
                )
                return True
            else:
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f": {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f": {response.text}"
                
                self.log_result("Get Coupons", False, error_msg)
                return False
                
        except Exception as e:
            self.log_result("Get Coupons", False, f"Request failed: {str(e)}")
            return False

    def test_validate_coupon(self):
        """Test POST /api/admin/coupons/validate"""
        try:
            # Test with WELCOME10 code and cart_total=100
            payload = {
                "code": "WELCOME10",
                "cart_total": 100.0,
                "cart_items": []
            }
            
            response = self.session.post(
                f"{self.api_base}/admin/coupons/validate",
                params=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required fields
                required_fields = ["valid", "discount_amount", "message"]
                missing_fields = []
                for field in required_fields:
                    if field not in data:
                        missing_fields.append(field)
                
                details = {
                    "valid": data.get("valid"),
                    "discount_amount": data.get("discount_amount"),
                    "message": data.get("message"),
                    "test_code": "WELCOME10",
                    "test_cart_total": 100.0
                }
                
                if missing_fields:
                    self.log_result(
                        "Validate Coupon", 
                        False, 
                        f"Missing required fields: {missing_fields}",
                        details
                    )
                    return False
                else:
                    success_msg = "Coupon validation working"
                    if data.get("valid"):
                        success_msg += f" - Valid coupon with ${data.get('discount_amount', 0):.2f} discount"
                    else:
                        success_msg += f" - Invalid coupon: {data.get('message', 'No message')}"
                    
                    self.log_result("Validate Coupon", True, success_msg, details)
                    return True
            else:
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f": {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f": {response.text}"
                
                self.log_result("Validate Coupon", False, error_msg)
                return False
                
        except Exception as e:
            self.log_result("Validate Coupon", False, f"Request failed: {str(e)}")
            return False

    def test_get_customers(self):
        """Test GET /api/admin/customers"""
        try:
            response = self.session.get(f"{self.api_base}/admin/customers", timeout=10)
            
            if response.status_code == 200:
                customers = response.json()
                
                # Check if it's a list
                if not isinstance(customers, list):
                    self.log_result("Get Customers", False, "Response is not a list")
                    return False
                
                details = {
                    "total_customers": len(customers),
                    "sample_customer": customers[0] if customers else "No customers found"
                }
                
                # Check if customers have order history (if any exist)
                if customers:
                    sample_customer = customers[0]
                    customer_fields = ["id", "email", "name", "total_orders", "total_spent"]
                    present_fields = [field for field in customer_fields if field in sample_customer]
                    details["customer_fields_present"] = present_fields
                
                self.log_result(
                    "Get Customers", 
                    True, 
                    f"Retrieved {len(customers)} customers",
                    details
                )
                return True
            else:
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f": {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f": {response.text}"
                
                self.log_result("Get Customers", False, error_msg)
                return False
                
        except Exception as e:
            self.log_result("Get Customers", False, f"Request failed: {str(e)}")
            return False

    def test_store_settings(self):
        """Test GET /api/admin/settings"""
        try:
            response = self.session.get(f"{self.api_base}/admin/settings", timeout=10)
            
            if response.status_code == 200:
                settings = response.json()
                
                # Check required fields
                expected_fields = [
                    "store_name", "currency", "tax_rate", "low_stock_threshold",
                    "email_notifications", "free_shipping_threshold"
                ]
                
                present_fields = []
                for field in expected_fields:
                    if field in settings:
                        present_fields.append(field)
                
                details = {
                    "store_name": settings.get("store_name", "N/A"),
                    "currency": settings.get("currency", "N/A"),
                    "tax_rate": settings.get("tax_rate", "N/A"),
                    "low_stock_threshold": settings.get("low_stock_threshold", "N/A"),
                    "present_fields": present_fields,
                    "total_fields": len(settings)
                }
                
                self.log_result(
                    "Store Settings", 
                    True, 
                    f"Store settings retrieved with {len(present_fields)}/{len(expected_fields)} expected fields",
                    details
                )
                return True
            else:
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f": {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f": {response.text}"
                
                self.log_result("Store Settings", False, error_msg)
                return False
                
        except Exception as e:
            self.log_result("Store Settings", False, f"Request failed: {str(e)}")
            return False

    def test_advanced_product_filtering(self):
        """Test GET /api/products with advanced filters"""
        test_cases = [
            {"filter": "on_sale=true", "params": {"on_sale": True}},
            {"filter": "is_new=true", "params": {"is_new": True}},
            {"filter": "best_seller=true", "params": {"best_seller": True}},
            {"filter": "sort_by=price&sort_order=asc", "params": {"sort_by": "price", "sort_order": "asc"}}
        ]
        
        all_passed = True
        results = []
        
        for test_case in test_cases:
            try:
                response = self.session.get(
                    f"{self.api_base}/products",
                    params=test_case["params"],
                    timeout=10
                )
                
                if response.status_code == 200:
                    products = response.json()
                    
                    if isinstance(products, list):
                        results.append({
                            "filter": test_case["filter"],
                            "success": True,
                            "count": len(products),
                            "sample": products[0] if products else None
                        })
                    else:
                        results.append({
                            "filter": test_case["filter"],
                            "success": False,
                            "error": "Response is not a list"
                        })
                        all_passed = False
                else:
                    results.append({
                        "filter": test_case["filter"],
                        "success": False,
                        "error": f"HTTP {response.status_code}"
                    })
                    all_passed = False
                    
            except Exception as e:
                results.append({
                    "filter": test_case["filter"],
                    "success": False,
                    "error": str(e)
                })
                all_passed = False
        
        details = {"test_results": results}
        
        if all_passed:
            self.log_result(
                "Advanced Product Filtering", 
                True, 
                f"All {len(test_cases)} filter tests passed",
                details
            )
        else:
            failed_tests = [r for r in results if not r["success"]]
            self.log_result(
                "Advanced Product Filtering", 
                False, 
                f"{len(failed_tests)} out of {len(test_cases)} filter tests failed",
                details
            )
        
        return all_passed

    def test_orders_with_filters(self):
        """Test GET /api/admin/orders/filters"""
        test_cases = [
            {"filter": "status=pending", "params": {"status": "pending"}},
            {"filter": "payment_method=plisio", "params": {"payment_method": "plisio"}}
        ]
        
        all_passed = True
        results = []
        
        for test_case in test_cases:
            try:
                response = self.session.get(
                    f"{self.api_base}/admin/orders/filters",
                    params=test_case["params"],
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check if response has expected structure
                    if "orders" in data and isinstance(data["orders"], list):
                        results.append({
                            "filter": test_case["filter"],
                            "success": True,
                            "orders_count": len(data["orders"]),
                            "total": data.get("total", "N/A"),
                            "page": data.get("page", "N/A")
                        })
                    else:
                        results.append({
                            "filter": test_case["filter"],
                            "success": False,
                            "error": "Invalid response structure"
                        })
                        all_passed = False
                else:
                    results.append({
                        "filter": test_case["filter"],
                        "success": False,
                        "error": f"HTTP {response.status_code}"
                    })
                    all_passed = False
                    
            except Exception as e:
                results.append({
                    "filter": test_case["filter"],
                    "success": False,
                    "error": str(e)
                })
                all_passed = False
        
        details = {"test_results": results}
        
        if all_passed:
            self.log_result(
                "Orders with Filters", 
                True, 
                f"All {len(test_cases)} order filter tests passed",
                details
            )
        else:
            failed_tests = [r for r in results if not r["success"]]
            self.log_result(
                "Orders with Filters", 
                False, 
                f"{len(failed_tests)} out of {len(test_cases)} order filter tests failed",
                details
            )
        
        return all_passed

    def run_complete_test(self):
        """Run the complete Admin API test suite"""
        print("🚀 Starting Ecwid-style Admin API Test Suite")
        print("=" * 60)
        
        # Test 1: Backend Health Check
        if not self.test_backend_health():
            print("❌ Backend health check failed. Stopping tests.")
            return False
        
        # Test 2: Dashboard Stats
        self.test_dashboard_stats()
        
        # Test 3: Get Coupons
        self.test_get_coupons()
        
        # Test 4: Validate Coupon
        self.test_validate_coupon()
        
        # Test 5: Get Customers
        self.test_get_customers()
        
        # Test 6: Store Settings
        self.test_store_settings()
        
        # Test 7: Advanced Product Filtering
        self.test_advanced_product_filtering()
        
        # Test 8: Orders with Filters
        self.test_orders_with_filters()
        
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
        tester = AdminAPITester()
        success = tester.run_complete_test()
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()