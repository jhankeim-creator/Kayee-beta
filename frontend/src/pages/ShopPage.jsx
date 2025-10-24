import { useEffect, useState, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { CartContext } from '../App';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import Footer from '../components/Footer';
import axios from 'axios';
import { toast } from 'sonner';
import { Heart } from 'lucide-react';

const ShopPage = () => {
  const { category } = useParams();
  const { API, addToCart, token } = useContext(CartContext);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalProducts, setTotalProducts] = useState(0);
  const productsPerPage = 20;
  const navigate = useNavigate();
  const [wishlistItems, setWishlistItems] = useState([]);
  
  // Price filter state
  const [priceRange, setPriceRange] = useState({ min: 0, max: 10000 });
  const [sortBy, setSortBy] = useState('featured'); // featured, price_asc, price_desc, newest

  useEffect(() => {
    setPage(1);
    loadProducts(1);
  }, [category, priceRange, sortBy]);

  useEffect(() => {
    if (page > 1) {
      loadProducts(page);
    }
  }, [page]);

  const loadProducts = async (currentPage) => {
    setLoading(true);
    try {
      const skip = (currentPage - 1) * productsPerPage;
      const params = new URLSearchParams({
        skip: skip.toString(),
        limit: productsPerPage.toString()
      });
      
      if (category) {
        params.append('category', category);
      }
      
      // Add price filter
      if (priceRange.min > 0) {
        params.append('min_price', priceRange.min.toString());
      }
      if (priceRange.max < 10000) {
        params.append('max_price', priceRange.max.toString());
      }
      
      // Add sort
      if (sortBy) {
        params.append('sort', sortBy);
      }
      
      const [productsRes, countRes] = await Promise.all([
        axios.get(`${API}/products?${params.toString()}`),
        axios.get(`${API}/products/count${category ? `?category=${category}` : ''}`)
      ]);
      
      // Client-side filtering and sorting as backup
      let filteredProducts = productsRes.data;
      
      // Apply price filter client-side
      filteredProducts = filteredProducts.filter(p => 
        p.price >= priceRange.min && p.price <= priceRange.max
      );
      
      // Apply sorting client-side
      if (sortBy === 'price_asc') {
        filteredProducts.sort((a, b) => a.price - b.price);
      } else if (sortBy === 'price_desc') {
        filteredProducts.sort((a, b) => b.price - a.price);
      } else if (sortBy === 'newest') {
        filteredProducts.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
      }
      
      setProducts(filteredProducts);
      setTotalProducts(filteredProducts.length);
    } catch (error) {
      console.error('Failed to load products:', error);
    } finally {
      setLoading(false);
    }
  };

  const totalPages = Math.ceil(totalProducts / productsPerPage);

  const handlePageChange = (newPage) => {
    setPage(newPage);
    window.scrollTo({ top: 0, behavior: 'smooth' });
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
            className="text-4xl md:text-5xl font-bold text-center mb-8"
            style={{ fontFamily: 'Playfair Display' }}
            data-testid="shop-page-title"
          >
            {getTitle()}
          </h1>

          {/* Filters Section - Mobile Responsive */}
          <div className="bg-gray-50 p-4 rounded-lg mb-8 space-y-4">
            {/* Price Filter */}
            <div className="flex flex-col space-y-2">
              <span className="font-semibold text-sm">Price Range:</span>
              <div className="flex items-center gap-2 flex-wrap">
                <input
                  type="number"
                  placeholder="Min $"
                  value={priceRange.min}
                  onChange={(e) => setPriceRange({ ...priceRange, min: Number(e.target.value) || 0 })}
                  className="flex-1 min-w-[100px] px-3 py-2 border rounded-md text-sm"
                />
                <span className="text-gray-500">-</span>
                <input
                  type="number"
                  placeholder="Max $"
                  value={priceRange.max}
                  onChange={(e) => setPriceRange({ ...priceRange, max: Number(e.target.value) || 10000 })}
                  className="flex-1 min-w-[100px] px-3 py-2 border rounded-md text-sm"
                />
                <button
                  onClick={() => setPriceRange({ min: 0, max: 10000 })}
                  className="px-4 py-2 text-sm text-white bg-[#d4af37] hover:bg-[#b8941f] rounded-md whitespace-nowrap"
                >
                  Reset
                </button>
              </div>
            </div>

            {/* Sort By */}
            <div className="flex flex-col sm:flex-row sm:items-center gap-2">
              <span className="font-semibold text-sm whitespace-nowrap">Sort by:</span>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="flex-1 px-4 py-2 border rounded-md bg-white text-sm"
              >
                <option value="featured">Featured</option>
                <option value="price_asc">Price: Low to High</option>
                <option value="price_desc">Price: High to Low</option>
                <option value="newest">Newest First</option>
              </select>
            </div>

            {/* Product Count */}
            <div className="text-sm text-gray-600">
              Showing {products.length} of {totalProducts} products
            </div>
          </div>

          {loading ? (
            <div className="text-center py-20">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-[#d4af37]"></div>
            </div>
          ) : products.length === 0 ? (
            <div className="text-center py-20">
              <p className="text-gray-600 text-lg">No products found in this category.</p>
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
              {products.map((product) => (
                <Card
                  key={product.id}
                  className="group cursor-pointer border-none shadow-md hover:shadow-2xl transition-all duration-300"
                  onClick={() => navigate(`/product/${product.id}`)}
                  data-testid={`product-card-${product.id}`}
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
                      {product.stock <= 5 && product.stock > 0 && !product.on_sale && !product.is_new && !product.best_seller && (
                        <span className="bg-orange-600 text-white px-3 py-1 text-xs font-bold rounded-full shadow-lg">
                          Only {product.stock} left
                        </span>
                      )}
                    </div>
                    {product.featured && !product.on_sale && !product.is_new && !product.best_seller && (
                      <div className="absolute top-3 right-3 bg-purple-600 text-white px-3 py-1 text-xs font-bold rounded-full shadow-lg">
                        FEATURED
                      </div>
                    )}
                    {product.stock === 0 && (
                      <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                        <span className="bg-gray-800 text-white px-4 py-2 text-sm font-bold rounded">
                          Out of Stock
                        </span>
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
                        disabled={product.stock === 0}
                        className="bg-white text-black hover:bg-[#d4af37] hover:text-white font-semibold px-6"
                        data-testid={`add-to-cart-${product.id}`}
                      >
                        {product.stock === 0 ? 'Out of Stock' : 'Quick Add'}
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
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {/* Pagination */}
          {totalProducts > productsPerPage && (
            <div className="mt-12 flex justify-center items-center gap-2">
              <Button
                onClick={() => handlePageChange(page - 1)}
                disabled={page === 1}
                variant="outline"
                data-testid="prev-page"
              >
                Previous
              </Button>
              
              <div className="flex gap-2">
                {[...Array(Math.min(5, totalPages))].map((_, idx) => {
                  let pageNumber;
                  if (totalPages <= 5) {
                    pageNumber = idx + 1;
                  } else if (page <= 3) {
                    pageNumber = idx + 1;
                  } else if (page >= totalPages - 2) {
                    pageNumber = totalPages - 4 + idx;
                  } else {
                    pageNumber = page - 2 + idx;
                  }

                  return (
                    <Button
                      key={pageNumber}
                      onClick={() => handlePageChange(pageNumber)}
                      variant={page === pageNumber ? "default" : "outline"}
                      className={page === pageNumber ? "bg-[#d4af37] hover:bg-[#b8941f] text-white" : ""}
                      data-testid={`page-${pageNumber}`}
                    >
                      {pageNumber}
                    </Button>
                  );
                })}
              </div>

              <Button
                onClick={() => handlePageChange(page + 1)}
                disabled={page === totalPages}
                variant="outline"
                data-testid="next-page"
              >
                Next
              </Button>
              
              <span className="ml-4 text-gray-600">
                Page {page} of {totalPages} ({totalProducts} products)
              </span>
            </div>
          )}
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default ShopPage;