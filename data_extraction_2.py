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

driver_path = r"C:\Users\syrym\Downloads\Platonus_Automatization\msedgedriver.exe"

edge_options = Options()
edge_options.add_argument('--disable-gpu')
edge_options.add_argument('--no-sandbox')
edge_options.add_argument('--disable-dev-shm-usage')
user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."]
random_user_agent = random.choice(user_agents)
edge_options.add_argument(f'user-agent={random_user_agent}')
edge_options.add_experimental_option('useAutomationExtension', False)
edge_options.add_experimental_option('excludeSwitches', ['enable-automation'])
edge_options.add_argument('--disable-blink-features=AutomationControlled')
edge_options.add_argument('--disable-extensions')
edge_options.add_argument('--profile-directory=Default')
edge_options.add_argument('--disable-plugins-discovery')
edge_options.add_argument('--disable-popup-blocking')
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
    personal_data = {}
    try:
        personal_data['Surname'] = driver.find_element(By.NAME, 'lastName').get_attribute('value')
        personal_data['Name'] = driver.find_element(By.NAME, 'firstName').get_attribute('value')
        personal_data['IIN'] = driver.find_element(By.NAME, 'iin').get_attribute('value')
        personal_data['Nationality'] = driver.find_element(By.XPATH, "//label[contains(text(), 'NATIONALITY')]/following::span[1]").get_attribute('title')
        personal_data['Date of birth'] = driver.find_element(By.NAME, 'birthDate').get_attribute('value')
        personal_data['Gender'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Gender')]/following::span[1]").get_attribute('title')
        personal_data['Citizenship'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Citizenship')]/following::span[1]").get_attribute('title')
        personal_data['Country of arrival'] = driver.find_element(By.XPATH, "//label[contains(text(), 'The country of arrival')]/following::span[1]").get_attribute('title')
        personal_data['Area of arrival'] = driver.find_element(By.XPATH, "//label[contains(text(), 'The area of arrival')]/following::span[1]").get_attribute('title')
        personal_data['Place of birth (cato)'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Place of birth (cato)')]/following::span[1]").get_attribute('title')
        personal_data['Registration place (cato)'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Registration place (cato)')]/following::span[1]").get_attribute('title')
        personal_data['Registration address'] = driver.find_element(By.NAME, 'address').get_attribute('value')
        personal_data['Living place (cato)'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Living place (cato)')]/following::span[1]").get_attribute('title')
        personal_data['Living address'] = driver.find_element(By.NAME, 'livingAddress').get_attribute('value')
    except NoSuchElementException:
        pass
    return personal_data

def extract_documents_data(driver):
    documents_data = {}
    try:
        documents_data['Type of identity document'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Type of identity document')]/following::span[1]").get_attribute('title')
        documents_data['Identity number'] = driver.find_element(By.NAME, 'icNumber').get_attribute('value')
        documents_data['Date of issuance'] = driver.find_element(By.NAME, 'icDate').get_attribute('value')
        documents_data['Issuing authority'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Select the authority that issued the identity document')]/following::span[1]").get_attribute('title')
    except NoSuchElementException:
        pass
    return documents_data

def extract_contact_details(driver):
    contact_details = {}
    try:
        contact_details['Home phone'] = driver.find_element(By.NAME, 'phone').get_attribute('value')
        contact_details['Mobile phone'] = driver.find_element(By.NAME, 'mobilePhone').get_attribute('value')
        contact_details['Mail'] = driver.find_element(By.NAME, 'mail').get_attribute('value')
        contact_details['Additional mail'] = driver.find_element(By.NAME, 'additionalMail').get_attribute('value')
        contact_details['VKontakte profile link'] = driver.find_element(By.NAME, 'vkLink').get_attribute('value')
        contact_details['Facebook profile link'] = driver.find_element(By.NAME, 'fbLink').get_attribute('value')
        contact_details['Instagram profile link'] = driver.find_element(By.NAME, 'instagramLink').get_attribute('value')
    except NoSuchElementException:
        pass
    return contact_details

def extract_specialty_information(driver):
    specialty_info = {}
    try:
        specialty_info['Enrolled date'] = driver.find_element(By.NAME, 'startDate').get_attribute('value')
        specialty_info['Form of education'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Form of education')]/following::span[1]").get_attribute('title')
        specialty_info['Specialization'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Specialization')]/following::span[1]").get_attribute('title')
        specialty_info['Course'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Course')]/following::span[1]").get_attribute('title')
        specialty_info['Curriculum'] = driver.find_element(By.XPATH, "//div[contains(@class, 'col-md-12 form-control ng-binding')]").text.strip()
        specialty_info['Form of payment'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Form of payment')]/following::span[1]").get_attribute('title')
        specialty_info['Academic degree'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Academic degree')]/following::span[1]").get_attribute('title')
        specialty_info['Profession/education program group'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Profession/education program group')]/following::span[1]").get_attribute('title')
        specialty_info['Language of education'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Language of education')]/following::span[1]").get_attribute('title')
        specialty_info['Group'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Group')]/following::span[1]").get_attribute('title')
        academic_calendar_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'col-md-12 form-control ng-binding')]")
        for elem in academic_calendar_elements:
            text = elem.text.strip()
            if 'Academic calendar' in text:
                specialty_info['Academic calendar'] = text
                break
    except NoSuchElementException:
        pass
    return specialty_info

def extract_education_information(driver):
    education_info = {}
    try:
        graduated_school = driver.find_element(By.XPATH, "//input[@name='end_school' and @type='radio']").is_selected()
        education_info['Graduated from school'] = 'Yes' if graduated_school else 'No'
        education_info['Country where graduated school'] = driver.find_element(By.XPATH, "//label[contains(text(), 'The country where graduated school')]/following::span[1]").get_attribute('title')
        education_info['Locality of the institution'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Locality of the institution')]/following::span[1]").get_attribute('title')
        education_info['Place of finishing school'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Place of finishing school')]/following::span[1]").get_attribute('title')
        education_info['Name of institution graduated'] = driver.find_element(By.XPATH, "//label[contains(text(), 'Name(number) of institution which he/she graduated')]/following::span[1]").get_attribute('title')
        education_info['Certificate number'] = driver.find_element(By.NAME, 'certificateNumber').get_attribute('value')
        education_info['Given date'] = driver.find_element(By.NAME, 'certificateDate').get_attribute('value')
        try:
            gpa_element = driver.find_element(By.XPATH, "//h5[contains(@class, 'ng-binding')]")
            gpa_text = gpa_element.text
            gpa_start = gpa_text.find('GPA')
            if gpa_start != -1:
                gpa_substring = gpa_text[gpa_start:]
                gpa_value = gpa_substring.split(':')[1].split(',')[0].strip()
                education_info['GPA'] = gpa_value
            else:
                education_info['GPA'] = None
        except NoSuchElementException:
            education_info['GPA'] = None
    except NoSuchElementException:
        pass
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
        pass
    try:
        contact_tab = driver.find_element(By.XPATH, "//button[@data-bs-target='#tab2']")
        contact_tab.click()
        time.sleep(1)
        student_data['Contact details'] = extract_contact_details(driver)
    except Exception:
        pass
    try:
        specialty_tab = driver.find_element(By.XPATH, "//button[@data-bs-target='#tab3']")
        specialty_tab.click()
        time.sleep(1)
        student_data['Information about the specialty'] = extract_specialty_information(driver)
    except Exception:
        pass
    try:
        education_tab = driver.find_element(By.XPATH, "//button[@data-bs-target='#tab4']")
        education_tab.click()
        time.sleep(1)
        student_data['Information about education'] = extract_education_information(driver)
    except Exception:
        pass
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
