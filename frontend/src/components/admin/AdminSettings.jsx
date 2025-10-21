import React, { useState, useEffect, useContext } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Textarea } from '../ui/textarea';
import { Switch } from '../ui/switch';
import { toast } from 'sonner';
import axios from 'axios';
import { CartContext } from '../../App';
import { Plus, Trash2, Save, Settings, Link as LinkIcon, Bell, Mail, CreditCard } from 'lucide-react';

const AdminSettings = () => {
  const { API, token } = useContext(CartContext);
  const [activeTab, setActiveTab] = useState('payment');
  const [loading, setLoading] = useState(false);

  // Payment Gateways State
  const [paymentGateways, setPaymentGateways] = useState([]);
  const [newGateway, setNewGateway] = useState({
    gateway_type: 'manual',
    name: '',
    description: '',
    logo_url: '',
    enabled: true,
    instructions: ''
  });

  // Social Links State
  const [socialLinks, setSocialLinks] = useState([]);
  const [newSocialLink, setNewSocialLink] = useState({
    platform: 'facebook',
    url: '',
    enabled: true
  });

  // External Links State
  const [externalLinks, setExternalLinks] = useState([]);
  const [newExternalLink, setNewExternalLink] = useState({
    title: '',
    url: '',
    enabled: true
  });

  // Floating Announcement State
  const [announcement, setAnnouncement] = useState({
    enabled: false,
    title: '',
    message: '',
    image_url: '',
    link_url: '',
    link_text: 'Learn More',
    button_color: '#d4af37',
    frequency: 'once_per_session'
  });

  // Bulk Email State
  const [bulkEmail, setBulkEmail] = useState({
    subject: '',
    message: '',
    recipient_filter: 'all'
  });
  const [bulkEmailHistory, setBulkEmailHistory] = useState([]);

  useEffect(() => {
    loadData();
  }, [activeTab]);

  const loadData = async () => {
    try {
      const headers = { Authorization: `Bearer ${token}` };
      
      if (activeTab === 'payment') {
        const res = await axios.get(`${API}/admin/settings/payment-gateways`, { headers });
        setPaymentGateways(res.data);
      } else if (activeTab === 'social') {
        const res = await axios.get(`${API}/admin/settings/social-links`, { headers });
        setSocialLinks(res.data);
      } else if (activeTab === 'external') {
        const res = await axios.get(`${API}/admin/settings/external-links`, { headers });
        setExternalLinks(res.data);
      } else if (activeTab === 'announcement') {
        const res = await axios.get(`${API}/admin/settings/floating-announcement`, { headers });
        if (res.data) setAnnouncement(res.data);
      } else if (activeTab === 'bulk-email') {
        const res = await axios.get(`${API}/admin/settings/bulk-emails`, { headers });
        setBulkEmailHistory(res.data);
      }
    } catch (error) {
      console.error('Failed to load data:', error);
    }
  };

  // Payment Gateway Functions
  const addPaymentGateway = async () => {
    if (!newGateway.name) {
      toast.error('Please enter gateway name');
      return;
    }
    
    try {
      const headers = { Authorization: `Bearer ${token}` };
      await axios.post(`${API}/admin/settings/payment-gateways`, newGateway, { headers });
      toast.success('Payment gateway added');
      setNewGateway({
        gateway_type: 'manual',
        name: '',
        description: '',
        logo_url: '',
        enabled: true,
        instructions: ''
      });
      loadData();
    } catch (error) {
      toast.error('Failed to add payment gateway');
    }
  };

  const deletePaymentGateway = async (gatewayId) => {
    try {
      const headers = { Authorization: `Bearer ${token}` };
      await axios.delete(`${API}/admin/settings/payment-gateways/${gatewayId}`, { headers });
      toast.success('Payment gateway deleted');
      loadData();
    } catch (error) {
      toast.error('Failed to delete payment gateway');
    }
  };

  // Social Link Functions
  const addSocialLink = async () => {
    if (!newSocialLink.url) {
      toast.error('Please enter URL');
      return;
    }
    
    try {
      const headers = { Authorization: `Bearer ${token}` };
      await axios.post(`${API}/admin/settings/social-links`, newSocialLink, { headers });
      toast.success('Social link added');
      setNewSocialLink({ platform: 'facebook', url: '', enabled: true });
      loadData();
    } catch (error) {
      toast.error('Failed to add social link');
    }
  };

  const deleteSocialLink = async (linkId) => {
    try {
      const headers = { Authorization: `Bearer ${token}` };
      await axios.delete(`${API}/admin/settings/social-links/${linkId}`, { headers });
      toast.success('Social link deleted');
      loadData();
    } catch (error) {
      toast.error('Failed to delete social link');
    }
  };

  // External Link Functions
  const addExternalLink = async () => {
    if (!newExternalLink.title || !newExternalLink.url) {
      toast.error('Please enter title and URL');
      return;
    }
    
    if (externalLinks.length >= 3) {
      toast.error('Maximum 3 external links allowed');
      return;
    }
    
    try {
      const headers = { Authorization: `Bearer ${token}` };
      await axios.post(`${API}/admin/settings/external-links`, newExternalLink, { headers });
      toast.success('External link added');
      setNewExternalLink({ title: '', url: '', enabled: true });
      loadData();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to add external link');
    }
  };

  const deleteExternalLink = async (linkId) => {
    try {
      const headers = { Authorization: `Bearer ${token}` };
      await axios.delete(`${API}/admin/settings/external-links/${linkId}`, { headers });
      toast.success('External link deleted');
      loadData();
    } catch (error) {
      toast.error('Failed to delete external link');
    }
  };

  // Floating Announcement Functions
  const saveAnnouncement = async () => {
    try {
      const headers = { Authorization: `Bearer ${token}` };
      await axios.put(`${API}/admin/settings/floating-announcement`, announcement, { headers });
      toast.success('Floating announcement updated');
    } catch (error) {
      toast.error('Failed to update announcement');
    }
  };

  // Bulk Email Functions
  const sendBulkEmail = async () => {
    if (!bulkEmail.subject || !bulkEmail.message) {
      toast.error('Please enter subject and message');
      return;
    }
    
    setLoading(true);
    try {
      const headers = { Authorization: `Bearer ${token}` };
      const res = await axios.post(`${API}/admin/settings/bulk-email`, bulkEmail, { headers });
      toast.success(res.data.message);
      setBulkEmail({ subject: '', message: '', recipient_filter: 'all' });
      loadData();
    } catch (error) {
      toast.error('Failed to send bulk email');
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'payment', label: 'Payment Gateways', icon: CreditCard },
    { id: 'social', label: 'Social Links', icon: LinkIcon },
    { id: 'external', label: 'External Links', icon: LinkIcon },
    { id: 'announcement', label: 'Floating Announcement', icon: Bell },
    { id: 'bulk-email', label: 'Bulk Email', icon: Mail },
  ];

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold flex items-center">
            <Settings className="h-8 w-8 mr-3" />
            Admin Settings
          </h1>
          <p className="text-gray-600 mt-1">Manage payment gateways, social links, and announcements</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b pb-2 overflow-x-auto">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center px-4 py-2 rounded-t-lg transition-colors whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-[#d4af37] text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            <tab.icon className="h-4 w-4 mr-2" />
            {tab.label}
          </button>
        ))}
      </div>

      {/* Payment Gateways Tab */}
      {activeTab === 'payment' && (
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Add Payment Gateway</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label>Gateway Type</Label>
                  <select
                    className="w-full p-2 border rounded"
                    value={newGateway.gateway_type}
                    onChange={(e) => setNewGateway({ ...newGateway, gateway_type: e.target.value })}
                  >
                    <option value="manual">Manual Payment</option>
                    <option value="stripe">Stripe</option>
                    <option value="plisio">Plisio (Crypto)</option>
                  </select>
                </div>
                <div>
                  <Label>Gateway Name *</Label>
                  <Input
                    value={newGateway.name}
                    onChange={(e) => setNewGateway({ ...newGateway, name: e.target.value })}
                    placeholder="e.g., PayPal, Bank Transfer"
                  />
                </div>
              </div>
              <div>
                <Label>Description</Label>
                <Input
                  value={newGateway.description}
                  onChange={(e) => setNewGateway({ ...newGateway, description: e.target.value })}
                  placeholder="Brief description of this payment method"
                />
              </div>
              <div>
                <Label>Logo URL (optional)</Label>
                <Input
                  value={newGateway.logo_url}
                  onChange={(e) => setNewGateway({ ...newGateway, logo_url: e.target.value })}
                  placeholder="https://..."
                />
              </div>
              {newGateway.gateway_type === 'manual' && (
                <div>
                  <Label>Payment Instructions *</Label>
                  <Textarea
                    value={newGateway.instructions}
                    onChange={(e) => setNewGateway({ ...newGateway, instructions: e.target.value })}
                    placeholder="Provide payment instructions (e.g., bank account details, PayPal email, etc.)"
                    rows={4}
                  />
                </div>
              )}
              <Button onClick={addPaymentGateway} className="bg-[#d4af37] hover:bg-[#b8941f]">
                <Plus className="h-4 w-4 mr-2" />
                Add Gateway
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Payment Gateways ({paymentGateways.length})</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {paymentGateways.map((gateway) => (
                  <div key={gateway.gateway_id} className="flex items-center justify-between p-4 border rounded">
                    <div className="flex-1">
                      <p className="font-semibold">{gateway.name}</p>
                      <p className="text-sm text-gray-600">{gateway.description}</p>
                      <p className="text-xs text-gray-500 mt-1">Type: {gateway.gateway_type}</p>
                      {gateway.instructions && (
                        <p className="text-xs text-gray-600 mt-2 whitespace-pre-wrap">{gateway.instructions}</p>
                      )}
                    </div>
                    <Button
                      onClick={() => deletePaymentGateway(gateway.gateway_id)}
                      variant="destructive"
                      size="sm"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
                {paymentGateways.length === 0 && (
                  <p className="text-center text-gray-500 py-8">No payment gateways configured yet</p>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Social Links Tab */}
      {activeTab === 'social' && (
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Add Social Link</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label>Platform</Label>
                  <select
                    className="w-full p-2 border rounded"
                    value={newSocialLink.platform}
                    onChange={(e) => setNewSocialLink({ ...newSocialLink, platform: e.target.value })}
                  >
                    <option value="facebook">Facebook</option>
                    <option value="instagram">Instagram</option>
                    <option value="twitter">Twitter</option>
                    <option value="whatsapp">WhatsApp</option>
                    <option value="tiktok">TikTok</option>
                    <option value="youtube">YouTube</option>
                  </select>
                </div>
                <div>
                  <Label>URL *</Label>
                  <Input
                    value={newSocialLink.url}
                    onChange={(e) => setNewSocialLink({ ...newSocialLink, url: e.target.value })}
                    placeholder="https://..."
                  />
                </div>
              </div>
              <Button onClick={addSocialLink} className="bg-[#d4af37] hover:bg-[#b8941f]">
                <Plus className="h-4 w-4 mr-2" />
                Add Social Link
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Social Links ({socialLinks.length})</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {socialLinks.map((link) => (
                  <div key={link.id} className="flex items-center justify-between p-4 border rounded">
                    <div>
                      <p className="font-semibold capitalize">{link.platform}</p>
                      <p className="text-sm text-gray-600">{link.url}</p>
                    </div>
                    <Button
                      onClick={() => deleteSocialLink(link.id)}
                      variant="destructive"
                      size="sm"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
                {socialLinks.length === 0 && (
                  <p className="text-center text-gray-500 py-8">No social links added yet</p>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* External Links Tab */}
      {activeTab === 'external' && (
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Add External Link (Max 3)</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label>Title *</Label>
                  <Input
                    value={newExternalLink.title}
                    onChange={(e) => setNewExternalLink({ ...newExternalLink, title: e.target.value })}
                    placeholder="e.g., Guide d'achat"
                  />
                </div>
                <div>
                  <Label>URL *</Label>
                  <Input
                    value={newExternalLink.url}
                    onChange={(e) => setNewExternalLink({ ...newExternalLink, url: e.target.value })}
                    placeholder="https://..."
                  />
                </div>
              </div>
              <Button 
                onClick={addExternalLink} 
                className="bg-[#d4af37] hover:bg-[#b8941f]"
                disabled={externalLinks.length >= 3}
              >
                <Plus className="h-4 w-4 mr-2" />
                Add External Link
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>External Links ({externalLinks.length}/3)</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {externalLinks.map((link) => (
                  <div key={link.id} className="flex items-center justify-between p-4 border rounded">
                    <div>
                      <p className="font-semibold">{link.title}</p>
                      <p className="text-sm text-gray-600">{link.url}</p>
                    </div>
                    <Button
                      onClick={() => deleteExternalLink(link.id)}
                      variant="destructive"
                      size="sm"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
                {externalLinks.length === 0 && (
                  <p className="text-center text-gray-500 py-8">No external links added yet</p>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Floating Announcement Tab */}
      {activeTab === 'announcement' && (
        <Card>
          <CardHeader>
            <CardTitle>Floating Announcement (Shein-Style Popup)</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-2">
              <Switch
                checked={announcement.enabled}
                onCheckedChange={(checked) => setAnnouncement({ ...announcement, enabled: checked })}
              />
              <Label>Enable Floating Announcement</Label>
            </div>

            <div>
              <Label>Title (optional)</Label>
              <Input
                value={announcement.title || ''}
                onChange={(e) => setAnnouncement({ ...announcement, title: e.target.value })}
                placeholder="Special Offer!"
              />
            </div>

            <div>
              <Label>Message *</Label>
              <Textarea
                value={announcement.message}
                onChange={(e) => setAnnouncement({ ...announcement, message: e.target.value })}
                placeholder="Get 20% OFF on all products this week!"
                rows={4}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label>Image URL (optional)</Label>
                <Input
                  value={announcement.image_url || ''}
                  onChange={(e) => setAnnouncement({ ...announcement, image_url: e.target.value })}
                  placeholder="https://..."
                />
              </div>
              <div>
                <Label>Link URL (optional)</Label>
                <Input
                  value={announcement.link_url || ''}
                  onChange={(e) => setAnnouncement({ ...announcement, link_url: e.target.value })}
                  placeholder="https://..."
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label>Link Button Text</Label>
                <Input
                  value={announcement.link_text}
                  onChange={(e) => setAnnouncement({ ...announcement, link_text: e.target.value })}
                  placeholder="Learn More"
                />
              </div>
              <div>
                <Label>Display Frequency</Label>
                <select
                  className="w-full p-2 border rounded"
                  value={announcement.frequency}
                  onChange={(e) => setAnnouncement({ ...announcement, frequency: e.target.value })}
                >
                  <option value="once_per_session">Once per session</option>
                  <option value="every_visit">Every visit</option>
                  <option value="daily">Once per day</option>
                </select>
              </div>
            </div>

            <Button onClick={saveAnnouncement} className="bg-[#d4af37] hover:bg-[#b8941f]">
              <Save className="h-4 w-4 mr-2" />
              Save Announcement
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Bulk Email Tab */}
      {activeTab === 'bulk-email' && (
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Send Bulk Email / Newsletter</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label>Recipient Filter</Label>
                <select
                  className="w-full p-2 border rounded"
                  value={bulkEmail.recipient_filter}
                  onChange={(e) => setBulkEmail({ ...bulkEmail, recipient_filter: e.target.value })}
                >
                  <option value="all">All Customers</option>
                  <option value="with_orders">Customers with Orders</option>
                </select>
              </div>

              <div>
                <Label>Subject *</Label>
                <Input
                  value={bulkEmail.subject}
                  onChange={(e) => setBulkEmail({ ...bulkEmail, subject: e.target.value })}
                  placeholder="e.g., Special Coupon Code Inside!"
                />
              </div>

              <div>
                <Label>Message *</Label>
                <Textarea
                  value={bulkEmail.message}
                  onChange={(e) => setBulkEmail({ ...bulkEmail, message: e.target.value })}
                  placeholder="Use code WELCOME10 for 10% OFF your next order! Valid until [date]"
                  rows={6}
                />
              </div>

              <Button
                onClick={sendBulkEmail}
                className="bg-green-600 hover:bg-green-700"
                disabled={loading}
              >
                <Mail className="h-4 w-4 mr-2" />
                {loading ? 'Sending...' : 'Send Bulk Email'}
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Email History</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {bulkEmailHistory.map((email) => (
                  <div key={email.id} className="p-4 border rounded">
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="font-semibold">{email.subject}</p>
                        <p className="text-sm text-gray-600 mt-1">{email.message.substring(0, 100)}...</p>
                      </div>
                      <p className="text-xs text-gray-500">Sent to {email.sent_to} customers</p>
                    </div>
                    <p className="text-xs text-gray-400 mt-2">
                      {new Date(email.sent_at).toLocaleString()}
                    </p>
                  </div>
                ))}
                {bulkEmailHistory.length === 0 && (
                  <p className="text-center text-gray-500 py-8">No emails sent yet</p>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default AdminSettings;
