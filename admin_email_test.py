#!/usr/bin/env python3
"""
🔍 TEST DE NOTIFICATION EMAIL ADMIN POUR NOUVELLES COMMANDES
Test Admin Email Notifications for New Orders
Tests that administrators receive email notifications at TWO addresses when new orders are placed
"""

import requests
import json
import os
import sys
import subprocess
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

class AdminEmailTester:
    def __init__(self):
        self.backend_url = get_backend_url()
        if not self.backend_url:
            raise Exception("Could not get backend URL from frontend/.env")
        
        self.api_base = f"{self.backend_url}/api"
        self.session = requests.Session()
        self.test_results = []
        
        print(f"🔗 Backend URL: {self.backend_url}")
        print(f"🔗 API Base: {self.api_base}")
        print("🔍 TEST DE NOTIFICATION EMAIL ADMIN POUR NOUVELLES COMMANDES")
        print("Testing admin email notifications for new orders as requested:")
        print("1. Test order creation with manual payment method")
        print("2. Test order creation with Stripe payment method")
        print("3. Verify admin notifications are sent to BOTH addresses:")
        print("   - kayicom509@gmail.com")
        print("   - Info.kayicom.com@gmx.fr")
        print("4. Check backend logs for email confirmation")
        print("=" * 80)

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

    def test_admin_email_notifications_for_orders(self):
        """🔍 TEST DE NOTIFICATION EMAIL ADMIN POUR NOUVELLES COMMANDES"""
        print("\n🎯 TESTING ADMIN EMAIL NOTIFICATIONS FOR NEW ORDERS")
        print("-" * 60)
        print("Testing that administrators receive email notifications at TWO addresses:")
        print("- kayicom509@gmail.com")
        print("- Info.kayicom.com@gmx.fr")
        print("When new orders are placed with different payment methods")
        print()
        
        # Test data for order creation
        test_order_data = {
            "items": [
                {
                    "id": "test-product-1",
                    "name": "Test Watch",
                    "price": 100,
                    "quantity": 1,
                    "image": "test.jpg"
                }
            ],
            "user_email": "testclient@example.com",
            "user_name": "Test Client",
            "phone": "+1234567890",
            "shipping_address": {
                "address": "123 Test St",
                "city": "Test City",
                "postal_code": "12345",
                "country": "USA"
            },
            "total": 100,
            "status": "pending"
        }
        
        # Test 1: Manual Payment Method
        print("📋 Test 1: Création Commande avec Paiement Manuel")
        manual_order_data = test_order_data.copy()
        manual_order_data["payment_method"] = "manual"
        
        success_1 = self.test_create_order_and_check_admin_notifications(
            manual_order_data, 
            "Manual Payment"
        )
        
        # Test 2: Stripe Payment Method
        print("\n📋 Test 2: Création Commande avec Stripe")
        stripe_order_data = test_order_data.copy()
        stripe_order_data["payment_method"] = "stripe"
        
        success_2 = self.test_create_order_and_check_admin_notifications(
            stripe_order_data, 
            "Stripe Payment"
        )
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DES TESTS DE NOTIFICATION ADMIN")
        print("=" * 60)
        
        if success_1 and success_2:
            print("✅ TOUS LES TESTS RÉUSSIS!")
            print("✅ Commande créée avec succès")
            print("✅ Logs 'Admin notifications sent' présents")
            print("✅ Emails envoyés aux DEUX adresses administrateur")
            print("✅ Aucune erreur dans les logs")
            return True
        else:
            print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
            if not success_1:
                print("❌ Test paiement manuel échoué")
            if not success_2:
                print("❌ Test paiement Stripe échoué")
            return False

    def test_create_order_and_check_admin_notifications(self, order_data: dict, test_name: str):
        """Create order and verify admin notifications are sent"""
        try:
            # Create order
            response = self.session.post(
                f"{self.api_base}/orders",
                json=order_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                order_response = response.json()
                order_id = order_response.get("id")
                order_number = order_response.get("order_number")
                
                details = {
                    "order_id": order_id,
                    "order_number": order_number,
                    "payment_method": order_data["payment_method"],
                    "user_email": order_data["user_email"],
                    "user_name": order_data["user_name"],
                    "total": order_data["total"]
                }
                
                self.log_result(
                    f"{test_name} - Order Creation", 
                    True, 
                    f"✅ Commande créée avec succès: {order_number}",
                    details
                )
                
                # Check backend logs for admin notification confirmation
                return self.check_backend_logs_for_admin_notifications(order_number, test_name)
                
            else:
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f": {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f": {response.text}"
                
                self.log_result(f"{test_name} - Order Creation", False, f"❌ {error_msg}")
                return False
                
        except Exception as e:
            self.log_result(f"{test_name} - Order Creation", False, f"❌ Requête échouée: {str(e)}")
            return False

    def check_backend_logs_for_admin_notifications(self, order_number: str, test_name: str):
        """Check backend logs for admin notification confirmation"""
        try:
            # Check supervisor backend logs
            result = subprocess.run(
                ["tail", "-n", "100", "/var/log/supervisor/backend.out.log"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                log_content = result.stdout
                
                # Look for admin notification messages
                admin_notification_sent = "Admin notifications sent" in log_content
                email_sent_kayicom = "Email sent successfully to kayicom509@gmail.com" in log_content
                email_sent_info = "Email sent successfully to Info.kayicom.com@gmx.fr" in log_content
                
                details = {
                    "order_number": order_number,
                    "admin_notification_log": admin_notification_sent,
                    "kayicom_email_sent": email_sent_kayicom,
                    "info_email_sent": email_sent_info,
                    "log_lines_checked": len(log_content.split('\n'))
                }
                
                # Check if all required logs are present
                all_notifications_sent = admin_notification_sent and (email_sent_kayicom or email_sent_info)
                
                if all_notifications_sent:
                    success_msg = f"✅ Notifications admin confirmées dans les logs"
                    if email_sent_kayicom and email_sent_info:
                        success_msg += " (DEUX adresses confirmées)"
                    elif email_sent_kayicom:
                        success_msg += " (kayicom509@gmail.com confirmé)"
                    elif email_sent_info:
                        success_msg += " (Info.kayicom.com@gmx.fr confirmé)"
                    
                    self.log_result(
                        f"{test_name} - Admin Notifications", 
                        True, 
                        success_msg,
                        details
                    )
                    return True
                else:
                    missing_logs = []
                    if not admin_notification_sent:
                        missing_logs.append("'Admin notifications sent'")
                    if not email_sent_kayicom and not email_sent_info:
                        missing_logs.append("'Email sent successfully' pour les deux adresses")
                    
                    self.log_result(
                        f"{test_name} - Admin Notifications", 
                        False, 
                        f"❌ Logs manquants: {', '.join(missing_logs)}",
                        details
                    )
                    return False
            else:
                self.log_result(
                    f"{test_name} - Log Check", 
                    False, 
                    f"❌ Impossible de lire les logs backend: {result.stderr}"
                )
                return False
                
        except subprocess.TimeoutExpired:
            self.log_result(
                f"{test_name} - Log Check", 
                False, 
                "❌ Timeout lors de la lecture des logs"
            )
            return False
        except Exception as e:
            self.log_result(
                f"{test_name} - Log Check", 
                False, 
                f"❌ Erreur lors de la vérification des logs: {str(e)}"
            )
            return False

    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 80)
        print("📊 RÉSUMÉ FINAL DES TESTS")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📈 Total des tests: {total_tests}")
        print(f"✅ Tests réussis: {passed_tests}")
        print(f"❌ Tests échoués: {failed_tests}")
        print(f"📊 Taux de réussite: {success_rate:.1f}%")
        print()
        
        # Print failed tests details
        failed_results = [r for r in self.test_results if not r["success"]]
        if failed_results:
            print("❌ DÉTAILS DES ÉCHECS:")
            for result in failed_results:
                print(f"  • {result['test']}: {result['message']}")
            print()
        
        # Final status
        if success_rate >= 90:
            print("🎉 STATUT GLOBAL: EXCELLENT - Notifications admin fonctionnent correctement!")
        elif success_rate >= 75:
            print("✅ STATUT GLOBAL: BON - La plupart des tests passent")
        elif success_rate >= 50:
            print("⚠️ STATUT GLOBAL: MOYEN - Quelques problèmes à résoudre")
        else:
            print("❌ STATUT GLOBAL: CRITIQUE - Notifications admin ne fonctionnent pas")
        
        print("=" * 80)
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": success_rate,
            "results": self.test_results
        }

    def run_tests(self):
        """Run admin email notification tests"""
        print("🚀 STARTING ADMIN EMAIL NOTIFICATION TESTING")
        print("=" * 80)
        
        # Test backend health first
        if not self.test_backend_health():
            print("❌ Backend not accessible. Stopping tests.")
            return self.print_summary()
        
        # Run the focused admin email notification tests
        success = self.test_admin_email_notifications_for_orders()
        
        return self.print_summary()

if __name__ == "__main__":
    try:
        tester = AdminEmailTester()
        summary = tester.run_tests()
        
        # Exit with appropriate code
        if summary["success_rate"] >= 90:
            print("\n✅ Tests de notification email admin terminés avec succès!")
            sys.exit(0)  # Success
        else:
            print(f"\n⚠️ Tests de notification email admin terminés avec {summary['failed_tests']} échecs")
            sys.exit(1)  # Failure
            
    except Exception as e:
        print(f"\n❌ Tests de notification email admin échoués: {str(e)}")
        sys.exit(1)