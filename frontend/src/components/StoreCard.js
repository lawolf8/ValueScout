import React from 'react';

function StoreCard({ store }) {
    return (
        <div className="store-card">
            <h2>{store.name}</h2>
            <p>Address: {store.address}</p>
            <p>Distance: {store.distance} km</p>
            <p>Total Price: ${store.totalPrice}</p>
        </div>
    );
}

export default StoreCard;
