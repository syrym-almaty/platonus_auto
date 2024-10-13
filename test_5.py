import time
import random
import os
import json
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

students_data = []

try:
    # Open Platonus login page
    driver.get("https://platonus.iitu.edu.kz/")

    # Wait for the login page to load
    time.sleep(random.uniform(3, 6))

    # Click the login button (assuming autofill is enabled)
    try:
        login_button = driver.find_element(By.ID, "Submit1")
        login_button.click()
    except NoSuchElementException:
        print("Login button not found, assuming already logged in.")

    # Wait for the page to load after login
    time.sleep(random.uniform(5, 10))

    # Open Platonus students page
    driver.get("https://platonus.iitu.edu.kz/template.html#/students?page=1&countInPart=50&facultyID=0&gender=0&fundingProgram=0&participantProgram=0&year=0&cafedraID=0&professionID=0&specializationID=0&sGroupID=0&course=0&studyFormID=0&departmentID=0&state=0&academic_mobility=0&studyLanguageID=0&paymentFormID=0&militaryID=0&conditionally_enrolled=0&degreeID=0&grantTypeID=0&professionTypeID=0&centerTrainingDirectionsID=0&differentiatedGrant=0")

    # Wait for the page to load
    time.sleep(random.uniform(3, 6))

    # Extract student information from each entry on the page
    entry_number = 1
    while True:
        student_elements = driver.find_elements(By.XPATH, "//tr[@ng-repeat='student in vm.students']")
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
                    "order_number": entry_number,
                    "name": student_name,
                    "profile_link": student_profile_link,
                    "id": student_id,
                    "faculty": student_faculty,
                    "program": student_program,
                    "date_of_birth": student_dob,
                    "enrollment_date": student_enrollment_date
                }
                students_data.append(student_data)
                entry_number += 1
            except NoSuchElementException:
                print("Some student details are missing.")

        # Check if there is a next page and navigate to it
        try:
            next_button = driver.find_element(By.CLASS_NAME, "next-page-button-class")  # Update with correct class name
            next_button.click()
            time.sleep(random.uniform(3, 6))
        except NoSuchElementException:
            print("No more pages available.")
            break

finally:
    # Save all student data to a JSON file
    with open("students_data.json", "w", encoding="utf-8") as json_file:
        json.dump(students_data, json_file, ensure_ascii=False, indent=4)

    # Close the browser
    driver.quit()

# Create a .gitignore entry for the credentials file
gitignore_path = r"C:\Users\syrym\Downloads\Platonus_Automatization\.gitignore"
with open(gitignore_path, 'a') as gitignore:
    if "credentials.txt" not in open(gitignore_path).read():
        gitignore.write("\ncredentials.txt")