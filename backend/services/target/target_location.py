import requests
from geopy.distance import geodesic

class OpenStreetMapService:
    def __init__(self):
        self.nominatim_base_url = "https://nominatim.openstreetmap.org/search"
    
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

    def find_nearby_stores(self, lat, lon, store_name="Target", radius=50):
        """
        Find nearby stores based on user's coordinates using OpenStreetMap Nominatim API.
        :param lat: Latitude of the user's location.
        :param lon: Longitude of the user's location.
        :param store_name: Name of the store to search for (e.g., Target).
        :param radius: Search radius in kilometers.
        :return: List of nearby stores with their names and locations.
        """
        params = {
            'q': store_name,
            'format': 'json',
            'lat': lat,
            'lon': lon,
            'radius': radius * 1000,  # Convert km to meters for the radius
            'addressdetails': 1,  # Return detailed address information
        }
        response = requests.get(self.nominatim_base_url, params=params)
        data = response.json()

        if response.status_code == 200 and len(data) > 0:
            return data  # List of nearby stores
        else:
            raise Exception(f"Error fetching nearby stores from OpenStreetMap: {response.text}")

    def find_nearest_target_store(self, user_location):
        """
        Find the nearest Target store based on the user's location.
        :param user_location: Address or postal code of the user.
        :return: Nearest Target store's address and distance from the user.
        """
        # Step 1: Geocode the user's address to get coordinates
        user_coords = self.geocode(user_location)
        
        # Step 2: Find nearby Target stores based on the user's coordinates
        nearby_stores = self.find_nearby_stores(user_coords[0], user_coords[1], store_name="Target")
        
        # Step 3: Identify the nearest store by calculating the distance
        nearest_store = None
        shortest_distance = float('inf')

        for store in nearby_stores:
            store_coords = (float(store['lat']), float(store['lon']))
            distance = geodesic(user_coords, store_coords).km  # Calculate straight-line distance

            if distance < shortest_distance:
                shortest_distance = distance
                nearest_store = store

        # Step 4: Return the nearest store's address
        if nearest_store:
            store_address = nearest_store['display_name']
            return store_address, shortest_distance
        else:
            return None, None


# Example usage
if __name__ == "__main__":
    osm_service = OpenStreetMapService()
    
    # User's location (e.g., input address or postal code)
    user_address = "33613"  # Example postal code
    
    # Find the nearest Target store
    nearest_store_address, distance = osm_service.find_nearest_target_store(user_address)
    
    if nearest_store_address:
        print(f"Nearest Target Store: {nearest_store_address}")
        print(f"Distance: {distance:.2f} km")
    else:
        print("No nearby Target store found.")
