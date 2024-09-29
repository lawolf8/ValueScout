import React from 'react';
import StoreCard from './StoreCard';

function StoreList({ stores }) {
    return (
        <div>
            {stores.map((store, index) => (
                <StoreCard key={index} store={store} />
            ))}
        </div>
    );
}

export default StoreList;
