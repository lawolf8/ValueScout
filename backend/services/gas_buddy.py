import os
import requests

class GasBuddyService:
    def __init__(self):
        self.api_key = os.getenv('GASBUDDY_API_KEY')
        self.base_url = "https://api.gasbuddy.com/v2"

    def get_gas_prices(self, latitude, longitude, radius=10):
        """
        Fetch gas prices near a given location.
        :param latitude: Latitude of the location
        :param longitude: Longitude of the location
        :param radius: Search radius in miles (default is 10)
        :return: A list of nearby gas stations with their prices
        """
        url = f"{self.base_url}/stations"
        params = {
            "lat": latitude,
            "lng": longitude,
            "distance": radius,
            "apikey": self.api_key
        }

        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200:
            stations = []
            for station in data.get('stations', []):
                stations.append({
                    "name": station['name'],
                    "address": station['address'],
                    "price": station['prices'][0]['price'],  # Assuming 'prices' has the gas prices list
                    "distance": station['distance']
                })
            return stations
        else:
            raise Exception(f"Error fetching data from GasBuddy API: {data['message']}")

