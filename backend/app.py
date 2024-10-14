from flask import Flask, jsonify, request, render_template, send_from_directory
import os

# Initialize Flask app, setting correct folders for templates and static files
app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend", static_url_path="/static")

# Route to serve index.html (the main page)
@app.route('/')
def home():
    return render_template('index.html')

# Serve static files (CSS and JS) from the frontend folder
@app.route('/static/<path:path>')
def serve_static_files(path):
    return send_from_directory('../frontend', path)

# Example API for product price (handle this based on your requirements)
@app.route('/api/product-price', methods=['POST'])
def product_price():
    data = request.json
    product_id = data.get('product_id')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not product_id or not latitude or not longitude:
        return jsonify({"error": "Product ID and location are required"}), 400

    # Dummy response (replace this with actual product price logic)
    response = {
        "price_data": [
            {"currency": "USD", "formatted_current_price": "$19.99", "min_price": 19.99, "max_price": 19.99}
        ],
        "store_lat": 37.773972,  # Example latitude (San Francisco)
        "store_lng": -122.431297  # Example longitude
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
