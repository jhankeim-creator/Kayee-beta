import { useEffect, useState, useContext, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ArrowRight, ShoppingBag, Star, ChevronLeft, ChevronRight } from 'lucide-react';
import { CartContext } from '../App';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import Footer from '../components/Footer';
import axios from 'axios';

const HomePage = () => {
  const { API, addToCart } = useContext(CartContext);
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [bestSellers, setBestSellers] = useState([]);
  const [categories, setCategories] = useState([]);
  const navigate = useNavigate();
  const scrollContainerRef = useRef(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [productsRes, categoriesRes, bestSellersRes] = await Promise.all([
        axios.get(`${API}/products?featured=true`),
        axios.get(`${API}/categories`),
        axios.get(`${API}/products/best-sellers?limit=12`)
      ]);
      setFeaturedProducts(productsRes.data.slice(0, 30));
      setCategories(categoriesRes.data);
      setBestSellers(bestSellersRes.data);
    } catch (error) {
      console.error('Failed to load data:', error);
    }
  };

  const scrollLeft = () => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollBy({ left: -400, behavior: 'smooth' });
    }
  };

  const scrollRight = () => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollBy({ left: 400, behavior: 'smooth' });
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

      {/* Best Sellers - Horizontal Scroll */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center mb-8">
            <h2
              className="text-4xl md:text-5xl font-bold"
              style={{ fontFamily: 'Playfair Display' }}
            >
              Best Sellers
            </h2>
            <div className="flex gap-2">
              <Button
                onClick={scrollLeft}
                variant="outline"
                size="icon"
                className="rounded-full"
              >
                <ChevronLeft className="h-5 w-5" />
              </Button>
              <Button
                onClick={scrollRight}
                variant="outline"
                size="icon"
                className="rounded-full"
              >
                <ChevronRight className="h-5 w-5" />
              </Button>
            </div>
          </div>
          
          <div 
            ref={scrollContainerRef}
            className="flex gap-6 overflow-x-auto scrollbar-hide scroll-smooth pb-4"
            style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
          >
            {bestSellers.map((product) => (
              <div
                key={product.id}
                className="flex-shrink-0 w-72 group cursor-pointer"
                onClick={() => navigate(`/product/${product.id}`)}
              >
                <div className="relative overflow-hidden rounded-lg mb-4 bg-gray-100" style={{ aspectRatio: '1/1' }}>
                  {product.images && product.images[0] && (
                    <img
                      src={product.images[0]}
                      alt={product.name}
                      className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                    />
                  )}
                  {product.on_sale && (
                    <span className="absolute top-2 left-2 bg-red-500 text-white px-3 py-1 text-xs font-bold rounded">
                      SALE
                    </span>
                  )}
                  {product.is_new && (
                    <span className="absolute top-2 right-2 bg-green-500 text-white px-3 py-1 text-xs font-bold rounded">
                      NEW
                    </span>
                  )}
                  {product.best_seller && (
                    <span className="absolute top-2 left-2 bg-[#d4af37] text-white px-3 py-1 text-xs font-bold rounded">
                      BEST SELLER
                    </span>
                  )}
                </div>
                <h3 className="font-semibold text-lg mb-2 line-clamp-2">{product.name}</h3>
                <div className="flex items-center gap-2">
                  {product.on_sale && product.original_price ? (
                    <>
                      <span className="text-red-600 font-bold text-xl">${product.price.toFixed(2)}</span>
                      <span className="text-gray-400 line-through text-sm">${product.original_price.toFixed(2)}</span>
                    </>
                  ) : (
                    <span className="text-gray-900 font-bold text-xl">${product.price.toFixed(2)}</span>
                  )}
                </div>
                {product.rating && (
                  <div className="flex items-center gap-1 mt-2">
                    <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                    <span className="text-sm text-gray-600">{product.rating} ({product.reviews_count || 0})</span>
                  </div>
                )}
              </div>
            ))}
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

      {/* We Accept Payment Methods */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2
            className="text-4xl md:text-5xl font-bold text-center mb-12"
            style={{ fontFamily: 'Playfair Display' }}
          >
            We Accept
          </h2>
          <div className="flex flex-wrap justify-center items-center gap-8 md:gap-12">
            {/* Stripe */}
            <div className="flex items-center justify-center p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow w-32 h-20">
              <svg className="h-8" viewBox="0 0 60 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M59.64 14.28h-8.06c.19 1.93 1.6 2.55 3.2 2.55 1.64 0 2.96-.37 4.05-.95v3.32a8.33 8.33 0 0 1-4.56 1.1c-4.01 0-6.83-2.5-6.83-7.48 0-4.19 2.39-7.52 6.3-7.52 3.92 0 5.96 3.28 5.96 7.5 0 .4-.04 1.26-.06 1.48zm-5.92-5.62c-1.03 0-2.17.73-2.17 2.58h4.25c0-1.85-1.07-2.58-2.08-2.58zM40.95 20.3c-1.44 0-2.32-.6-2.9-1.04l-.02 4.63-4.12.87V5.57h3.76l.08 1.02a4.7 4.7 0 0 1 3.23-1.29c2.9 0 5.62 2.6 5.62 7.4 0 5.23-2.7 7.6-5.65 7.6zM40 8.95c-.95 0-1.54.34-1.97.81l.02 6.12c.4.44.98.78 1.95.78 1.52 0 2.54-1.65 2.54-3.87 0-2.15-1.04-3.84-2.54-3.84zM28.24 5.57h4.13v14.44h-4.13V5.57zm0-4.7L32.37 0v3.36l-4.13.88V.88zm-4.32 9.35v9.79H19.8V5.57h3.7l.12 1.22c1-1.77 3.07-1.41 3.62-1.22v3.79c-.52-.17-2.29-.43-3.32.86zm-8.55 4.72c0 2.43 2.6 1.68 3.12 1.46v3.36c-.55.3-1.54.54-2.89.54a4.15 4.15 0 0 1-4.27-4.24l.01-13.17 4.02-.86v3.54h3.14V9.1h-3.13v5.85zm-4.91.7c0 2.97-2.31 4.66-5.73 4.66a11.2 11.2 0 0 1-4.46-.93v-3.93c1.38.75 3.1 1.31 4.46 1.31.92 0 1.53-.24 1.53-1C6.26 13.77 0 14.51 0 9.95 0 7.04 2.28 5.3 5.62 5.3c1.36 0 2.72.2 4.09.75v3.88a9.23 9.23 0 0 0-4.1-1.06c-.86 0-1.44.25-1.44.9 0 1.85 6.29.97 6.29 5.88z" fill="#635BFF"/>
              </svg>
            </div>
            
            {/* Plisio Crypto */}
            <div className="flex items-center justify-center p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow w-32 h-20">
              <div className="text-center">
                <div className="text-2xl font-bold text-[#d4af37]">₿</div>
                <div className="text-xs text-gray-600 mt-1">Crypto</div>
              </div>
            </div>
            
            {/* PayPal */}
            <div className="flex items-center justify-center p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow w-32 h-20">
              <svg className="h-8" viewBox="0 0 100 32" xmlns="http://www.w3.org/2000/svg">
                <path d="M12.237 2.8H4.442a.65.65 0 0 0-.642.538L.067 25.74a.39.39 0 0 0 .384.45h2.776a.65.65 0 0 0 .643-.538l1.009-6.384a.65.65 0 0 1 .643-.538h1.483c3.083 0 4.862-1.492 5.33-4.448.21-1.295.006-2.313-.609-3.026-.676-.786-1.877-1.202-3.472-1.202h-.01zm.55 4.384c-.27 1.777-1.634 1.777-2.953 1.777h-.75l.527-3.336a.39.39 0 0 1 .385-.322h.323c.844 0 1.64 0 2.052.481.247.289.32.722.417 1.4zM35.21 7.133h-2.783a.39.39 0 0 0-.385.322l-.099.626-.156-.227c-.486-.705-1.57-.94-2.65-.94-2.48 0-4.6 1.88-5.011 4.517-.214 1.313.091 2.566.835 3.438.683.8 1.659 1.135 2.822 1.135 1.996 0 3.104-1.283 3.104-1.283l-.1.622a.39.39 0 0 0 .384.45h2.506a.65.65 0 0 0 .643-.538l1.214-7.686a.39.39 0 0 0-.384-.45zm-3.86 4.364c-.216 1.28-1.234 2.14-2.53 2.14-.65 0-1.17-.21-1.504-.606-.333-.394-.458-.955-.352-1.58.206-1.268 1.24-2.156 2.515-2.156.64 0 1.155.21 1.495.61.342.403.474.968.376 1.592z" fill="#253B80"/>
                <path d="M55.433 7.133h-2.79a.65.65 0 0 0-.538.286l-3.102 4.57-1.315-4.39a.65.65 0 0 0-.622-.466h-2.74a.39.39 0 0 0-.37.513l2.48 7.277-2.33 3.286a.39.39 0 0 0 .318.615h2.787a.65.65 0 0 0 .536-.282l7.48-10.79a.39.39 0 0 0-.32-.616z" fill="#179BD7"/>
                <path d="M67.222 2.8h-7.795a.65.65 0 0 0-.642.538l-3.733 23.402a.39.39 0 0 0 .385.45h2.913a.45.45 0 0 0 .446-.38l1.043-6.585a.65.65 0 0 1 .643-.538h1.483c3.083 0 4.862-1.492 5.33-4.448.21-1.295.006-2.313-.609-3.026-.676-.786-1.877-1.202-3.472-1.202h-.01zm.55 4.384c-.27 1.777-1.634 1.777-2.953 1.777h-.75l.527-3.336a.39.39 0 0 1 .385-.322h.323c.844 0 1.64 0 2.052.481.247.289.32.722.417 1.4z" fill="#253B80"/>
                <path d="M90.195 7.133h-2.783a.39.39 0 0 0-.385.322l-.099.626-.156-.227c-.486-.705-1.57-.94-2.65-.94-2.48 0-4.6 1.88-5.011 4.517-.214 1.313.091 2.566.835 3.438.683.8 1.659 1.135 2.822 1.135 1.996 0 3.104-1.283 3.104-1.283l-.1.622a.39.39 0 0 0 .384.45h2.506a.65.65 0 0 0 .643-.538l1.214-7.686a.39.39 0 0 0-.384-.45zm-3.86 4.364c-.216 1.28-1.234 2.14-2.53 2.14-.65 0-1.17-.21-1.504-.606-.333-.394-.458-.955-.352-1.58.206-1.268 1.24-2.156 2.515-2.156.64 0 1.155.21 1.495.61.342.403.474.968.376 1.592z" fill="#179BD7"/>
                <path d="M95.85 2.8l-3.792 24.19a.39.39 0 0 0 .385.45h2.412a.65.65 0 0 0 .643-.538l3.733-23.402a.39.39 0 0 0-.385-.45h-2.612a.39.39 0 0 0-.385.322z" fill="#179BD7"/>
              </svg>
            </div>
            
            {/* Manual Payments */}
            <div className="flex items-center justify-center p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow w-32 h-20">
              <div className="text-center">
                <div className="text-2xl font-bold text-[#d4af37]">💳</div>
                <div className="text-xs text-gray-600 mt-1">Manual</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Why Choose Us Section with 3D Emojis */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <h2
            className="text-4xl md:text-5xl font-bold text-center mb-12"
            style={{ fontFamily: 'Playfair Display' }}
          >
            Why Choose Us
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center p-6 bg-gray-50 rounded-lg shadow-sm hover:shadow-md transition-shadow">
              <div className="text-6xl mb-4 animate-bounce">⌚</div>
              <h3 className="text-2xl font-bold mb-3" style={{ fontFamily: 'Playfair Display' }}>
                Premium Quality
              </h3>
              <p className="text-gray-600">
                High-quality 1:1 replicas with attention to every detail
              </p>
            </div>
            <div className="text-center p-6 bg-gray-50 rounded-lg shadow-sm hover:shadow-md transition-shadow">
              <div className="text-6xl mb-4 animate-bounce" style={{ animationDelay: '0.1s' }}>🚚</div>
              <h3 className="text-2xl font-bold mb-3" style={{ fontFamily: 'Playfair Display' }}>
                Fast Shipping
              </h3>
              <p className="text-gray-600">
                Worldwide delivery with FedEx Express in 3-5 days
              </p>
            </div>
            <div className="text-center p-6 bg-gray-50 rounded-lg shadow-sm hover:shadow-md transition-shadow">
              <div className="text-6xl mb-4 animate-bounce" style={{ animationDelay: '0.2s' }}>🔒</div>
              <h3 className="text-2xl font-bold mb-3" style={{ fontFamily: 'Playfair Display' }}>
                Secure Payment
              </h3>
              <p className="text-gray-600">
                Multiple secure payment options available
              </p>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default HomePage;