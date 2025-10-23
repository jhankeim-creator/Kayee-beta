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

      <Footer />
    </div>
  );
};

export default HomePage;