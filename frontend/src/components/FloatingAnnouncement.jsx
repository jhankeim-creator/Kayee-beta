import { useState, useEffect, useContext } from 'react';
import { useLocation } from 'react-router-dom';
import { X } from 'lucide-react';
import axios from 'axios';
import { CartContext } from '../App';

const FloatingAnnouncement = () => {
  const [announcement, setAnnouncement] = useState(null);
  const [isVisible, setIsVisible] = useState(false);
  const { API } = useContext(CartContext);
  const location = useLocation();

  useEffect(() => {
    loadAnnouncement();
  }, []);

  const loadAnnouncement = async () => {
    // Don't show popup on admin pages, login pages, or checkout
    const excludedPaths = ['/admin', '/forgot-password', '/reset-password'];
    const isExcludedPage = excludedPaths.some(path => location.pathname.startsWith(path));
    
    if (isExcludedPage) {
      return;
    }
    
    try {
      const res = await axios.get(`${API}/settings/floating-announcement`);
      if (res.data && res.data.enabled) {
        // Check if announcement should be shown based on frequency
        const lastShown = localStorage.getItem('announcement_last_shown');
        const frequency = res.data.frequency || 'once_per_session';
        
        let shouldShow = false;
        
        if (frequency === 'every_visit') {
          shouldShow = true;
        } else if (frequency === 'once_per_session') {
          shouldShow = !sessionStorage.getItem('announcement_shown');
        } else if (frequency === 'daily') {
          const today = new Date().toDateString();
          shouldShow = lastShown !== today;
        }
        
        if (shouldShow) {
          setAnnouncement(res.data);
          setTimeout(() => setIsVisible(true), 1000); // Show after 1 second
        }
      }
    } catch (error) {
      console.error('Failed to load announcement:', error);
    }
  };

  const handleClose = () => {
    setIsVisible(false);
    
    // Record that announcement was shown
    if (announcement.frequency === 'once_per_session') {
      sessionStorage.setItem('announcement_shown', 'true');
    } else if (announcement.frequency === 'daily') {
      const today = new Date().toDateString();
      localStorage.setItem('announcement_last_shown', today);
    }
  };

  if (!announcement || !isVisible) return null;

  return (
    <>
      {/* Overlay */}
      <div
        className={`fixed inset-0 bg-black transition-opacity duration-300 z-50 ${
          isVisible ? 'opacity-50' : 'opacity-0 pointer-events-none'
        }`}
        onClick={handleClose}
      />

      {/* Modal */}
      <div
        className={`fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white rounded-lg shadow-2xl z-50 max-w-md w-full mx-4 transition-all duration-300 ${
          isVisible ? 'opacity-100 scale-100' : 'opacity-0 scale-95 pointer-events-none'
        }`}
      >
        {/* Close Button */}
        <button
          onClick={handleClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors z-10"
        >
          <X className="h-6 w-6" />
        </button>

        {/* Image (if provided) */}
        {announcement.image_url && (
          <div className="w-full h-48 overflow-hidden rounded-t-lg">
            <img
              src={announcement.image_url}
              alt="Announcement"
              className="w-full h-full object-cover"
            />
          </div>
        )}

        {/* Content */}
        <div className="p-6">
          {announcement.title && (
            <h2 className="text-2xl font-bold mb-3 text-center" style={{ fontFamily: 'Playfair Display' }}>
              {announcement.title}
            </h2>
          )}
          
          <p className="text-gray-700 text-center mb-6 whitespace-pre-wrap">
            {announcement.message}
          </p>

          {/* Call to Action Button */}
          {announcement.link_url && (
            <div className="text-center">
              <a
                href={announcement.link_url}
                className="inline-block px-8 py-3 rounded-lg text-white font-semibold hover:opacity-90 transition-opacity"
                style={{ backgroundColor: announcement.button_color || '#d4af37' }}
                onClick={handleClose}
              >
                {announcement.link_text || 'Learn More'}
              </a>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default FloatingAnnouncement;
