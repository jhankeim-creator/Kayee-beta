import { useState } from 'react';
import { Button } from './ui/button';
import { toast } from 'sonner';
import axios from 'axios';

const SocialAuth = ({ onSuccess }) => {
  const [loading, setLoading] = useState(false);
  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
  const API = `${BACKEND_URL}/api`;

  const handleGoogleLogin = async () => {
    setLoading(true);
    try {
      // Demo mode - simulate login
      toast.info('Demo mode - Google login simulated');
      
      // En production, vous utiliseriez Google Sign-In SDK
      // const response = await gapi.auth2.getAuthInstance().signIn();
      // const token = response.getAuthResponse().id_token;
      
      // const result = await axios.post(`${API}/auth/oauth/google`, { token });
      // if (result.data.success) {
      //   onSuccess(result.data.user);
      // }
      
      setTimeout(() => {
        onSuccess({
          email: 'demo@gmail.com',
          name: 'Demo User',
          picture: 'https://via.placeholder.com/150'
        });
      }, 1000);
    } catch (error) {
      console.error('Google login failed:', error);
      toast.error('Google login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleFacebookLogin = async () => {
    setLoading(true);
    try {
      toast.info('Mode démo - Connexion Facebook simulée');
      
      // En production, vous utiliseriez Facebook SDK
      // FB.login((response) => {
      //   if (response.authResponse) {
      //     const token = response.authResponse.accessToken;
      //     axios.post(`${API}/auth/oauth/facebook`, { access_token: token });
      //   }
      // });
      
      setTimeout(() => {
        onSuccess({
          email: 'demo@facebook.com',
          name: 'Demo User',
          picture: 'https://via.placeholder.com/150'
        });
      }, 1000);
    } catch (error) {
      console.error('Facebook login failed:', error);
      toast.error('Échec de la connexion Facebook');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-3">
      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <span className="w-full border-t" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-white px-2 text-gray-500">Ou connectez-vous avec</span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <Button
          onClick={handleGoogleLogin}
          disabled={loading}
          variant="outline"
          className="w-full"
          data-testid="google-login-button"
        >
          <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
            <path
              fill="currentColor"
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            />
            <path
              fill="currentColor"
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            />
            <path
              fill="currentColor"
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
            />
            <path
              fill="currentColor"
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
            />
          </svg>
          Google
        </Button>

        <Button
          onClick={handleFacebookLogin}
          disabled={loading}
          variant="outline"
          className="w-full"
          data-testid="facebook-login-button"
        >
          <svg className="w-5 h-5 mr-2" fill="#1877F2" viewBox="0 0 24 24">
            <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
          </svg>
          Facebook
        </Button>
      </div>

      <p className="text-xs text-center text-gray-500">
        Mode démo activé - Les connexions sociales sont simulées
      </p>
    </div>
  );
};

export default SocialAuth;
