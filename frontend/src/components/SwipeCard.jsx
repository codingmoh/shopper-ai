import { useState } from 'react';
import './SwipeCard.css';

function SwipeCard({ item, onSwipe, swipeDirection }) {
    const [dragStart, setDragStart] = useState(null);
    const [dragOffset, setDragOffset] = useState(0);
    const [selectedSide, setSelectedSide] = useState(null);

    const handleMouseDown = (e) => {
        setDragStart(e.clientX);
    };

    const handleMouseMove = (e) => {
        if (dragStart !== null) {
            const offset = e.clientX - dragStart;
            setDragOffset(offset);
        }
    };

    const handleMouseUp = (e) => {
        if (dragStart !== null) {
            const offset = e.clientX - dragStart;

            // Determine swipe threshold
            if (Math.abs(offset) > 100) {
                if (offset < 0) {
                    handleSelect('left', item.left);
                } else {
                    handleSelect('right', item.right);
                }
            }

            setDragStart(null);
            setDragOffset(0);
        }
    };

    const handleSelect = (side, selectedItem) => {
        setSelectedSide(side);
        setTimeout(() => {
            onSwipe(side, selectedItem);
            setSelectedSide(null);
        }, 200);
    };

    const handleAddToCart = (side, selectedItem) => {
        setSelectedSide(side);
        setTimeout(() => {
            onSwipe('cart', selectedItem);
            setSelectedSide(null);
        }, 200);
    };

    return (
        <div
            className={`swipe-card ${swipeDirection ? `swipe-${swipeDirection}` : ''} ${selectedSide ? `selected-${selectedSide}` : ''}`}
            onMouseDown={handleMouseDown}
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onMouseLeave={handleMouseUp}
            style={{
                transform: `translateX(${dragOffset}px) rotate(${dragOffset * 0.05}deg)`
            }}
        >
            <div className="card-content">
                {/* Left Item */}
                <div
                    className={`item-card left-card ${selectedSide === 'right' ? 'dimmed' : ''}`}
                    onClick={() => handleSelect('left', item.left)}
                >
                    <div className="item-image">
                        <img src={item.left.image} alt={item.left.name} />
                        <div className="item-overlay">
                            <span className="tap-indicator">👈 TAP</span>
                        </div>
                    </div>
                    <div className="item-info">
                        <h3>{item.left.name}</h3>
                        <p className="price">${item.left.price}</p>
                        <button
                            className="action-button add-to-cart"
                            onClick={(e) => {
                                e.stopPropagation();
                                handleAddToCart('left', item.left);
                            }}
                        >
                            🛒 Add to Cart
                        </button>
                    </div>
                </div>

                {/* VS Divider */}
                <div className="vs-divider">
                    <span>VS</span>
                </div>

                {/* Right Item */}
                <div
                    className={`item-card right-card ${selectedSide === 'left' ? 'dimmed' : ''}`}
                    onClick={() => handleSelect('right', item.right)}
                >
                    <div className="item-image">
                        <img src={item.right.image} alt={item.right.name} />
                        <div className="item-overlay">
                            <span className="tap-indicator">TAP 👉</span>
                        </div>
                    </div>
                    <div className="item-info">
                        <h3>{item.right.name}</h3>
                        <p className="price">${item.right.price}</p>
                        <button
                            className="action-button add-to-cart"
                            onClick={(e) => {
                                e.stopPropagation();
                                handleAddToCart('right', item.right);
                            }}
                        >
                            🛒 Add to Cart
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default SwipeCard;



