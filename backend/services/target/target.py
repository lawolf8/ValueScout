'''
Target Web Scrapping - Grabbing Prices and Availability of list
'''

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from chromedriver import create_chromedriver

class TargetPriceBot:
    def __init__(self):
        self.driver = create_chromedriver()
        self.items_prices = {}  # To store item names and their prices

    def search_item(self, item_name, quantity):
        """Search for an item on Target's website and handle quantity."""
        try:
            # Step 1: Open Target's homepage
            self.driver.get('https://www.target.com/')
            time.sleep(3)  # Wait for the page to load

            # Step 2: Find the search bar using the ID or placeholder attribute and type the item
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'search'))
            )
            search_input.send_keys(item_name)
            time.sleep(2)  # Give time for the input to be processed

            # Step 3: Submit the search by clicking the search button
            search_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="@web/Search/SearchButton"]'))
            )
            search_button.click()
            time.sleep(3)  # Wait for search results to load

            # Step 4: Collect the price and handle quantity for the first item in the results
            self.collect_price(item_name, quantity)

        except Exception as e:
            print(f"Error during the search process for {item_name}: {e}")

    def collect_price(self, item_name, quantity):
        """Collect price for the first item in the search results, handle quantity, and check availability."""
        try:
            # Locate the first item in the search results
            price_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-test="current-price"] span'))
            )
            price_text = price_element.text.strip()

            # Check for price range (e.g., "$1.39 - $4.99")
            if ' - ' in price_text:
                print(f"Price range detected for {item_name}: {price_text}")
                # Select the 1-count option, optimize the quantity, and retrieve the actual price
                final_price = self.select_count_and_get_price(quantity)
                self.items_prices[item_name] = final_price
            else:
                # If there's a single price, multiply it by the quantity and store it
                price = float(price_text.replace('$', ''))
                total_price = price * quantity
                self.items_prices[item_name] = total_price

            # Check availability (if "Not available at" is found, mark the item as unavailable)
            try:
                self.driver.find_element(By.XPATH, "//div[contains(text(), 'Not available')]")
                self.items_prices[item_name] = 'N/A'
                print(f"Item {item_name} is not available.")
            except NoSuchElementException:
                print(f"Price for {item_name} with quantity {quantity}: {self.items_prices[item_name]}")

        except Exception as e:
            self.items_prices[item_name] = 'N/A'
            print(f"Error collecting price for {item_name}: {e}")

    def select_count_and_get_price(self, required_quantity):
        """Handles selecting the optimal count to meet the required quantity and fetching the price."""
        try:
            # Step 1: Click 'Add to cart'
            add_to_cart_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'addToCartButtonOrTextIdFor12935253'))  # Adjust this ID as needed
            )
            add_to_cart_button.click()
            time.sleep(2)

            # Step 2: Get available counts (e.g., 1-count, 4-count) and select the best option for the required quantity
            count_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.sc-1aa3ca61-2.hhgEZq li a'))
            )

            # Convert available counts into integer values
            available_counts = []
            for count_element in count_elements:
                count_value = int(count_element.get_attribute('value'))
                available_counts.append((count_value, count_element))

            # Step 3: Select optimal count combination (largest possible count first)
            total_items_selected = 0
            total_price = 0.0

            for count_value, count_element in sorted(available_counts, reverse=True):
                if total_items_selected >= required_quantity:
                    break  # We've selected enough items
                if count_value > 0:
                    times_to_add = (required_quantity - total_items_selected) // count_value
                    if times_to_add > 0:
                        # Select this count
                        for _ in range(times_to_add):
                            count_element.click()
                            total_items_selected += count_value
                            # Get price after adding count
                            price_element = WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-test="product-price"]'))
                            )
                            price_text = price_element.text.strip()
                            price_per_unit = float(price_text.replace('$', ''))
                            total_price += price_per_unit * count_value
                            print(f"Added {count_value} items at price: {price_per_unit}")

            # Handle any remaining items that couldn't be fulfilled with the available counts
            if total_items_selected < required_quantity:
                smallest_count_value, smallest_count_element = available_counts[-1]  # Pick the smallest count
                while total_items_selected < required_quantity:
                    smallest_count_element.click()
                    total_items_selected += smallest_count_value
                    price_element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-test="product-price"]'))
                    )
                    price_text = price_element.text.strip()
                    price_per_unit = float(price_text.replace('$', ''))
                    total_price += price_per_unit * smallest_count_value
                    print(f"Added {smallest_count_value} more items at price: {price_per_unit}")

            return total_price

        except Exception as e:
            print(f"Error adding item to cart or selecting count: {e}")
            return 0.0

    def calculate_total_price(self, tax_rate=0.07):
        """Calculate total price with tax for available items."""
        total_price = 0
        for item, price in self.items_prices.items():
            if price != 'N/A':
                total_price += price

        # Add tax to the total price
        total_with_tax = total_price * (1 + tax_rate)
        return round(total_with_tax, 2)

    def run(self, items, quantities, tax_rate=0.07):
        """Run the bot for a list of items and their quantities, and return the total price with tax."""
        for item, quantity in zip(items, quantities):
            self.search_item(item, quantity)

        # Calculate total price with tax
        total_price_with_tax = self.calculate_total_price(tax_rate)

        print("Items and Prices: ", self.items_prices)
        print(f"Total Price (with tax): ${total_price_with_tax}")

        # Quit the driver
        self.driver.quit()

        # Return the hashmap and total price
        return self.items_prices, total_price_with_tax

# Example usage

if __name__ == "__main__":
    items_to_search = ['Fairlife Lactose-Free Skim Milk - 52 fl oz', "Annie's Shells & White Cheddar Mac & Cheese"]
    quantities = [2, 7]  # Corresponding quantities for each item
    bot = TargetPriceBot()
    items_prices, total_price_with_tax = bot.run(items_to_search, quantities)

