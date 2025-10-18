import { Link } from 'react-router-dom';
import { MessageCircle, Mail, MapPin } from 'lucide-react';

const Footer = () => {
  const whatsappNumber = '+1234567890'; // You can change this
  const whatsappLink = `https://wa.me/${whatsappNumber.replace(/[^0-9]/g, '')}`;

  return (
    <footer className="bg-[#1a1a1a] text-white">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div>
            <h3 className="text-2xl font-bold mb-4" style={{ fontFamily: 'Playfair Display' }}>
              <span className="text-[#d4af37]">Kayee</span>01
            </h3>
            <p className="text-gray-400 text-sm">
              Your destination for luxury fashion and exquisite jewelry.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/shop" className="text-gray-400 hover:text-[#d4af37]">
                  Shop
                </Link>
              </li>
              <li>
                <Link to="/track-order" className="text-gray-400 hover:text-[#d4af37]">
                  Track Order
                </Link>
              </li>
              <li>
                <Link to="/terms" className="text-gray-400 hover:text-[#d4af37]">
                  Terms of Service
                </Link>
              </li>
              <li>
                <Link to="/refund-policy" className="text-gray-400 hover:text-[#d4af37]">
                  Refund Policy
                </Link>
              </li>
              <li>
                <Link to="/faq" className="text-gray-400 hover:text-[#d4af37]">
                  FAQ
                </Link>
              </li>
            </ul>
          </div>

          {/* Customer Service */}
          <div>
            <h4 className="font-semibold mb-4">Customer Service</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/faq" className="text-gray-400 hover:text-[#d4af37]">
                  FAQ
                </Link>
              </li>
              <li>
                <a href={whatsappLink} target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-[#d4af37] flex items-center">
                  <MessageCircle className="h-4 w-4 mr-2" />
                  WhatsApp Support
                </a>
              </li>
              <li>
                <a href="mailto:support@kayee01.com" className="text-gray-400 hover:text-[#d4af37] flex items-center">
                  <Mail className="h-4 w-4 mr-2" />
                  Email Us
                </a>
              </li>
              <li className="text-gray-400 flex items-start">
                <MapPin className="h-4 w-4 mr-2 mt-1" />
                <span>Your Address Here</span>
              </li>
            </ul>
          </div>

          {/* Payment Methods */}
          <div>
            <h4 className="font-semibold mb-4">We Accept</h4>
            <div className="space-y-2 text-sm text-gray-400">
              <p>💳 Credit Cards (Stripe)</p>
              <p>💰 Payoneer</p>
              <p>💰 PayPal</p>
              <p>💰 Multiple Crypto (Plisio)</p>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm text-gray-400">
          <p>&copy; {new Date().getFullYear()} Kayee01. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;