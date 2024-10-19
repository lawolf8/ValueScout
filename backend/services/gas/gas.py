import requests

class Gas:
    def __init__(self):
        self.api_url = "https://www.gasbuddy.com/graphql"
        self.headers = {
            "Content-Type": "application/json"
        }

    def get_gas_prices(self, zip_code, fuel_type=1):
        """
        Query GasBuddy GraphQL API to get gas prices by zip code.
        
        :param zip_code: The zip code to search for gas prices.
        :param fuel_type: Fuel type (1 = regular gasoline). Modify for other types if needed.
        :return: A dictionary containing gas price data (today's price and the lowest price).
        """
        payload = {
            "operationName": "LocationBySearchTerm",
            "variables": {
                "fuel": fuel_type,
                "maxAge": 0,
                "search": zip_code
            },
            "query": """
                query LocationBySearchTerm($search: String) {
                    locationBySearchTerm(search: $search) {
                        trends {
                            areaName
                            country
                            today
                            todayLow
                        }
                    }
                }
            """
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)
        data = response.json()

        if response.status_code == 200 and 'data' in data:
            trends = data['data']['locationBySearchTerm']['trends'][0]
            gas_prices = {
                "area": trends['areaName'],
                "country": trends['country'],
                "today_price": float(trends['today']),
                "lowest_price": float(trends['todayLow'])
            }
            return gas_prices
        else:
            raise Exception(f"Error fetching data from GasBuddy API: {response.text}")
