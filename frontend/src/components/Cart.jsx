import { useState } from 'react';
import './Cart.css';

function Cart({ cart, onClose, onRemove, totalPrice, onCheckout }) {
  const [size, setSize] = useState('Medium');
  return (
    <div className="cart-overlay" onClick={onClose}>
      <div className="cart-content" onClick={(e) => e.stopPropagation()}>
        <div className="cart-header">
          <h2>🛒 Your Cart</h2>
          <button className="close-button" onClick={onClose}>✕</button>
        </div>
        
        <div className="cart-items">
          {cart.length === 0 ? (
            <div className="empty-cart">
              <p>Your cart is empty! 😢</p>
              <p>Start swiping to add items!</p>
            </div>
          ) : (
            cart.map((item, index) => (
              <div key={index} className="cart-item">
                <img src={item.image} alt={item.name} />
                <div className="cart-item-info">
                  <h4>{item.name}</h4>
                  <p className="cart-item-price">${item.price}</p>
                </div>
                <button 
                  className="remove-button"
                  onClick={() => onRemove(index)}
                >
                  🗑️
                </button>
              </div>
            ))
          )}
        </div>

        {cart.length > 0 && (
          <div className="cart-footer">
            <div className="size-select">
              <label htmlFor="size">Size: </label>
              <select id="size" value={size} onChange={(e) => setSize(e.target.value)}>
                <option value="XS">XS</option>
                <option value="S">S</option>
                <option value="Medium">Medium</option>
                <option value="L">L</option>
                <option value="XL">XL</option>
                <option value="XXL">XXL</option>
              </select>
            </div>
            <div className="cart-total">
              <span>Total:</span>
              <span className="total-price">${totalPrice}</span>
            </div>
            <button className="checkout-button" onClick={() => onCheckout?.(size)}>
              ✨ Checkout ✨
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default Cart;

