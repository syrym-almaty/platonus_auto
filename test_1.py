import time
import random
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Define the path to the Edge WebDriver
driver_path = r"C:\Users\syrym\Downloads\Platonus_Automatization\msedgedriver.exe"

# Set up Edge options
edge_options = Options()

# Randomized User-Agent to avoid detection
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Safari/537.36 Edg/110.0.1587.49",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
]
random_user_agent = random.choice(user_agents)
edge_options.add_argument(f'user-agent={random_user_agent}')

# Avoid detection by disabling certain automation flags
edge_options.add_experimental_option('useAutomationExtension', False)
edge_options.add_experimental_option('excludeSwitches', ['enable-automation'])
edge_options.add_argument("--disable-blink-features=AutomationControlled")

# Other useful options to simulate a human-like behavior
edge_options.add_argument("--disable-extensions")
edge_options.add_argument("--profile-directory=Default")
edge_options.add_argument("--disable-plugins-discovery")
edge_options.add_argument("--incognito")  # Open in incognito mode to avoid cache issues
edge_options.add_argument("--start-maximized")
edge_options.add_argument("--disable-popup-blocking")

# Create a Service object with the path to the Edge WebDriver
service = EdgeService(driver_path)

# Initialize the Edge WebDriver
driver = webdriver.Edge(service=service, options=edge_options)

# Additional steps to bypass bot detection
# Set navigator.webdriver to False using JavaScript
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

try:
    # Open a website (for example, Google)
    driver.get("https://www.google.com")
    
    # Random wait to mimic human-like behavior
    time.sleep(random.uniform(3, 6))
    
    # Example interaction: Search for a term in Google to look more human-like
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Selenium automation tips")
    time.sleep(random.uniform(1, 3))  # Pause before hitting enter
    search_box.send_keys(Keys.RETURN)
    
    # Random browsing actions
    time.sleep(random.uniform(5, 10))
    
    # Scroll down to simulate human activity
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(2, 4))

    # Perform more actions if needed
    
finally:
    # Close the browser after waiting for a few seconds
    time.sleep(random.uniform(3, 5))
    driver.quit()