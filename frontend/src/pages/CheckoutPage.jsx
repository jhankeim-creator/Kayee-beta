import { useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { CartContext } from '../App';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { RadioGroup, RadioGroupItem } from '../components/ui/radio-group';
import Footer from '../components/Footer';
import axios from 'axios';
import { toast } from 'sonner';
import { CreditCard, Coins, Wallet, DollarSign } from 'lucide-react';

const CheckoutPage = () => {
  const { cart, cartTotal, clearCart, API } = useContext(CartContext);
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [orderPlaced, setOrderPlaced] = useState(false);
  const [shippingMethod, setShippingMethod] = useState('free');
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    postalCode: '',
    country: '',
    paymentMethod: 'stripe',
    notes: ''
  });

  useEffect(() => {
    if (cart.length === 0 && !orderPlaced) {
      navigate('/cart');
    }
  }, [cart, navigate, orderPlaced]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const orderData = {
        user_email: formData.email,
        user_name: formData.name,
        items: cart.map(item => ({
          product_id: item.id,
          name: item.name,
          price: item.price,
          quantity: item.quantity,
          image: item.images[0]
        })),
        total: cartTotal,
        payment_method: formData.paymentMethod,
        shipping_address: {
          address: formData.address,
          city: formData.city,
          postal_code: formData.postalCode,
          country: formData.country
        },
        phone: formData.phone,
        notes: formData.notes || null
      };

      const response = await axios.post(`${API}/orders`, orderData);
      setOrderPlaced(true);
      clearCart();
      toast.success('Order placed successfully!');
      navigate(`/order-success/${response.data.id}`);
    } catch (error) {
      console.error('Failed to create order:', error);
      toast.error('Failed to place order. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const paymentMethods = [
    { id: 'stripe', name: 'Carte Bancaire (Stripe)', icon: CreditCard, description: 'Paiement par carte bancaire' },
    { id: 'paypal', name: 'PayPal', icon: DollarSign, description: 'Paiement sécurisé via PayPal' },
    { id: 'binance', name: 'Binance Pay', icon: Coins, description: '0% frais - Paiement crypto instantané' },
    { id: 'plisio', name: 'Plisio', icon: Wallet, description: '100+ cryptomonnaies acceptées' },
    { id: 'manual', name: 'Paiement Manuel', icon: DollarSign, description: 'Virement bancaire ou crypto manuel' }
  ];

  return (
    <div className="min-h-screen">
      <div className="pt-32 pb-20">
        <div className="container mx-auto px-4">
          <h1
            className="text-4xl md:text-5xl font-bold mb-12 text-center"
            style={{ fontFamily: 'Playfair Display' }}
            data-testid="checkout-title"
          >
            Checkout
          </h1>

          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Checkout Form */}
              <div className="lg:col-span-2 space-y-6">
                {/* Contact Information */}
                <Card>
                  <CardHeader>
                    <CardTitle>Contact Information</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="name">Full Name *</Label>
                        <Input
                          id="name"
                          name="name"
                          value={formData.name}
                          onChange={handleChange}
                          required
                          data-testid="input-name"
                        />
                      </div>
                      <div>
                        <Label htmlFor="email">Email *</Label>
                        <Input
                          id="email"
                          name="email"
                          type="email"
                          value={formData.email}
                          onChange={handleChange}
                          required
                          data-testid="input-email"
                        />
                      </div>
                    </div>
                    <div>
                      <Label htmlFor="phone">Phone Number *</Label>
                      <Input
                        id="phone"
                        name="phone"
                        type="tel"
                        value={formData.phone}
                        onChange={handleChange}
                        required
                        data-testid="input-phone"
                      />
                    </div>
                  </CardContent>
                </Card>

                {/* Shipping Address */}
                <Card>
                  <CardHeader>
                    <CardTitle>Shipping Address</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <Label htmlFor="address">Street Address *</Label>
                      <Input
                        id="address"
                        name="address"
                        value={formData.address}
                        onChange={handleChange}
                        required
                        data-testid="input-address"
                      />
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div>
                        <Label htmlFor="city">City *</Label>
                        <Input
                          id="city"
                          name="city"
                          value={formData.city}
                          onChange={handleChange}
                          required
                          data-testid="input-city"
                        />
                      </div>
                      <div>
                        <Label htmlFor="postalCode">Postal Code *</Label>
                        <Input
                          id="postalCode"
                          name="postalCode"
                          value={formData.postalCode}
                          onChange={handleChange}
                          required
                          data-testid="input-postal-code"
                        />
                      </div>
                      <div>
                        <Label htmlFor="country">Country *</Label>
                        <Input
                          id="country"
                          name="country"
                          value={formData.country}
                          onChange={handleChange}
                          required
                          data-testid="input-country"
                        />
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Payment Method */}
                <Card>
                  <CardHeader>
                    <CardTitle>Payment Method</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <RadioGroup
                      value={formData.paymentMethod}
                      onValueChange={(value) => setFormData({ ...formData, paymentMethod: value })}
                      data-testid="payment-method-selector"
                    >
                      {paymentMethods.map((method) => (
                        <div
                          key={method.id}
                          className="flex items-start space-x-3 p-4 border rounded-lg cursor-pointer hover:bg-gray-50"
                          onClick={() => setFormData({ ...formData, paymentMethod: method.id })}
                        >
                          <RadioGroupItem value={method.id} id={method.id} />
                          <div className="flex-1">
                            <Label htmlFor={method.id} className="flex items-center cursor-pointer">
                              <method.icon className="h-5 w-5 mr-2 text-[#d4af37]" />
                              <span className="font-semibold">{method.name}</span>
                            </Label>
                            <p className="text-sm text-gray-600 mt-1">{method.description}</p>
                          </div>
                        </div>
                      ))}
                    </RadioGroup>
                    <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                      <p className="text-sm text-yellow-800">
                        <strong>Note:</strong> After placing your order, you'll receive payment instructions via email.
                        For manual and crypto payments, please confirm payment in your order confirmation page.
                      </p>
                    </div>
                  </CardContent>
                </Card>

                {/* Order Notes */}
                <Card>
                  <CardHeader>
                    <CardTitle>Order Notes (Optional)</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Textarea
                      name="notes"
                      placeholder="Any special instructions or notes..."
                      value={formData.notes}
                      onChange={handleChange}
                      rows={4}
                      data-testid="input-notes"
                    />
                  </CardContent>
                </Card>
              </div>

              {/* Order Summary */}
              <div className="lg:col-span-1">
                <Card className="sticky top-24">
                  <CardHeader>
                    <CardTitle>Order Summary</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-3 max-h-64 overflow-y-auto">
                      {cart.map((item) => (
                        <div key={item.id} className="flex gap-3">
                          <img src={item.images[0]} alt={item.name} className="w-16 h-16 object-cover" />
                          <div className="flex-1">
                            <p className="font-semibold text-sm line-clamp-1">{item.name}</p>
                            <p className="text-sm text-gray-600">Qty: {item.quantity}</p>
                            <p className="text-sm font-bold text-[#d4af37]">${(item.price * item.quantity).toFixed(2)}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="border-t pt-4 space-y-2">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Subtotal</span>
                        <span className="font-semibold">${cartTotal.toFixed(2)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Shipping</span>
                        <span className="font-semibold">TBD</span>
                      </div>
                      <div className="border-t pt-2 flex justify-between text-lg font-bold">
                        <span>Total</span>
                        <span className="text-[#d4af37]" data-testid="order-total">${cartTotal.toFixed(2)}</span>
                      </div>
                    </div>
                    <Button
                      type="submit"
                      disabled={loading}
                      className="w-full bg-[#d4af37] hover:bg-[#b8941f] text-white py-6 text-lg"
                      data-testid="place-order-button"
                    >
                      {loading ? 'Processing...' : 'Place Order'}
                    </Button>
                  </CardContent>
                </Card>
              </div>
            </div>
          </form>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default CheckoutPage;