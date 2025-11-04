import { useState } from 'react'
import './App.css'
import SwipeCard from './components/SwipeCard'
import CheckoutModal from './components/CheckoutModal'
import Cart from './components/Cart'
import data from '../data.json'

// Build pairs from data.json entries (keys are image filenames)
const buildPairsFromData = (records) => {
  const entries = Object.entries(records);
  const items = [];
  for (let i = 0; i < entries.length; i += 2) {
    const [leftKey, leftVal] = entries[i];
    const rightEntry = entries[i + 1];
    if (!rightEntry) break;
    const [rightKey, rightVal] = rightEntry;
    items.push({
      id: i / 2 + 1,
      left: {
        name: leftVal.name,
        price: leftVal.price,
        image: `/img/${leftKey}`,
        url: leftVal.url,
      },
      right: {
        name: rightVal.name,
        price: rightVal.price,
        image: `/img/${rightKey}`,
        url: rightVal.url,
      },
    });
  }
  return items;
};

const clothingItems = buildPairsFromData(data);

function App() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [cart, setCart] = useState([]);
  const [showCart, setShowCart] = useState(false);
  const [swipeDirection, setSwipeDirection] = useState(null);
  const [showCheckoutModal, setShowCheckoutModal] = useState(false);

  const handleSwipe = (direction, selectedItem) => {
    setSwipeDirection(direction);
    
    // Only add to cart when explicitly adding to cart
    if (direction === 'cart' && selectedItem) {
      const itemToAdd = { ...selectedItem, addedAt: Date.now() };
      setCart([...cart, itemToAdd]);
    }

    // Move to next card after animation
    setTimeout(() => {
      setCurrentIndex((prev) => (prev + 1) % clothingItems.length);
      setSwipeDirection(null);
    }, 300);
  };

  const handleCheckout = async (size = 'Medium') => {
    const productUrls = cart.map((item) => item.url);
    if (productUrls.length === 0) return;
    try {
      await fetch('http://localhost:8000/api/buy/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_urls: productUrls, size }),
      });
    } catch (_) {
      // noop
    }
    // Show confirmation modal in all cases to keep flow stylish
    setShowCart(false);
    setShowCheckoutModal(true);
    setTimeout(() => setShowCheckoutModal(false), 2600);
  };

  const removeFromCart = (index) => {
    setCart(cart.filter((_, i) => i !== index));
  };

  const getTotalPrice = () => {
    return cart.reduce((sum, item) => sum + item.price, 0).toFixed(2);
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <h1 className="logo">✨ FitSwipe ✨</h1>
        <button 
          className="cart-button"
          onClick={() => setShowCart(!showCart)}
        >
          🛒 Cart ({cart.length})
        </button>
      </header>

      {/* Main Content */}
      <div className="container">
        {currentIndex < clothingItems.length ? (
          <>
            <div className="swipe-hint">
              <p>👈 Swipe or tap to choose your style 👉</p>
            </div>
            <SwipeCard
              item={clothingItems[currentIndex]}
              onSwipe={handleSwipe}
              swipeDirection={swipeDirection}
            />
            <div className="progress">
              {currentIndex + 1} / {clothingItems.length}
            </div>
          </>
        ) : (
          <div className="completion">
            <h2>🎉 You've seen all items! 🎉</h2>
            <button 
              className="restart-button"
              onClick={() => setCurrentIndex(0)}
            >
              Start Over
            </button>
          </div>
        )}
      </div>

      {/* Cart Overlay */}
      {showCart && (
        <Cart
          cart={cart}
          onClose={() => setShowCart(false)}
          onRemove={removeFromCart}
          totalPrice={getTotalPrice()}
          onCheckout={handleCheckout}
        />
      )}

      {/* Checkout Confirmation */}
      {showCheckoutModal && (
        <CheckoutModal onClose={() => setShowCheckoutModal(false)} />
      )}
    </div>
  );
}

export default App;
