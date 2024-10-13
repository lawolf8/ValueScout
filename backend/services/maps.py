import requests

#https://wiki.openstreetmap.org/wiki/About_OpenStreetMap

class OpenStreetMapService:
    def __init__(self):
        self.nominatim_base_url = "https://nominatim.openstreetmap.org/search"
        self.osrm_base_url = "http://router.project-osrm.org/route/v1"

    def geocode(self, location):
        """
        Geocode the location (convert address to coordinates) using OpenStreetMap Nominatim API.
        :param location: The address or place name to geocode.
        :return: Latitude and Longitude of the location.
        """
        params = {
            'q': location,
            'format': 'json'
        }

        response = requests.get(self.nominatim_base_url, params=params)
        data = response.json()

        if response.status_code == 200 and len(data) > 0:
            return float(data[0]['lat']), float(data[0]['lon'])
        else:
            raise Exception(f"Error fetching geocode data from OpenStreetMap: {response.text}")

    def get_route(self, origin_coords, destination_coords):
        """
        Get the driving route between two locations using OSRM (Open Source Routing Machine).
        :param origin_coords: Tuple of (latitude, longitude) for the origin.
        :param destination_coords: Tuple of (latitude, longitude) for the destination.
        :return: Distance in kilometers and travel duration in minutes.
        """
        origin = f"{origin_coords[1]},{origin_coords[0]}"
        destination = f"{destination_coords[1]},{destination_coords[0]}"
        
        url = f"{self.osrm_base_url}/driving/{origin};{destination}"
        params = {
            'overview': 'false',  # Don't include detailed route geometry
            'alternatives': 'false',  # Don't provide alternative routes
            'steps': 'false'  # Don't include detailed steps
        }

        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200 and 'routes' in data:
            route = data['routes'][0]
            distance = route['distance'] / 1000  # distance in km
            duration = route['duration'] / 60  # duration in minutes
            return distance, duration
        else:
            raise Exception(f"Error fetching route data from OSRM: {response.text}")


