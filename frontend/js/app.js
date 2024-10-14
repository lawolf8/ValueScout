document.getElementById('product-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const productId = document.getElementById('product-id').value;
    const zipCode = document.getElementById('zip-code').value;

    // Fetch product price and store location from the API
    fetch('/api/product-price', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_id: productId, zip_code: zipCode })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('price-info').innerHTML = `<p>Error: ${data.error}</p>`;
        } else {
            const priceData = data.price_data;
            document.getElementById('price-info').innerHTML = `
                <h3>Price Information:</h3>
                <p>Currency: ${priceData[0].currency}</p>
                <p>Price: ${priceData[0].formatted_current_price}</p>
                <p>Min Price: ${priceData[0].min_price}</p>
                <p>Max Price: ${priceData[0].max_price}</p>
            `;

            const storeLat = data.store_lat;
            const storeLng = data.store_lng;

            const map = L.map('map').setView([storeLat, storeLng], 13);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; OpenStreetMap contributors'
            }).addTo(map);

            L.marker([storeLat, storeLng]).addTo(map)
                .bindPopup('Nearest Target Store')
                .openPopup();
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
