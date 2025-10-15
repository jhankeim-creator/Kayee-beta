import { useEffect, useState, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { CartContext } from '../App';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import Footer from '../components/Footer';
import axios from 'axios';

const ShopPage = () => {
  const { category } = useParams();
  const { API, addToCart } = useContext(CartContext);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadProducts();
  }, [category]);

  const loadProducts = async () => {
    setLoading(true);
    try {
      const url = category ? `${API}/products?category=${category}` : `${API}/products`;
      const response = await axios.get(url);
      setProducts(response.data);
    } catch (error) {
      console.error('Failed to load products:', error);
    } finally {
      setLoading(false);
    }
  };

  const getTitle = () => {
    if (category === 'fashion') return 'Fashion Collection';
    if (category === 'jewelry') return 'Jewelry Collection';
    return 'All Products';
  };

  return (
    <div className="min-h-screen">
      <div className="pt-32 pb-20">
        <div className="container mx-auto px-4">
          <h1
            className="text-4xl md:text-5xl font-bold text-center mb-12"
            style={{ fontFamily: 'Playfair Display' }}
            data-testid="shop-page-title"
          >
            {getTitle()}
          </h1>

          {loading ? (
            <div className="text-center py-20">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-[#d4af37]"></div>
            </div>
          ) : products.length === 0 ? (
            <div className="text-center py-20">
              <p className="text-gray-600 text-lg">No products found in this category.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {products.map((product) => (
                <Card
                  key={product.id}
                  className="group cursor-pointer border-none shadow-lg hover:shadow-xl transition-shadow duration-300"
                  onClick={() => navigate(`/product/${product.id}`)}
                  data-testid={`product-card-${product.id}`}
                >
                  <div className="relative overflow-hidden">
                    <img
                      src={product.images[0]}
                      alt={product.name}
                      className="w-full h-80 object-cover transition-transform duration-500 group-hover:scale-110"
                    />
                    {product.featured && (
                      <div className="absolute top-4 right-4 bg-[#d4af37] text-white px-3 py-1 text-sm font-semibold">
                        Featured
                      </div>
                    )}
                    {product.stock <= 5 && product.stock > 0 && (
                      <div className="absolute top-4 left-4 bg-red-600 text-white px-3 py-1 text-sm font-semibold">
                        Only {product.stock} left
                      </div>
                    )}
                    {product.stock === 0 && (
                      <div className="absolute top-4 left-4 bg-gray-800 text-white px-3 py-1 text-sm font-semibold">
                        Out of Stock
                      </div>
                    )}
                  </div>
                  <CardContent className="p-4">
                    <h3 className="font-semibold text-lg mb-2 line-clamp-1">{product.name}</h3>
                    <p className="text-gray-600 text-sm mb-3 line-clamp-2">{product.description}</p>
                    <div className="flex items-center justify-between">
                      <span className="text-2xl font-bold text-[#d4af37]">${product.price.toFixed(2)}</span>
                      <Button
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          addToCart(product);
                        }}
                        disabled={product.stock === 0}
                        className="bg-black hover:bg-gray-800 text-white"
                        data-testid={`add-to-cart-${product.id}`}
                      >
                        {product.stock === 0 ? 'Out of Stock' : 'Add to Cart'}
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default ShopPage;