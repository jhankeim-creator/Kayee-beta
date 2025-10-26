import { useEffect, useState, useContext } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import { CartContext } from '../App';

const GoogleAnalytics = () => {
  const [gaSettings, setGaSettings] = useState(null);
  const [scriptLoaded, setScriptLoaded] = useState(false);
  const location = useLocation();
  const { API } = useContext(CartContext);

  useEffect(() => {
    loadGASettings();
  }, []);

  const loadGASettings = async () => {
    try {
      const response = await axios.get(`${API}/settings/google-analytics`);
      if (response.data && response.data.tracking_id) {
        setGaSettings(response.data);
        initializeGA(response.data);
      }
    } catch (error) {
      console.error('Failed to load GA settings:', error);
    }
  };

  const initializeGA = (settings) => {
    if (!settings.tracking_id || scriptLoaded) return;

    // Load Google Analytics script
    const script1 = document.createElement('script');
    script1.async = true;
    script1.src = `https://www.googletagmanager.com/gtag/js?id=${settings.tracking_id}`;
    document.head.appendChild(script1);

    // Initialize gtag
    const script2 = document.createElement('script');
    script2.innerHTML = `
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', '${settings.tracking_id}', {
        ${settings.anonymize_ip ? "'anonymize_ip': true," : ''}
        ${settings.disable_advertising ? "'allow_google_signals': false," : ''}
        ${settings.disable_advertising ? "'allow_ad_personalization_signals': false," : ''}
        'send_page_view': false
      });
    `;
    document.head.appendChild(script2);

    setScriptLoaded(true);
  };

  // Track page views
  useEffect(() => {
    if (scriptLoaded && gaSettings && window.gtag) {
      window.gtag('event', 'page_view', {
        page_path: location.pathname + location.search,
        page_location: window.location.href,
        page_title: document.title
      });
    }
  }, [location, scriptLoaded, gaSettings]);

  return null; // This component doesn't render anything
};

export default GoogleAnalytics;
