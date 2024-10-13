import requests
import pandas as pd

class TargetService:
    def __init__(self):
        self.base_url = "https://www.target.com"
        self.redsky_base_url = "https://redsky.target.com/v3"

    def get_store_id(self):
        """
        Creates a session and retrieves the nearest Target store ID based on the user's location.
        :return: Store ID
        """
        # Create a session to get cookies
        session = requests.session()
        session.get(self.base_url)

        # Extract visitorId (API key) and location from cookies
        api_key = session.cookies['visitorId']
        location = session.cookies['GuestLocation'].split('|')[0]

        # Get the nearest store ID based on location
        store_response = requests.get(f'{self.redsky_base_url}/stores/nearby/{location}?key={api_key}&limit=1&within=100&unit=mile')
        store_data = store_response.json()

        # Extract store ID from response
        store_id = store_data['locations'][0]['location_id']
        return store_id, api_key

    def get_product_price(self, product_id):
        """
        Fetches the real-time price of a product from the nearest Target store.
        :param product_id: The Target product ID (TCIN).
        :return: Product pricing information (price, availability, etc.).
        """
        store_id, api_key = self.get_store_id()

        # Build the product URL for querying price details
        product_url = f'https://redsky.target.com/web/pdp_location/v1/tcin/{product_id}'
        payload = {
            'pricing_store_id': store_id,
            'key': api_key
        }

        # Make the request to get product pricing info
        response = requests.get(product_url, params=payload)
        product_data = response.json()

        if 'price' in product_data:
            # Convert price data to a DataFrame for easier manipulation (optional)
            df = pd.DataFrame(product_data['price'], index=[0])
            return df
        else:
            raise Exception(f"Error fetching product price for ID {product_id}")

