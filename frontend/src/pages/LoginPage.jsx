import React, { useState, useContext } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { CartContext } from '../App';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import Footer from '../components/Footer';
import axios from 'axios';
import { toast } from 'sonner';
import { Eye, EyeOff, Mail, Lock, User, ShoppingBag } from 'lucide-react';

const LoginPage = () => {
  const { setUser, setToken, API } = useContext(CartContext);
  const navigate = useNavigate();
  const location = useLocation();
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  
  // Login form
  const [loginData, setLoginData] = useState({
    email: '',
    password: ''
  });

  // Register form
  const [registerData, setRegisterData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    phone: ''
  });

  const handleLoginChange = (e) => {
    setLoginData({ ...loginData, [e.target.name]: e.target.value });
  };

  const handleRegisterChange = (e) => {
    setRegisterData({ ...registerData, [e.target.name]: e.target.value });
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post(`${API}/auth/login`, loginData);
      setUser(response.data.user);
      setToken(response.data.access_token);
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      
      toast.success('Welcome back!');
      
      // Redirect to intended page or account
      const from = location.state?.from?.pathname || '/account';
      navigate(from);
    } catch (error) {
      console.error('Login failed:', error);
      toast.error(error.response?.data?.detail || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();

    // Validation
    if (registerData.password !== registerData.confirmPassword) {
      toast.error('Passwords do not match');
      return;
    }

    if (registerData.password.length < 6) {
      toast.error('Password must be at least 6 characters');
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post(`${API}/auth/register`, {
        email: registerData.email,
        password: registerData.password,
        name: registerData.name,
        phone: registerData.phone
      });
      
      setUser(response.data.user);
      setToken(response.data.access_token);
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      
      toast.success('Account created successfully!');
      navigate('/account');
    } catch (error) {
      console.error('Registration failed:', error);
      toast.error(error.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="pt-32 pb-20">
        <div className="container mx-auto px-4 max-w-md">
          <div className="text-center mb-8">
            <ShoppingBag className="h-16 w-16 mx-auto mb-4 text-[#d4af37]" />
            <h1 className="text-4xl font-bold mb-2" style={{ fontFamily: 'Playfair Display' }}>
              Welcome
            </h1>
            <p className="text-gray-600">Sign in to access your account</p>
          </div>

          <Card>
            <CardHeader>
              <Tabs defaultValue="login" className="w-full">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="login">Login</TabsTrigger>
                  <TabsTrigger value="register">Register</TabsTrigger>
                </TabsList>

                {/* Login Tab */}
                <TabsContent value="login">
                  <CardTitle className="text-2xl mb-2">Login</CardTitle>
                  <CardDescription>Enter your credentials to access your account</CardDescription>
                  
                  <form onSubmit={handleLogin} className="space-y-4 mt-6">
                    <div>
                      <Label htmlFor="login-email">Email</Label>
                      <div className="relative">
                        <Mail className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                        <Input
                          id="login-email"
                          name="email"
                          type="email"
                          placeholder="your@email.com"
                          value={loginData.email}
                          onChange={handleLoginChange}
                          className="pl-10"
                          required
                        />
                      </div>
                    </div>

                    <div>
                      <Label htmlFor="login-password">Password</Label>
                      <div className="relative">
                        <Lock className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                        <Input
                          id="login-password"
                          name="password"
                          type={showPassword ? 'text' : 'password'}
                          placeholder="••••••••"
                          value={loginData.password}
                          onChange={handleLoginChange}
                          className="pl-10 pr-10"
                          required
                        />
                        <button
                          type="button"
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                        >
                          {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                        </button>
                      </div>
                    </div>

                    <div className="flex justify-between items-center">
                      <Link to="/forgot-password" className="text-sm text-[#d4af37] hover:underline">
                        Forgot Password?
                      </Link>
                    </div>

                    <Button
                      type="submit"
                      className="w-full bg-[#d4af37] hover:bg-[#b8941f]"
                      disabled={loading}
                    >
                      {loading ? 'Logging in...' : 'Login'}
                    </Button>

                    <div className="text-center text-sm text-gray-600">
                      Or continue as{' '}
                      <Link to="/shop" className="text-[#d4af37] hover:underline font-semibold">
                        Guest
                      </Link>
                    </div>
                  </form>
                </TabsContent>

                {/* Register Tab */}
                <TabsContent value="register">
                  <CardTitle className="text-2xl mb-2">Create Account</CardTitle>
                  <CardDescription>Fill in your details to get started</CardDescription>
                  
                  <form onSubmit={handleRegister} className="space-y-4 mt-6">
                    <div>
                      <Label htmlFor="register-name">Full Name</Label>
                      <div className="relative">
                        <User className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                        <Input
                          id="register-name"
                          name="name"
                          type="text"
                          placeholder="John Doe"
                          value={registerData.name}
                          onChange={handleRegisterChange}
                          className="pl-10"
                          required
                        />
                      </div>
                    </div>

                    <div>
                      <Label htmlFor="register-email">Email</Label>
                      <div className="relative">
                        <Mail className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                        <Input
                          id="register-email"
                          name="email"
                          type="email"
                          placeholder="your@email.com"
                          value={registerData.email}
                          onChange={handleRegisterChange}
                          className="pl-10"
                          required
                        />
                      </div>
                    </div>

                    <div>
                      <Label htmlFor="register-phone">Phone (Optional)</Label>
                      <Input
                        id="register-phone"
                        name="phone"
                        type="tel"
                        placeholder="+1 234 567 8900"
                        value={registerData.phone}
                        onChange={handleRegisterChange}
                      />
                    </div>

                    <div>
                      <Label htmlFor="register-password">Password</Label>
                      <div className="relative">
                        <Lock className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                        <Input
                          id="register-password"
                          name="password"
                          type={showPassword ? 'text' : 'password'}
                          placeholder="••••••••"
                          value={registerData.password}
                          onChange={handleRegisterChange}
                          className="pl-10 pr-10"
                          required
                        />
                        <button
                          type="button"
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                        >
                          {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                        </button>
                      </div>
                    </div>

                    <div>
                      <Label htmlFor="register-confirm">Confirm Password</Label>
                      <Input
                        id="register-confirm"
                        name="confirmPassword"
                        type="password"
                        placeholder="••••••••"
                        value={registerData.confirmPassword}
                        onChange={handleRegisterChange}
                        required
                      />
                    </div>

                    <Button
                      type="submit"
                      className="w-full bg-[#d4af37] hover:bg-[#b8941f]"
                      disabled={loading}
                    >
                      {loading ? 'Creating Account...' : 'Create Account'}
                    </Button>

                    <p className="text-xs text-center text-gray-500">
                      By creating an account, you agree to our{' '}
                      <Link to="/terms-of-service" className="text-[#d4af37] hover:underline">
                        Terms of Service
                      </Link>{' '}
                      and{' '}
                      <Link to="/refund-policy" className="text-[#d4af37] hover:underline">
                        Privacy Policy
                      </Link>
                    </p>
                  </form>
                </TabsContent>
              </Tabs>
            </CardHeader>
          </Card>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default LoginPage;
