import time
import random
import json
import logging
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the path to the Edge WebDriver
driver_path = r"C:\Users\syrym\Downloads\Platonus_Automatization\msedgedriver.exe"

# Set up Edge options
edge_options = Options()
edge_options.add_argument('--headless')  # Run in headless mode for better performance
edge_options.add_argument('--disable-gpu')
edge_options.add_argument('--no-sandbox')
edge_options.add_argument('--disable-dev-shm-usage')  # To optimize memory usage in headless mode

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

# Other useful options to simulate a human-like behavior
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

def scrape_student_page(driver, page_number):
    page_data = []
    try:
        logging.info(f"Opening student data page {page_number}.")
        driver.get(f"https://platonus.iitu.edu.kz/template.html#/students?page={page_number}&countInPart=50&facultyID=0&gender=0&fundingProgram=0&participantProgram=0&year=0&cafedraID=0&professionID=0&specializationID=0&sGroupID=0&course=0&studyFormID=0&departmentID=0&state=0&academic_mobility=0&studyLanguageID=0&paymentFormID=0&militaryID=0&conditionally_enrolled=0&degreeID=0&grantTypeID=0&professionTypeID=0&centerTrainingDirectionsID=0&differentiatedGrant=0")

        # Wait for the page to load
        time.sleep(random.uniform(2, 4))

        # Extract student information from each entry on the page
        student_elements = driver.find_elements(By.XPATH, "//tr[@ng-repeat='student in vm.students']")
        if not student_elements:
            logging.info(f"No students found on page {page_number}. Ending data extraction for this page.")
            return page_data

        for student in student_elements:
            try:
                student_name = student.find_element(By.XPATH, ".//a[@class='link-info ng-binding']").text
                student_profile_link = student.find_element(By.XPATH, ".//a[@class='link-info ng-binding']").get_attribute("href")
                student_id = student_profile_link.split("/")[-1]
                student_faculty = student.find_elements(By.XPATH, ".//td[@class='ng-binding']")[1].text
                student_program = student.find_elements(By.XPATH, ".//td[@class='ng-binding']")[2].text
                student_dob = student.find_elements(By.XPATH, ".//td[@class='ng-binding']")[3].text
                student_enrollment_date = student.find_elements(By.XPATH, ".//td[@class='ng-binding']")[4].text

                # Create a dictionary for the student information
                student_data = {
                    "order_number": (page_number - 1) * 50 + len(page_data) + 1,
                    "name": student_name,
                    "profile_link": student_profile_link,
                    "id": student_id,
                    "faculty": student_faculty,
                    "program": student_program,
                    "date_of_birth": student_dob,
                    "enrollment_date": student_enrollment_date
                }
                page_data.append(student_data)
                logging.info(f"Extracted data for student {student_data['order_number']}: {student_name}.")
            except NoSuchElementException:
                logging.warning(f"Some student details are missing on page {page_number}.")
    except UnexpectedAlertPresentException as e:
        # Handle unexpected alert
        alert = driver.switch_to.alert
        alert_text = alert.text
        logging.error(f"Unexpected alert on page {page_number}: {alert_text}")
        alert.accept()
        # Retry accessing the page after handling the alert
        logging.info(f"Retrying page {page_number} after handling alert.")
        return scrape_student_page(driver, page_number)
    except Exception as e:
        logging.error(f"An error occurred on page {page_number}: {e}")
    return page_data

def scrape_all_pages(total_pages):
    all_students_data = []
    driver = webdriver.Edge(service=EdgeService(driver_path), options=edge_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    try:
        # Perform login before scraping
        login_to_platonus(driver)
        for page in range(1, total_pages + 1):
            page_data = scrape_student_page(driver, page)
            all_students_data.extend(page_data)
            # Random delay to mimic human behavior
            time.sleep(random.uniform(1, 3))
    finally:
        logging.info("Closing WebDriver.")
        driver.quit()
    return all_students_data

# Set the total number of pages to scrape
total_pages = 298
students_data = scrape_all_pages(total_pages)

# Save all student data to a JSON file
logging.info("Saving all student data to 'students_data.json'.")
with open("students_data.json", "w", encoding="utf-8") as json_file:
    json.dump(students_data, json_file, ensure_ascii=False, indent=4)

# Create a .gitignore entry for the credentials file
gitignore_path = r"C:\Users\syrym\Downloads\Platonus_Automatization\.gitignore"
gitignore_entry = "credentials.txt"

with open(gitignore_path, 'r+') as gitignore:
    content = gitignore.read()
    if gitignore_entry not in content:
        gitignore.write(f"\n{gitignore_entry}")
