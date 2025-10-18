import os
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        self.smtp_user = os.environ.get('SMTP_USER', '')
        self.smtp_password = os.environ.get('SMTP_PASSWORD', '')
        self.from_email = os.environ.get('FROM_EMAIL', 'noreply@kayee01.com')
        self.from_name = os.environ.get('FROM_NAME', 'Kayee01')
    
    async def send_email(self, to_email: str, subject: str, html_content: str):
        """Send an email using SMTP"""
        try:
            message = MIMEMultipart('alternative')
            message['From'] = f"{self.from_name} <{self.from_email}>"
            message['To'] = to_email
            message['Subject'] = subject
            
            html_part = MIMEText(html_content, 'html')
            message.attach(html_part)
            
            # For testing/demo, just log the email instead of sending
            if not self.smtp_user or self.smtp_user == 'your-email@gmail.com':
                logger.info(f"📧 EMAIL (Demo Mode - Not Sent):")
                logger.info(f"To: {to_email}")
                logger.info(f"Subject: {subject}")
                logger.info(f"Content: {html_content[:200]}...")
                return True
            
            # Send actual email
            await aiosmtplib.send(
                message,
                hostname=self.smtp_host,
                port=self.smtp_port,
                start_tls=True,
                username=self.smtp_user,
                password=self.smtp_password
            )
            logger.info(f"✓ Email sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    async def send_order_confirmation(self, order_data: dict):
        """Send order confirmation email"""
        subject = f"Order Confirmation - {order_data['order_number']}"
        
        items_html = ""
        for item in order_data['items']:
            items_html += f"""
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">
                    <strong>{item['name']}</strong><br>
                    Quantity: {item['quantity']}
                </td>
                <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: right;">
                    ${item['price'] * item['quantity']:.2f}
                </td>
            </tr>
            """
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="text-align: center; padding: 20px; background: #1a1a1a; color: white;">
                    <h1 style="margin: 0; font-family: 'Playfair Display', serif;">
                        <span style="color: #d4af37;">Luxe</span>Boutique
                    </h1>
                </div>
                
                <div style="padding: 30px 20px;">
                    <h2 style="color: #d4af37;">Merci pour votre commande !</h2>
                    <p>Bonjour <strong>{order_data['user_name']}</strong>,</p>
                    <p>Nous avons bien reçu votre commande. Voici les détails :</p>
                    
                    <div style="background: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p><strong>Numéro de commande :</strong> {order_data['order_number']}</p>
                        <p><strong>Méthode de paiement :</strong> {order_data['payment_method']}</p>
                        <p><strong>Statut :</strong> {order_data['status']}</p>
                    </div>
                    
                    <h3>Articles commandés :</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        {items_html}
                        <tr>
                            <td style="padding: 15px 10px; text-align: right; font-size: 18px;">
                                <strong>Total :</strong>
                            </td>
                            <td style="padding: 15px 10px; text-align: right; font-size: 18px; color: #d4af37;">
                                <strong>${order_data['total']:.2f}</strong>
                            </td>
                        </tr>
                    </table>
                    
                    <h3>Adresse de livraison :</h3>
                    <p>
                        {order_data['shipping_address']['address']}<br>
                        {order_data['shipping_address']['city']}, {order_data['shipping_address']['postal_code']}<br>
                        {order_data['shipping_address']['country']}
                    </p>
                    
                    <div style="margin: 30px 0; padding: 20px; background: #fff8e1; border-left: 4px solid #d4af37;">
                        <p style="margin: 0;"><strong>Suivez votre commande :</strong></p>
                        <p style="margin: 10px 0 0 0;">
                            Vous pouvez suivre votre commande à tout moment avec le numéro : 
                            <strong>{order_data['order_number']}</strong>
                        </p>
                    </div>
                    
                    <p>Si vous avez des questions, n'hésitez pas à nous contacter via WhatsApp.</p>
                </div>
                
                <div style="text-align: center; padding: 20px; background: #f5f5f5; color: #666; font-size: 12px;">
                    <p>© 2025 LuxeBoutique. Tous droits réservés.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        await self.send_email(order_data['user_email'], subject, html_content)
    
    async def send_order_status_update(self, order_data: dict, old_status: str):
        """Send order status update email"""
        status_messages = {
            'processing': '🔄 Votre commande est en cours de traitement',
            'shipped': '📦 Votre commande a été expédiée',
            'delivered': '✅ Votre commande a été livrée',
            'cancelled': '❌ Votre commande a été annulée'
        }
        
        status_descriptions = {
            'processing': 'Nous préparons votre commande avec soin.',
            'shipped': 'Votre colis est en route ! Vous devriez le recevoir dans les prochains jours.',
            'delivered': 'Votre commande a été livrée avec succès. Nous espérons que vous êtes satisfait(e) !',
            'cancelled': 'Votre commande a été annulée. Si vous avez des questions, contactez-nous.'
        }
        
        subject = f"Mise à jour de commande - {order_data['order_number']}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="text-align: center; padding: 20px; background: #1a1a1a; color: white;">
                    <h1 style="margin: 0; font-family: 'Playfair Display', serif;">
                        <span style="color: #d4af37;">Luxe</span>Boutique
                    </h1>
                </div>
                
                <div style="padding: 30px 20px;">
                    <h2 style="color: #d4af37;">{status_messages.get(order_data['status'], 'Mise à jour de commande')}</h2>
                    <p>Bonjour <strong>{order_data['user_name']}</strong>,</p>
                    
                    <div style="background: #f9f9f9; padding: 20px; border-radius: 5px; margin: 20px 0; text-align: center;">
                        <p style="font-size: 18px; margin: 0;">
                            {status_descriptions.get(order_data['status'], 'Le statut de votre commande a été mis à jour.')}
                        </p>
                    </div>
                    
                    <div style="background: #fff; padding: 15px; border: 1px solid #ddd; border-radius: 5px; margin: 20px 0;">
                        <p><strong>Numéro de commande :</strong> {order_data['order_number']}</p>
                        <p><strong>Ancien statut :</strong> {old_status}</p>
                        <p><strong>Nouveau statut :</strong> <span style="color: #d4af37; font-weight: bold;">{order_data['status']}</span></p>
                        <p><strong>Total :</strong> ${order_data['total']:.2f}</p>
                    </div>
                    
                    <p style="text-align: center; margin: 30px 0;">
                        <a href="https://your-store.com/track-order" 
                           style="display: inline-block; padding: 12px 30px; background: #d4af37; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;">
                            Suivre ma commande
                        </a>
                    </p>
                    
                    <p>Si vous avez des questions, n'hésitez pas à nous contacter.</p>
                </div>
                
                <div style="text-align: center; padding: 20px; background: #f5f5f5; color: #666; font-size: 12px;">
                    <p>© 2025 LuxeBoutique. Tous droits réservés.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        await self.send_email(order_data['user_email'], subject, html_content)
    
    async def send_payment_confirmation(self, order_data: dict):
        """Send payment confirmation email"""
        subject = f"Paiement confirmé - {order_data['order_number']}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="text-align: center; padding: 20px; background: #1a1a1a; color: white;">
                    <h1 style="margin: 0; font-family: 'Playfair Display', serif;">
                        <span style="color: #d4af37;">Luxe</span>Boutique
                    </h1>
                </div>
                
                <div style="padding: 30px 20px;">
                    <h2 style="color: #28a745;">✅ Paiement confirmé !</h2>
                    <p>Bonjour <strong>{order_data['user_name']}</strong>,</p>
                    <p>Nous avons bien reçu votre paiement pour la commande <strong>{order_data['order_number']}</strong>.</p>
                    
                    <div style="background: #d4edda; padding: 20px; border-radius: 5px; border-left: 4px solid #28a745; margin: 20px 0;">
                        <p style="margin: 0; font-size: 18px;">
                            Montant payé : <strong style="color: #d4af37;">${order_data['total']:.2f}</strong>
                        </p>
                        <p style="margin: 10px 0 0 0;">
                            Méthode : <strong>{order_data['payment_method']}</strong>
                        </p>
                    </div>
                    
                    <p>Votre commande est maintenant en cours de traitement. Nous vous tiendrons informé(e) de son avancement.</p>
                    
                    <p style="text-align: center; margin: 30px 0;">
                        <a href="https://your-store.com/track-order" 
                           style="display: inline-block; padding: 12px 30px; background: #d4af37; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;">
                            Suivre ma commande
                        </a>
                    </p>
                </div>
                
                <div style="text-align: center; padding: 20px; background: #f5f5f5; color: #666; font-size: 12px;">
                    <p>© 2025 LuxeBoutique. Tous droits réservés.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        await self.send_email(order_data['user_email'], subject, html_content)

# Initialize email service
email_service = EmailService()
