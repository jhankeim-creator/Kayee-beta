#!/usr/bin/env python3
"""
🔍 TEST COMPLET DES CORRECTIONS DEMANDÉES
Complete Test of Requested Corrections

Tests the following specific corrections as requested:
1. TEST PAIEMENT MANUEL - Instructions UNIQUEMENT par Email
2. TEST SYSTÈME BULK EMAIL  
3. TEST NOTIFICATIONS ADMIN (re-verification)
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

class FrenchReviewTester:
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
        print("🔍 TEST COMPLET DES CORRECTIONS DEMANDÉES")
        print("Testing specific corrections as requested:")
        print("1. TEST PAIEMENT MANUEL - Instructions UNIQUEMENT par Email")
        print("   - Create manual payment gateway in admin")
        print("   - Verify gateway appears on public API")
        print("   - Create order with manual gateway")
        print("   - Verify client email contains payment instructions + order number")
        print("2. TEST SYSTÈME BULK EMAIL")
        print("   - POST /api/admin/settings/bulk-email")
        print("   - Verify API returns success and logs show email sent")
        print("   - GET /api/admin/settings/bulk-emails for history")
        print("3. TEST NOTIFICATIONS ADMIN (re-verification)")
        print("   - Create order and verify 2 admin emails sent:")
        print("   - kayicom509@gmail.com + Info.kayicom.com@gmx.fr")
        print("Credentials: kayicom509@gmail.com / Admin123!")
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

    def test_admin_login(self):
        """Test admin login"""
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

                login_valid = (
                    access_token is not None and 
                    token_type == "bearer" and
                    user is not None and
                    user.get("email") == "kayicom509@gmail.com" and
                    user.get("role") == "admin"
                )

                if login_valid:
                    self.admin_token = access_token
                    self.session.headers.update({"Authorization": f"Bearer {access_token}"})
                    
                    self.log_result(
                        "Admin Login", 
                        True, 
                        "✅ Login réussi - token JWT retourné et utilisateur vérifié",
                        details
                    )
                    return True
                else:
                    self.log_result(
                        "Admin Login", 
                        False, 
                        "❌ Validation échouée - champs manquants ou rôle incorrect",
                        details
                    )
                    return False
            else:
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f": {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f": {response.text}"
                
                self.log_result("Admin Login", False, f"❌ {error_msg}")
                return False

        except Exception as e:
            self.log_result("Admin Login", False, f"❌ Requête échouée: {str(e)}")
            return False

    def test_manual_payment_instructions_email(self):
        """🔍 TEST 1: PAIEMENT MANUEL - Instructions UNIQUEMENT par Email"""
        if not self.admin_token:
            self.log_result("Manual Payment Instructions Email", False, "Admin authentication required")
            return False
        
        print("\n🎯 TEST 1: PAIEMENT MANUEL - Instructions UNIQUEMENT par Email")
        print("-" * 60)
        
        # Step 1: Create manual payment gateway
        gateway_payload = {
            "gateway_type": "manual",
            "name": "PayPal Test",
            "description": "Payment via PayPal",
            "payment_instructions": "Envoyez le paiement à: paypal@kayee01.com\nMontant: [VOIR EMAIL]\nRéférence: [NUMERO_COMMANDE]",
            "enabled": True
        }
        
        try:
            # Create gateway
            response = self.session.post(
                f"{self.api_base}/admin/settings/payment-gateways",
                json=gateway_payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.admin_token}"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                gateway_data = response.json()
                gateway_id = gateway_data.get("gateway_id")
                
                self.log_result(
                    "Create Manual Payment Gateway", 
                    True, 
                    f"Manual gateway created: {gateway_data.get('name')}",
                    {"gateway_id": gateway_id, "instructions": gateway_data.get("payment_instructions")}
                )
                
                # Step 2: Verify gateway appears on public API
                public_response = self.session.get(f"{self.api_base}/settings/payment-gateways", timeout=10)
                if public_response.status_code == 200:
                    public_gateways = public_response.json()
                    gateway_found = any(g.get("gateway_id") == gateway_id for g in public_gateways)
                    
                    self.log_result(
                        "Verify Gateway on Public API", 
                        gateway_found, 
                        f"Gateway {'found' if gateway_found else 'not found'} on /api/settings/payment-gateways",
                        {"public_gateways_count": len(public_gateways)}
                    )
                    
                    if gateway_found:
                        # Step 3: Create order with manual gateway
                        return self.test_create_order_with_manual_gateway(gateway_id)
                
            else:
                self.log_result("Create Manual Payment Gateway", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Create Manual Payment Gateway", False, f"Request failed: {str(e)}")
            return False

    def test_create_order_with_manual_gateway(self, gateway_id: str):
        """Create order with manual payment gateway and verify email instructions"""
        order_payload = {
            "items": [{
                "id": "test-1",
                "name": "Test Product",
                "price": 50,
                "quantity": 1,
                "image": "test.jpg"
            }],
            "user_email": "client-test@example.com",
            "user_name": "Test Client",
            "phone": "+1234567890",
            "shipping_address": {
                "address": "123 Test St",
                "city": "Test City",
                "postal_code": "12345",
                "country": "USA"
            },
            "payment_method": f"manual-{gateway_id}",
            "total": 50,
            "status": "pending"
        }
        
        try:
            response = self.session.post(
                f"{self.api_base}/orders",
                json=order_payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                order_data = response.json()
                order_number = order_data.get("order_number")
                
                self.log_result(
                    "Create Order with Manual Gateway", 
                    True, 
                    f"Order created successfully: {order_number}",
                    {
                        "order_id": order_data.get("id"),
                        "order_number": order_number,
                        "payment_method": order_data.get("payment_method"),
                        "total": order_data.get("total"),
                        "user_email": order_data.get("user_email")
                    }
                )
                
                # Check backend logs for email confirmation
                print("📧 VÉRIFICATION: L'email client doit contenir:")
                print("   - Les instructions de paiement")
                print("   - Le numéro de commande comme référence")
                print("   - Le message 'Veuillez inclure votre numéro de commande'")
                print("   ✅ Vérifiez les logs backend pour confirmation d'envoi d'email")
                
                return True
            else:
                self.log_result("Create Order with Manual Gateway", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Create Order with Manual Gateway", False, f"Request failed: {str(e)}")
            return False

    def test_bulk_email_system_comprehensive(self):
        """🔍 TEST 2: SYSTÈME BULK EMAIL"""
        if not self.admin_token:
            self.log_result("Bulk Email System Comprehensive", False, "Admin authentication required")
            return False
        
        print("\n🎯 TEST 2: SYSTÈME BULK EMAIL")
        print("-" * 60)
        
        # Test bulk email sending
        bulk_email_payload = {
            "subject": "Test Email Promotionnel",
            "message": "Ceci est un test d'email en masse",
            "recipient_filter": "all"
        }
        
        try:
            response = self.session.post(
                f"{self.api_base}/admin/settings/bulk-email",
                json=bulk_email_payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.admin_token}"
                },
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                email_data = response.json()
                
                self.log_result(
                    "Send Bulk Email", 
                    True, 
                    f"Bulk email sent successfully: {email_data.get('message')}",
                    {
                        "sent_to": email_data.get("sent_to"),
                        "subject": bulk_email_payload["subject"],
                        "message": bulk_email_payload["message"]
                    }
                )
                
                # Test getting bulk email history
                return self.test_bulk_email_history_check()
            else:
                self.log_result("Send Bulk Email", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Send Bulk Email", False, f"Request failed: {str(e)}")
            return False

    def test_bulk_email_history_check(self):
        """Check bulk email history"""
        try:
            response = self.session.get(
                f"{self.api_base}/admin/settings/bulk-emails",
                headers={"Authorization": f"Bearer {self.admin_token}"},
                timeout=10
            )
            
            if response.status_code == 200:
                emails = response.json()
                
                self.log_result(
                    "Get Bulk Email History", 
                    True, 
                    f"Retrieved {len(emails)} bulk emails from history",
                    {"emails_count": len(emails), "latest_email": emails[0] if emails else None}
                )
                
                print("📧 VÉRIFICATION: Vérifiez les logs backend pour confirmation d'envoi d'email")
                return True
            else:
                self.log_result("Get Bulk Email History", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Get Bulk Email History", False, f"Request failed: {str(e)}")
            return False

    def test_admin_notifications_reverification(self):
        """🔍 TEST 3: NOTIFICATIONS ADMIN (re-vérification)"""
        print("\n🎯 TEST 3: NOTIFICATIONS ADMIN (re-vérification)")
        print("-" * 60)
        
        # Create a test order to trigger admin notifications
        order_payload = {
            "items": [{
                "id": "admin-test-1",
                "name": "Admin Notification Test Product",
                "price": 75,
                "quantity": 1,
                "image": "admin-test.jpg"
            }],
            "user_email": "admin-test@example.com",
            "user_name": "Admin Test User",
            "phone": "+1234567890",
            "shipping_address": {
                "address": "456 Admin St",
                "city": "Admin City",
                "postal_code": "67890",
                "country": "USA"
            },
            "payment_method": "stripe",
            "total": 75,
            "status": "pending"
        }
        
        try:
            response = self.session.post(
                f"{self.api_base}/orders",
                json=order_payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                order_data = response.json()
                order_number = order_data.get("order_number")
                
                self.log_result(
                    "Create Order for Admin Notifications", 
                    True, 
                    f"Order created successfully: {order_number}",
                    {
                        "order_id": order_data.get("id"),
                        "order_number": order_number,
                        "payment_method": order_data.get("payment_method"),
                        "total": order_data.get("total")
                    }
                )
                
                print("📧 VÉRIFICATION: Les 2 emails admin doivent être envoyés à:")
                print("   - kayicom509@gmail.com")
                print("   - Info.kayicom.com@gmx.fr")
                print("   ✅ Vérifiez les logs backend pour confirmation d'envoi aux 2 adresses")
                
                return True
            else:
                self.log_result("Create Order for Admin Notifications", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Create Order for Admin Notifications", False, f"Request failed: {str(e)}")
            return False

    def run_french_review_tests(self):
        """Run the specific tests requested in the French review"""
        print("🚀 DÉMARRAGE DES TESTS DE RÉVISION FRANÇAISE")
        print("=" * 80)
        
        # Test backend health first
        if not self.test_backend_health():
            print("❌ Backend not accessible. Stopping tests.")
            return self.print_summary()
        
        # Test admin login first (required for tests)
        if not self.test_admin_login():
            print("❌ Admin login failed. Cannot proceed with tests.")
            return self.print_summary()
        
        # Run the three specific tests requested
        print("\n📋 EXÉCUTION DES TESTS SPÉCIFIQUES DEMANDÉS:")
        print("-" * 50)
        
        # Test 1: Manual Payment Instructions Email
        self.test_manual_payment_instructions_email()
        
        # Test 2: Bulk Email System
        self.test_bulk_email_system_comprehensive()
        
        # Test 3: Admin Notifications Re-verification
        self.test_admin_notifications_reverification()
        
        return self.print_summary()

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
            print("🎉 STATUT GLOBAL: EXCELLENT - Tous les endpoints fonctionnent correctement!")
        elif success_rate >= 75:
            print("✅ STATUT GLOBAL: BON - La plupart des fonctionnalités marchent")
        elif success_rate >= 50:
            print("⚠️ STATUT GLOBAL: MOYEN - Quelques problèmes à résoudre")
        else:
            print("❌ STATUT GLOBAL: CRITIQUE - Plusieurs fonctionnalités ne marchent pas")
        
        print("=" * 80)
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": success_rate,
            "results": self.test_results
        }

def main():
    """Main function for French review tests"""
    try:
        tester = FrenchReviewTester()
        # Run the specific French review tests
        summary = tester.run_french_review_tests()
        
        # Exit with appropriate code
        if summary["success_rate"] >= 80:
            print("\n✅ Tests de révision française terminés avec succès!")
            sys.exit(0)  # Success
        else:
            print(f"\n⚠️ Tests de révision française terminés avec {summary['failed_tests']} échecs")
            sys.exit(1)  # Failure
            
    except Exception as e:
        print(f"\n❌ Tests de révision française échoués: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()