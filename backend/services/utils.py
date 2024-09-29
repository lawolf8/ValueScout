def format_address(address):
    """
    Format an address string for API requests.
    :param address: Raw address string
    :return: Formatted address string
    """
    return address.replace(" ", "+").replace(",", "")

def handle_api_error(response):
    """
    Handle API errors by raising an appropriate exception.
    :param response: The API response object
    :return: None
    """
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

