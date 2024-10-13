import time
import random
import json
import logging
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define the path to the Edge WebDriver
driver_path = r"C:\Users\syrym\Downloads\Platonus_Automatization\msedgedriver.exe"

# Set up Edge options
edge_options = Options()
# Removed headless mode so you can see the browser
# edge_options.add_argument('--headless')
edge_options.add_argument('--disable-gpu')
edge_options.add_argument('--no-sandbox')
edge_options.add_argument('--disable-dev-shm-usage')

# Randomized User-Agent to avoid detection
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    # Add more user agents as needed
]
random_user_agent = random.choice(user_agents)
edge_options.add_argument(f'user-agent={random_user_agent}')

# Avoid detection by disabling certain automation flags
edge_options.add_experimental_option('useAutomationExtension', False)
edge_options.add_experimental_option('excludeSwitches', ['enable-automation'])
edge_options.add_argument('--disable-blink-features=AutomationControlled')

# Other useful options to simulate human-like behavior
edge_options.add_argument('--disable-extensions')
edge_options.add_argument('--profile-directory=Default')
edge_options.add_argument('--disable-plugins-discovery')
edge_options.add_argument('--disable-popup-blocking')

# Set the user data directory to save cookies, cache, and session data
user_data_dir = r"C:\Users\syrym\Downloads\Platonus_Automatization\User_Data"
edge_options.add_argument(f'--user-data-dir={user_data_dir}')

def login_to_platonus(driver):
    # Open Platonus login page
    logging.info("Opening Platonus login page.")
    driver.get("https://platonus.iitu.edu.kz/")

    # Wait for the login page to load
    login_wait_time = random.uniform(2, 4)
    logging.info(f"Waiting for {login_wait_time:.2f} seconds for the login page to load.")
    time.sleep(login_wait_time)

    # Click the login button (assuming autofill is enabled)
    try:
        logging.info("Attempting to click the login button.")
        login_button = driver.find_element(By.ID, "Submit1")
        login_button.click()
    except NoSuchElementException:
        logging.warning("Login button not found, assuming already logged in.")

    # Wait for the page to load after login
    post_login_wait_time = random.uniform(3, 6)
    logging.info(f"Waiting for {post_login_wait_time:.2f} seconds for the page to load after login.")
    time.sleep(post_login_wait_time)

def extract_personal_data(driver):
    """
    Extracts data from the 'Personal data' tab.
    """
    personal_data = {}
    try:
        personal_data['Full name'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Full name')]/following-sibling::div//input").get_attribute('value')
        personal_data['Date of birth'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Date of birth')]/following-sibling::div//input").get_attribute('value')
        personal_data['IIN'] = driver.find_element(By.XPATH, "//label[contains(text(), 'IIN')]/following-sibling::div//input").get_attribute('value')
        personal_data['Registration address'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Registration address')]/following-sibling::div//input").get_attribute('value')
    except NoSuchElementException as e:
        logging.warning(f"Personal data field missing: {e}")
    return personal_data

def extract_documents_data(driver):
    """
    Extracts data from the 'Documents' tab.
    """
    documents_data = {}
    try:
        documents_data['Identity number'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Identity number')]/following-sibling::div//input").get_attribute('value')
        documents_data['Date of issuance'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Date of issuance')]/following-sibling::div//input").get_attribute('value')
        documents_data['Validity of identity document'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Validity of identity document')]/following-sibling::div//input").get_attribute('value')
    except NoSuchElementException as e:
        logging.warning(f"Documents data field missing: {e}")
    return documents_data

def extract_contact_details(driver):
    """
    Extracts data from the 'Contact details' tab.
    """
    contact_details = {}
    try:
        contact_details['Home phone'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Home phone')]/following-sibling::div//input").get_attribute('value')
        contact_details['Mobile phone'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Mobile phone')]/following-sibling::div//input").get_attribute('value')
        contact_details['Mail'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Mail')]/following-sibling::div//input").get_attribute('value')
    except NoSuchElementException as e:
        logging.warning(f"Contact detail field missing: {e}")
    return contact_details

def extract_specialty_information(driver):
    """
    Extracts data from the 'Information about the specialty' tab.
    """
    specialty_info = {}
    try:
        specialty_info['Enrolled date'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Enrolled date')]/following-sibling::div//input").get_attribute('value')
        specialty_info['Specialization'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Specialization') or contains(text(), 'Educational Program')]/following-sibling::div//input").get_attribute('value')
        specialty_info['Course'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Course')]/following-sibling::div//input").get_attribute('value')
        specialty_info['Group'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Group')]/following-sibling::div//input").get_attribute('value')
    except NoSuchElementException as e:
        logging.warning(f"Specialty information field missing: {e}")
    return specialty_info

def extract_education_information(driver):
    """
    Extracts data from the 'Information about education' tab.
    """
    education_info = {}
    try:
        education_info['Graduated institution'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Name(number) of institution')]/following-sibling::div//input").get_attribute('value')
        education_info['Certificate number'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Certificate number')]/following-sibling::div//input").get_attribute('value')
        education_info['Given date'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Given date')]/following-sibling::div//input").get_attribute('value')
        # Since GPA is very important, try to locate it
        try:
            education_info['GPA'] = driver.find_element(By.XPATH, "//span[contains(text(), 'GPA')]/following-sibling::span").text
        except NoSuchElementException:
            logging.warning("GPA field not found.")
            education_info['GPA'] = None
    except NoSuchElementException as e:
        logging.warning(f"Education information field missing: {e}")
    return education_info

def scrape_student_profile(driver, profile_link):
    """
    Opens the student profile and extracts information from tabs.
    """
    driver.get(profile_link)
    time.sleep(2)  # Wait for the page to load

    student_data = {}

    # Wait until the tabs are present
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'nav-tabs'))
        )
    except Exception as e:
        logging.error(f"Tabs not found: {e}")
        return student_data

    # Extract data from 'Personal data' tab (default open)
    logging.info("Extracting 'Personal data'...")
    student_data['Personal data'] = extract_personal_data(driver)

    # Navigate to 'Documents' tab
    try:
        documents_tab = driver.find_element(By.XPATH, "//button[@data-bs-target='#tab1']")
        documents_tab.click()
        time.sleep(1)
        logging.info("Extracting 'Documents'...")
        student_data['Documents'] = extract_documents_data(driver)
    except Exception as e:
        logging.error(f"Error accessing 'Documents' tab: {e}")

    # Navigate to 'Contact details' tab
    try:
        contact_tab = driver.find_element(By.XPATH, "//button[@data-bs-target='#tab2']")
        contact_tab.click()
        time.sleep(1)
        logging.info("Extracting 'Contact details'...")
        student_data['Contact details'] = extract_contact_details(driver)
    except Exception as e:
        logging.error(f"Error accessing 'Contact details' tab: {e}")

    # Navigate to 'Information about the specialty' tab
    try:
        specialty_tab = driver.find_element(By.XPATH, "//button[@data-bs-target='#tab3']")
        specialty_tab.click()
        time.sleep(1)
        logging.info("Extracting 'Information about the specialty'...")
        student_data['Information about the specialty'] = extract_specialty_information(driver)
    except Exception as e:
        logging.error(f"Error accessing 'Information about the specialty' tab: {e}")

    # Navigate to 'Information about education' tab
    try:
        education_tab = driver.find_element(By.XPATH, "//button[@data-bs-target='#tab4']")
        education_tab.click()
        time.sleep(1)
        logging.info("Extracting 'Information about education'...")
        student_data['Information about education'] = extract_education_information(driver)
    except Exception as e:
        logging.error(f"Error accessing 'Information about education' tab: {e}")

    return student_data

def main():
    # Load the links from the existing JSON file
    with open(r'C:\Users\syrym\Downloads\Platonus_Automatization\links.json', 'r', encoding='utf-8') as file:
        links_data = json.load(file)
        links = links_data['links']

    # Select a random student profile link for testing
    random_link = random.choice(links)
    logging.info(f"Opening random student profile: {random_link}")

    # Initialize Selenium WebDriver
    driver = webdriver.Edge(service=EdgeService(driver_path), options=edge_options)

    try:
        # Perform login before scraping
        login_to_platonus(driver)

        # Scrape data from the random profile
        student_data = scrape_student_profile(driver, random_link)

        # Save the scraped data to a JSON file
        output_path = r'C:\Users\syrym\Downloads\Platonus_Automatization\test_student_data.json'
        with open(output_path, 'w', encoding='utf-8') as outfile:
            json.dump(student_data, outfile, ensure_ascii=False, indent=4)
        logging.info(f"Student data successfully extracted and saved to '{output_path}'.")

    except Exception as e:
        logging.error(f"An error occurred during the scraping process: {e}")

    finally:
        logging.info("Closing WebDriver.")
        driver.quit()

if __name__ == "__main__":
    main()
