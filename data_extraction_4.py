import time
import random
import json
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to the Edge WebDriver
driver_path = r"C:\Users\syrym\Downloads\Platonus_Automatization\msedgedriver.exe"

# Edge options
edge_options = Options()
edge_options.add_argument('--disable-gpu')
edge_options.add_argument('--no-sandbox')
edge_options.add_argument('--disable-dev-shm-usage')

# User-Agent
user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."]
random_user_agent = random.choice(user_agents)
edge_options.add_argument(f'user-agent={random_user_agent}')

# Disable automation flags
edge_options.add_experimental_option('useAutomationExtension', False)
edge_options.add_experimental_option('excludeSwitches', ['enable-automation'])
edge_options.add_argument('--disable-blink-features=AutomationControlled')

# Other options
edge_options.add_argument('--disable-extensions')
edge_options.add_argument('--profile-directory=Default')
edge_options.add_argument('--disable-plugins-discovery')
edge_options.add_argument('--disable-popup-blocking')

# User data directory
user_data_dir = r"C:\Users\syrym\Downloads\Platonus_Automatization\User_Data"
edge_options.add_argument(f'--user-data-dir={user_data_dir}')

def login_to_platonus(driver):
    driver.get("https://platonus.iitu.edu.kz/")
    time.sleep(2)
    try:
        login_button = driver.find_element(By.ID, "Submit1")
        login_button.click()
    except NoSuchElementException:
        pass
    time.sleep(3)

def extract_personal_data(driver):
    # [Code remains the same as before]
    # Assuming this section works fine based on your feedback
    personal_data = {}
    # (Existing code here...)
    return personal_data

def extract_documents_data(driver):
    documents_data = {}
    try:
        # Type of identity document
        documents_data['Type of identity document'] = driver.find_element(
            By.XPATH,
            "//label[contains(text(), 'Type of identity document')]/following-sibling::div//span[@class='select2-selection__rendered']"
        ).text.strip()
        # Identity number
        documents_data['Identity number'] = driver.find_element(
            By.NAME,
            'icNumber'
        ).get_attribute('value').strip()
        # Serial number of identity card
        documents_data['Serial number of identity card'] = driver.find_element(
            By.NAME,
            'icseries'
        ).get_attribute('value').strip()
        # Date of issuance of the identity document
        documents_data['Date of issuance'] = driver.find_element(
            By.NAME,
            'icDate'
        ).get_attribute('value').strip()
        # Validity of identity document
        documents_data['Validity of identity document'] = driver.find_element(
            By.NAME,
            'icFinishDate'
        ).get_attribute('value').strip()
    except NoSuchElementException:
        pass
    return documents_data

def extract_contact_details(driver):
    contact_details = {}
    try:
        # Home phone
        contact_details['Home phone'] = driver.find_element(
            By.NAME,
            'phone'
        ).get_attribute('value').strip()
        # Mobile phone
        contact_details['Mobile phone'] = driver.find_element(
            By.NAME,
            'mobilePhone'
        ).get_attribute('value').strip()
        # Mail
        contact_details['Mail'] = driver.find_element(
            By.NAME,
            'mail'
        ).get_attribute('value').strip()
        # Additional mail
        contact_details['Additional mail'] = driver.find_element(
            By.NAME,
            'additionalMail'
        ).get_attribute('value').strip()
        # VKontakte profile link
        contact_details['VKontakte profile link'] = driver.find_element(
            By.NAME,
            'vkLink'
        ).get_attribute('value').strip()
        # Facebook profile link
        contact_details['Facebook profile link'] = driver.find_element(
            By.NAME,
            'fbLink'
        ).get_attribute('value').strip()
        # Instagram profile link
        contact_details['Instagram profile link'] = driver.find_element(
            By.NAME,
            'instagramLink'
        ).get_attribute('value').strip()
    except NoSuchElementException:
        pass
    return contact_details

def extract_specialty_information(driver):
    specialty_info = {}
    try:
        # Enrolled date
        specialty_info['Enrolled date'] = driver.find_element(
            By.NAME,
            'startDate'
        ).get_attribute('value').strip()
        # Academic degree
        specialty_info['Academic degree'] = driver.find_element(
            By.XPATH,
            "//label[contains(text(), 'Academic degree')]/following-sibling::div//span[@class='select2-selection__rendered']"
        ).text.strip()
        # Form of education
        specialty_info['Form of education'] = driver.find_element(
            By.XPATH,
            "//label[contains(text(), 'Form of education')]/following-sibling::div//span[@class='select2-selection__rendered']"
        ).text.strip()
        # Profession/education program group
        specialty_info['Profession/education program group'] = driver.find_element(
            By.XPATH,
            "//label[contains(text(), 'Profession/education program group')]/following-sibling::div//span[@class='select2-selection__rendered']"
        ).text.strip()
        # Specialization/Educational Program
        specialty_info['Specialization/Educational Program'] = driver.find_element(
            By.XPATH,
            "//label[contains(text(), 'Specialization/Educational Program')]/following-sibling::div//span[@class='select2-selection__rendered']"
        ).text.strip()
        # Language of education
        specialty_info['Language of education'] = driver.find_element(
            By.XPATH,
            "//label[contains(text(), 'Language of education')]/following-sibling::div//span[@class='select2-selection__rendered']"
        ).text.strip()
        # Course
        specialty_info['Course'] = driver.find_element(
            By.XPATH,
            "//label[contains(text(), 'Course')]/following-sibling::div//span[@class='select2-selection__rendered']"
        ).text.strip()
        # Group
        specialty_info['Group'] = driver.find_element(
            By.XPATH,
            "//label[contains(text(), 'Group')]/following-sibling::div//span[@class='select2-selection__rendered']"
        ).text.strip()
        # Curriculum
        specialty_info['Curriculum'] = driver.find_element(
            By.XPATH,
            "//label[contains(text(), 'Curriculum')]/following-sibling::div[contains(@class, 'form-control')]"
        ).text.strip()
        # Academic calendar
        specialty_info['Academic calendar'] = driver.find_element(
            By.XPATH,
            "//label[contains(text(), 'Academic calendar')]/following-sibling::div[contains(@class, 'form-control')]"
        ).text.strip()
        # Form of payment
        specialty_info['Form of payment'] = driver.find_element(
            By.XPATH,
            "//label[contains(text(), 'Form of payment')]/following-sibling::div//span[@class='select2-selection__rendered']"
        ).text.strip()
    except NoSuchElementException:
        pass
    return specialty_info

def extract_education_information(driver):
    education_info = {}
    # [Adjustments can be made here similarly if needed]
    # Since you didn't provide the DOM for this section, ensure to update it accordingly
    return education_info

def scrape_student_profile(driver, profile_link):
    driver.get(profile_link)
    time.sleep(2)
    student_data = {}
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'nav-tabs')))
    except TimeoutException:
        return student_data
    student_data['Personal data'] = extract_personal_data(driver)
    try:
        documents_tab = driver.find_element(By.XPATH, "//button[@data-bs-target='#tab1']")
        documents_tab.click()
        time.sleep(1)
        student_data['Documents'] = extract_documents_data(driver)
    except Exception:
        student_data['Documents'] = {}
    try:
        contact_tab = driver.find_element(By.XPATH, "//button[@data-bs-target='#tab2']")
        contact_tab.click()
        time.sleep(1)
        student_data['Contact details'] = extract_contact_details(driver)
    except Exception:
        student_data['Contact details'] = {}
    try:
        specialty_tab = driver.find_element(By.XPATH, "//button[@data-bs-target='#tab3']")
        specialty_tab.click()
        time.sleep(1)
        student_data['Information about the specialty'] = extract_specialty_information(driver)
    except Exception:
        student_data['Information about the specialty'] = {}
    try:
        education_tab = driver.find_element(By.XPATH, "//button[@data-bs-target='#tab4']")
        education_tab.click()
        time.sleep(1)
        student_data['Information about education'] = extract_education_information(driver)
    except Exception:
        student_data['Information about education'] = {}
    return student_data

def main():
    with open(r'C:\Users\syrym\Downloads\Platonus_Automatization\links.json', 'r', encoding='utf-8') as file:
        links_data = json.load(file)
        links = links_data['links']
    random_link = random.choice(links)
    driver = webdriver.Edge(service=EdgeService(driver_path), options=edge_options)
    try:
        login_to_platonus(driver)
        student_data = scrape_student_profile(driver, random_link)
        output_path = r'C:\Users\syrym\Downloads\Platonus_Automatization\test_student_data.json'
        with open(output_path, 'w', encoding='utf-8') as outfile:
            json.dump(student_data, outfile, ensure_ascii=False, indent=4)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
