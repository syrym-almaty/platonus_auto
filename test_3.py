import time
import random
import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

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
edge_options.add_argument("--start-maximized")
edge_options.add_argument("--disable-popup-blocking")

# Set the user data directory to save cookies, cache, and session data
user_data_dir = r"C:\Users\syrym\Downloads\Platonus_Automatization\User_Data"
edge_options.add_argument(f"--user-data-dir={user_data_dir}")

# Create a Service object with the path to the Edge WebDriver
service = EdgeService(driver_path)

# Initialize the Edge WebDriver
driver = webdriver.Edge(service=service, options=edge_options)

# Additional steps to bypass bot detection
# Set navigator.webdriver to False using JavaScript
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

try:
    # Open Platonus website
    driver.get("https://platonus.iitu.edu.kz/")
    
    # Random wait to mimic human-like behavior
    time.sleep(random.uniform(3, 6))
    
    # Click the login button if fields are already populated
    try:
        login_button = driver.find_element(By.ID, "Submit1")
        login_button.click()
    except NoSuchElementException:
        # If login button is not found, assume already logged in
        print("Login button not found, assuming already logged in.")
    
    # Random browsing actions after login
    time.sleep(random.uniform(5, 10))
    
finally:
    # Close the browser after waiting for a few seconds
    time.sleep(random.uniform(3, 5))
    driver.quit()

# Create a .gitignore entry for the credentials file
gitignore_path = r"C:\Users\syrym\Downloads\Platonus_Automatization\.gitignore"
with open(gitignore_path, 'a') as gitignore:
    if "credentials.txt" not in open(gitignore_path).read():
        gitignore.write("\ncredentials.txt")