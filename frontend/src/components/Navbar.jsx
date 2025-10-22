import { useState, useContext, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShoppingCart, User, Menu, X, Search, LogOut, Heart } from 'lucide-react';
import { CartContext } from '../App';
import { Button } from './ui/button';
import SearchBar from './SearchBar';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from './ui/dropdown-menu';

const Navbar = () => {
  const { cartCount, user, logout } = useContext(CartContext);
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled ? 'bg-white shadow-md' : 'bg-white/95 backdrop-blur-sm'
      }`}
    >
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="text-2xl font-bold" style={{ fontFamily: 'Playfair Display' }}>
              <span className="text-[#d4af37]">Kayee</span>
              <span className="text-[#1a1a1a]">01</span>
            </div>
          </Link>

          {/* Search Bar (Desktop) */}
          <div className="hidden md:flex flex-1 max-w-md mx-8">
            <SearchBar />
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link to="/" className="text-gray-700 hover:text-[#d4af37] font-medium">
              Home
            </Link>
            <Link to="/shop" className="text-gray-700 hover:text-[#d4af37] font-medium">
              Shop All
            </Link>
            <Link to="/shop/fashion" className="text-gray-700 hover:text-[#d4af37] font-medium">
              Fashion
            </Link>
            <Link to="/shop/jewelry" className="text-gray-700 hover:text-[#d4af37] font-medium">
              Jewelry
            </Link>
            <Link to="/track-order" className="text-gray-700 hover:text-[#d4af37] font-medium">
              Track Order
            </Link>
          </div>

          {/* Right Side Actions */}
          <div className="flex items-center space-x-4">
            {/* User Menu */}
            {user ? (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="icon" className="relative">
                    <User className="h-5 w-5" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuLabel>{user.name}</DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem onClick={() => navigate('/my-orders')}>
                    My Orders
                  </DropdownMenuItem>
                  {user.role === 'admin' && (
                    <DropdownMenuItem onClick={() => navigate('/admin')}>
                      Admin Dashboard
                    </DropdownMenuItem>
                  )}
                  <DropdownMenuSeparator />
                  <DropdownMenuItem onClick={logout}>
                    <LogOut className="h-4 w-4 mr-2" />
                    Logout
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            ) : (
              <Button
                variant="ghost"
                size="icon"
                onClick={() => navigate('/admin/login')}
                data-testid="login-button"
              >
                <User className="h-5 w-5" />
              </Button>
            )}

            {/* Wishlist */}
            <Link to="/wishlist" className="relative" data-testid="wishlist-button">
              <Button variant="ghost" size="icon" title="Wishlist">
                <Heart className="h-5 w-5" />
              </Button>
            </Link>

            {/* Cart */}
            <Link to="/cart" className="relative" data-testid="cart-button">
              <Button variant="ghost" size="icon">
                <ShoppingCart className="h-5 w-5" />
                {cartCount > 0 && (
                  <span className="absolute -top-1 -right-1 bg-[#d4af37] text-white text-xs rounded-full w-5 h-5 flex items-center justify-center font-semibold">
                    {cartCount}
                  </span>
                )}
              </Button>
            </Link>

            {/* Mobile Menu Toggle */}
            <button
              className="md:hidden"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              data-testid="mobile-menu-toggle"
            >
              {isMobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden pb-4 space-y-3">
            {/* Mobile Search Bar */}
            <div className="px-2 py-2">
              <SearchBar />
            </div>
            
            <Link
              to="/"
              className="block py-2 text-gray-700 hover:text-[#d4af37]"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Home
            </Link>
            <Link
              to="/shop"
              className="block py-2 text-gray-700 hover:text-[#d4af37]"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Shop All
            </Link>
            <Link
              to="/shop/fashion"
              className="block py-2 text-gray-700 hover:text-[#d4af37]"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Fashion
            </Link>
            <Link
              to="/shop/jewelry"
              className="block py-2 text-gray-700 hover:text-[#d4af37]"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Jewelry
            </Link>
            <Link
              to="/track-order"
              className="block py-2 text-gray-700 hover:text-[#d4af37]"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Track Order
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;