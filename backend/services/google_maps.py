import os
import requests

class GoogleMapsService:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        self.base_url = "https://maps.googleapis.com/maps/api"

    def get_distance(self, origin, destination):
        """
        Calculate the distance between two locations using Google Maps Distance Matrix API.
        :param origin: Starting point (e.g., "123 Main St, City, State")
        :param destination: Ending point (e.g., "456 Market St, City, State")
        :return: Distance in kilometers and estimated travel time in minutes.
        """
        url = f"{self.base_url}/distancematrix/json"
        params = {
            "origins": origin,
            "destinations": destination,
            "key": self.api_key,
            "units": "metric"
        }

        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200 and data['status'] == 'OK':
            distance = data['rows'][0]['elements'][0]['distance']['value'] / 1000  # distance in km
            duration = data['rows'][0]['elements'][0]['duration']['value'] / 60  # duration in minutes
            return distance, duration
        else:
            raise Exception(f"Error fetching data from Google Maps API: {data['error_message']}")

