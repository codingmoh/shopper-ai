import { useEffect } from 'react';
import './CheckoutModal.css';

function CheckoutModal({ onClose, autoCloseMs = 2600 }) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose?.();
    }, autoCloseMs);
    return () => clearTimeout(timer);
  }, [autoCloseMs, onClose]);

  return (
    <div className="checkout-overlay" onClick={onClose}>
      <div className="checkout-content" onClick={(e) => e.stopPropagation()}>
        <div className="glow" />
        <div className="sparkles" aria-hidden="true" />
        <div className="check-badge">✅</div>
        <h3 className="title">We’ve got it!</h3>
        <p className="subtitle">The products will be ordered for you.</p>
      </div>
    </div>
  );
}

export default CheckoutModal;




