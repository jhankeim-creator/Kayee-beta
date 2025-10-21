import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { MessageCircle, Mail, MapPin, Facebook, Instagram, Twitter } from 'lucide-react';
import axios from 'axios';

const Footer = () => {
  const whatsappNumber = '+12393293813';
  const whatsappLink = `https://wa.me/${whatsappNumber.replace(/[^0-9]/g, '')}`;
  const [socialLinks, setSocialLinks] = useState([]);
  const [externalLinks, setExternalLinks] = useState([]);
  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
  const API = `${BACKEND_URL}/api`;

  useEffect(() => {
    loadLinks();
  }, []);

  const loadLinks = async () => {
    try {
      const [socialRes, externalRes] = await Promise.all([
        axios.get(`${API}/settings/social-links`),
        axios.get(`${API}/settings/external-links`)
      ]);
      setSocialLinks(socialRes.data);
      setExternalLinks(externalRes.data);
    } catch (error) {
      console.error('Failed to load links:', error);
    }
  };

  const getSocialIcon = (platform) => {
    switch (platform.toLowerCase()) {
      case 'facebook': return <Facebook className="h-5 w-5" />;
      case 'instagram': return <Instagram className="h-5 w-5" />;
      case 'twitter': return <Twitter className="h-5 w-5" />;
      case 'whatsapp': return <MessageCircle className="h-5 w-5" />;
      default: return null;
    }
  };

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
              Your destination for high-quality 1:1 replica watches, premium clothing and exclusive accessories.
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
              {/* External Links from Admin */}
              {externalLinks.map((link) => (
                <li key={link.id}>
                  <a
                    href={link.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-gray-400 hover:text-[#d4af37]"
                  >
                    {link.title}
                  </a>
                </li>
              ))}
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
                <a href="mailto:kayee01.shop@gmail.com" className="text-gray-400 hover:text-[#d4af37] flex items-center">
                  <Mail className="h-4 w-4 mr-2" />
                  Email Us
                </a>
              </li>
              <li className="text-gray-400 flex items-start">
                <MapPin className="h-4 w-4 mr-2 mt-1" />
                <span>Contact: kayee01.shop@gmail.com</span>
              </li>
            </ul>
          </div>

          {/* Payment Methods */}
          <div>
            <h4 className="font-semibold mb-4">We Accept</h4>
            <div className="space-y-2 text-sm text-gray-400">
              <p>💳 Credit Cards (Stripe)</p>
              <p>💰 Payoneer</p>
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