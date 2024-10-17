import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def create_chromedriver(headless=False):
    try:
        # Automatically install the correct version of ChromeDriver
        path = chromedriver_autoinstaller.install()  # This will install the matching ChromeDriver version
        
        if path:
            print(f"ChromeDriver installed at: {path}")
        else:
            print("ChromeDriver installation failed!")

        chrome_options = Options()
        
        # Optional: run Chrome in headless mode (without GUI)
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Create the ChromeDriver instance
        driver = webdriver.Chrome(options=chrome_options)
        
        return driver

    except Exception as e:
        print(f"Error setting up ChromeDriver: {e}")
        raise

# Example usage
'''
if __name__ == "__main__":
    driver = create_chromedriver()
    driver.get('https://www.walmart.com/')
    print("Opened Walmart homepage.")
    driver.quit()
'''