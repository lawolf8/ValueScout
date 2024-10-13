from flask import Flask, render_template, request, jsonify
from services.google_maps import GoogleMapsService
from services.gasbuddy import GasBuddyService

app = Flask(__name__)

google_maps_service = GoogleMapsService()
gasbuddy_service = GasBuddyService()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate_route():
    location = request.form.get('location')
    items = request.form.get('items')

    # Dummy data for now
    stores = [
        {"name": "Store A", "address": "123 Main St", "distance": 5, "totalPrice": 20.5},
        {"name": "Store B", "address": "456 Market St", "distance": 8, "totalPrice": 19.0}
    ]

    return render_template('results.html', stores=stores)

if __name__ == '__main__':
    app.run(debug=True)
