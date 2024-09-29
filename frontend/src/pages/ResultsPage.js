import React from 'react';
import { useLocation } from 'react-router-dom';
import StoreList from '../components/StoreList';

function ResultsPage() {
    const { state } = useLocation();
    const { data } = state || {};

    return (
        <div>
            <h1>Results</h1>
            {data ? (
                <StoreList stores={data.stores} />
            ) : (
                <p>No results available.</p>
            )}
        </div>
    );
}

export default ResultsPage;
