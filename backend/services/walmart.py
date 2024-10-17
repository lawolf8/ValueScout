from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
from chromedriver import create_chromedriver

class WalmartAddressBot:
    def __init__(self):
        self.driver = create_chromedriver()

    def handle_bot_detector(self):
        """Checks and handles bot detection 'Press & Hold' button."""
        try:
            # Check if the "Press & Hold" button exists
            press_and_hold = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, 'EZohBERupUAbpVL'))
            )
            if press_and_hold:
                print("Bot detector found: Pressing and holding for 10 seconds...")

                # Simulate holding the button for 10 seconds
                actions = ActionChains(self.driver)
                actions.click_and_hold(press_and_hold).perform()
                time.sleep(10)  # Hold for 10 seconds
                actions.release().perform()

                print("Bot detector passed.")
        except Exception as e:
            print("No bot detector found or error handling bot detector:", e)

    def add_address(self, address_info):
        """Fills in the address details in Walmart's location form."""
        try:
            # Step 1: Open Walmart and check for bot detection
            self.driver.get('https://www.walmart.com/')
            time.sleep(3)  # Wait for the page to load

            # Handle bot detection if necessary
            self.handle_bot_detector()

            # Step 2: Proceed with clicking the location button
            location_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.lh-title.fw4'))
            )
            print("Clicking location button...")
            location_button.click()
            time.sleep(2)

            # Step 3: Click "Add address"
            add_address_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Add address")]'))
            )
            print("Clicking 'Add address' button...")
            add_address_button.click()
            time.sleep(2)

            # Step 4: Fill out the address details
            print("Entering first name...")
            first_name_input = self.driver.find_element(By.ID, 'react-aria4283164293-:r2r:')
            first_name_input.send_keys("a")  # Enter unique first name

            print("Entering last name...")
            last_name_input = self.driver.find_element(By.ID, 'react-aria4283164293-:r2t:')
            last_name_input.send_keys("a")  # Enter unique last name

            print("Entering street address...")
            street_address_input = self.driver.find_element(By.ID, 'addressLineOne')
            street_address_input.send_keys(address_info['address'])  # Enter street address

            print("Entering city...")
            city_input = self.driver.find_element(By.ID, 'react-aria4283164293-:r33:')
            city_input.send_keys(address_info['city'])  # Enter city

            print("Selecting state...")
            state_dropdown = Select(self.driver.find_element(By.ID, 'react-aria4283164293-:r35:'))
            state_dropdown.select_by_value(address_info['state'])  # Select state

            print("Entering zip code...")
            zip_input = self.driver.find_element(By.ID, 'react-aria4283164293-:r37:')
            zip_input.send_keys(address_info['zip'])  # Enter zip code

            print("Entering phone number...")
            phone_input = self.driver.find_element(By.ID, 'react-aria4283164293-:r39:')
            phone_input.send_keys("1111111111")  # Enter phone number

            # Pause for 20 seconds to observe the process
            print("Pausing for 20 seconds to observe the process...")
            time.sleep(20)

        except Exception as e:
            print(f"Error during the address entry process: {e}")
        finally:
            # Quit the driver after the process
            self.driver.quit()


# Example usage
if __name__ == "__main__":
    # Sample address details (can be modified dynamically)
    address_info = {
        'address': '123 Main St',
        'city': 'Tampa',
        'state': 'FL',
        'zip': '33617'
    }

    bot = WalmartAddressBot()
    bot.add_address(address_info)
