import { useEffect, useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ArrowRight, ShoppingBag, Star } from 'lucide-react';
import { CartContext } from '../App';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import Footer from '../components/Footer';
import axios from 'axios';

const HomePage = () => {
  const { API, addToCart } = useContext(CartContext);
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [productsRes, categoriesRes] = await Promise.all([
        axios.get(`${API}/products?featured=true`),
        axios.get(`${API}/categories`)
      ]);
      setFeaturedProducts(productsRes.data.slice(0, 30));
      setCategories(categoriesRes.data);
    } catch (error) {
      console.error('Failed to load data:', error);
    }
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section with Background Image */}
      <section
        className="relative h-[600px] bg-cover bg-center"
        style={{
          backgroundImage: 'url(/hero-bg.png)',
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}
      >
        <div className="absolute inset-0 bg-black bg-opacity-50"></div>
        <div className="relative h-full flex items-center justify-center text-center px-4">
          <div className="max-w-4xl">
            <h1
              className="text-5xl md:text-7xl font-bold text-white mb-6"
              style={{ fontFamily: 'Playfair Display' }}
            >
              Luxury 1:1 Replica Watches
            </h1>
            <p className="text-xl md:text-2xl text-white mb-8">
              Premium Quality Replica Watches, Clothing & Accessories
            </p>
            <Button
              onClick={() => navigate('/shop')}
              size="lg"
              className="bg-[#d4af37] hover:bg-[#b8941f] text-white text-lg px-8 py-6"
            >
              Shop Now
            </Button>
          </div>
        </div>
      </section>

      {/* Why Choose Us Section with 3D Emojis */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2
            className="text-4xl md:text-5xl font-bold text-center mb-12"
            style={{ fontFamily: 'Playfair Display' }}
          >
            Pourquoi Nous Choisir
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center p-6 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
              <div className="text-6xl mb-4 animate-bounce">⌚</div>
              <h3 className="text-2xl font-bold mb-3" style={{ fontFamily: 'Playfair Display' }}>
                Qualité Premium
              </h3>
              <p className="text-gray-600">
                Répliques 1:1 de haute qualité avec attention aux détails
              </p>
            </div>
            <div className="text-center p-6 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
              <div className="text-6xl mb-4 animate-bounce" style={{ animationDelay: '0.1s' }}>🚚</div>
              <h3 className="text-2xl font-bold mb-3" style={{ fontFamily: 'Playfair Display' }}>
                Livraison Rapide
              </h3>
              <p className="text-gray-600">
                Expédition mondiale avec FedEx Express en 3-5 jours
              </p>
            </div>
            <div className="text-center p-6 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
              <div className="text-6xl mb-4 animate-bounce" style={{ animationDelay: '0.2s' }}>🔒</div>
              <h3 className="text-2xl font-bold mb-3" style={{ fontFamily: 'Playfair Display' }}>
                Paiement Sécurisé
              </h3>
              <p className="text-gray-600">
                Plusieurs options de paiement sécurisées disponibles
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Products - 3 columns grid Ecwid-style */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2
              className="text-4xl md:text-5xl font-bold mb-4"
              style={{ fontFamily: 'Playfair Display' }}
            >
              Featured Collection
            </h2>
            <p className="text-gray-600 text-lg">Handpicked items just for you</p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
            {featuredProducts.map((product) => (
              <Card
                key={product.id}
                className="group cursor-pointer border-none shadow-md hover:shadow-2xl transition-all duration-300"
                onClick={() => navigate(`/product/${product.id}`)}
                data-testid={`featured-product-${product.id}`}
              >
                <div className="relative overflow-hidden aspect-square">
                  <img
                    src={product.images[0]}
                    alt={product.name}
                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                  />
                  {/* Multiple Badges */}
                  <div className="absolute top-3 left-3 flex flex-col gap-2">
                    {product.on_sale && (
                      <span className="bg-red-600 text-white px-3 py-1 text-xs font-bold rounded-full shadow-lg">
                        SALE
                      </span>
                    )}
                    {product.is_new && (
                      <span className="bg-green-600 text-white px-3 py-1 text-xs font-bold rounded-full shadow-lg">
                        NEW
                      </span>
                    )}
                    {product.best_seller && (
                      <span className="bg-[#d4af37] text-white px-3 py-1 text-xs font-bold rounded-full shadow-lg">
                        BEST SELLER
                      </span>
                    )}
                  </div>
                  {product.featured && !product.on_sale && !product.is_new && !product.best_seller && (
                    <div className="absolute top-3 right-3 bg-purple-600 text-white px-3 py-1 text-xs font-bold rounded-full shadow-lg">
                      FEATURED
                    </div>
                  )}
                  {/* Quick Add Button on Hover */}
                  <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-300 flex items-center justify-center opacity-0 group-hover:opacity-100">
                    <Button
                      size="sm"
                      onClick={(e) => {
                        e.stopPropagation();
                        addToCart(product);
                      }}
                      className="bg-white text-black hover:bg-[#d4af37] hover:text-white font-semibold px-6"
                    >
                      Quick Add
                    </Button>
                  </div>
                </div>
                <CardContent className="p-4">
                  <h3 className="font-semibold text-base mb-2 line-clamp-2 min-h-[3rem]">{product.name}</h3>
                  <div className="flex items-center gap-2 mb-2">
                    {product.on_sale && product.compare_at_price ? (
                      <>
                        <span className="text-xl font-bold text-red-600">${product.price.toFixed(2)}</span>
                        <span className="text-sm text-gray-500 line-through">${product.compare_at_price.toFixed(2)}</span>
                      </>
                    ) : (
                      <span className="text-xl font-bold text-[#d4af37]">${product.price.toFixed(2)}</span>
                    )}
                  </div>
                  {product.rating > 0 && (
                    <div className="flex items-center gap-1 text-xs text-gray-600">
                      <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                      <span>{product.rating.toFixed(1)}</span>
                      {product.reviews_count > 0 && <span>({product.reviews_count})</span>}
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="text-center mt-12">
            <Button
              onClick={() => navigate('/shop')}
              variant="outline"
              size="lg"
              className="border-2 border-black hover:bg-black hover:text-white"
            >
              View All Products <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-[#1a1a1a] text-white">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <ShoppingBag className="h-12 w-12 mx-auto mb-4 text-[#d4af37]" />
              <h3 className="text-xl font-bold mb-2">Premium Quality</h3>
              <p className="text-gray-400">Curated collection of the finest fashion and jewelry</p>
            </div>
            <div>
              <Star className="h-12 w-12 mx-auto mb-4 text-[#d4af37]" />
              <h3 className="text-xl font-bold mb-2">Secure Payments</h3>
              <p className="text-gray-400">Multiple payment options including crypto</p>
            </div>
            <div>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto mb-4 text-[#d4af37]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
              </svg>
              <h3 className="text-xl font-bold mb-2">Fast Shipping</h3>
              <p className="text-gray-400">Track your order every step of the way</p>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default HomePage;