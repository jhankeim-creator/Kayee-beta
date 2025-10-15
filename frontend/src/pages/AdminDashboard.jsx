import { useState, useEffect, useContext } from 'react';
import { Routes, Route, Link, useNavigate, Navigate } from 'react-router-dom';
import { CartContext } from '../App';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import AdminProducts from '../components/AdminProducts';
import AdminOrders from '../components/AdminOrders';
import AdminCategories from '../components/AdminCategories';
import axios from 'axios';
import { toast } from 'sonner';
import { Package, ShoppingCart, Users, DollarSign, Home } from 'lucide-react';

const AdminDashboard = () => {
  const { user, token, API } = useContext(CartContext);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    if (!user || !token) {
      toast.error('Please login to access admin dashboard');
      navigate('/admin/login');
      return;
    }
    if (user.role !== 'admin') {
      toast.error('Admin access required');
      navigate('/');
      return;
    }
    loadStats();
  }, [user, token]);

  const loadStats = async () => {
    try {
      const response = await axios.get(`${API}/admin/stats`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStats(response.data);
    } catch (error) {
      console.error('Failed to load stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!user || user.role !== 'admin') {
    return <Navigate to="/admin/login" />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="pt-32 pb-20">
        <div className="container mx-auto px-4">
          {/* Header */}
          <div className="flex justify-between items-center mb-8">
            <h1
              className="text-4xl md:text-5xl font-bold"
              style={{ fontFamily: 'Playfair Display' }}
              data-testid="admin-dashboard-title"
            >
              Admin Dashboard
            </h1>
            <Button
              onClick={() => navigate('/')}
              variant="outline"
              data-testid="back-to-store-button"
            >
              <Home className="mr-2 h-4 w-4" />
              Back to Store
            </Button>
          </div>

          {/* Stats Cards */}
          {stats && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">Total Products</CardTitle>
                  <Package className="h-5 w-5 text-[#d4af37]" />
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold" data-testid="stat-products">{stats.total_products}</div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">Total Orders</CardTitle>
                  <ShoppingCart className="h-5 w-5 text-[#d4af37]" />
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold" data-testid="stat-orders">{stats.total_orders}</div>
                  <p className="text-xs text-gray-600 mt-1">{stats.pending_orders} pending</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">Total Customers</CardTitle>
                  <Users className="h-5 w-5 text-[#d4af37]" />
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold" data-testid="stat-users">{stats.total_users}</div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">Total Revenue</CardTitle>
                  <DollarSign className="h-5 w-5 text-[#d4af37]" />
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold" data-testid="stat-revenue">${stats.total_revenue.toFixed(2)}</div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Management Tabs */}
          <Card>
            <CardContent className="p-6">
              <Tabs defaultValue="products">
                <TabsList className="mb-6">
                  <TabsTrigger value="products" data-testid="tab-products">Products</TabsTrigger>
                  <TabsTrigger value="orders" data-testid="tab-orders">Orders</TabsTrigger>
                  <TabsTrigger value="categories" data-testid="tab-categories">Categories</TabsTrigger>
                </TabsList>
                <TabsContent value="products">
                  <AdminProducts />
                </TabsContent>
                <TabsContent value="orders">
                  <AdminOrders />
                </TabsContent>
                <TabsContent value="categories">
                  <AdminCategories />
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;