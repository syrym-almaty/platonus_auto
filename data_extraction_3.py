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
    personal_data = {}
    try:
        personal_data['Surname'] = driver.find_element(By.NAME, 'lastName').get_attribute('value').strip()
        personal_data['Name'] = driver.find_element(By.NAME, 'firstName').get_attribute('value').strip()
        personal_data['IIN'] = driver.find_element(By.NAME, 'iin').get_attribute('value').strip()
        personal_data['Nationality'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NATIONALITY')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
        personal_data['Date of birth'] = driver.find_element(By.NAME, 'birthDate').get_attribute('value').strip()
        personal_data['Gender'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'GENDER')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
        personal_data['Citizenship'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CITIZENSHIP')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
        personal_data['Country of arrival'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'THE COUNTRY OF ARRIVAL')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
        personal_data['Area of arrival'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'THE AREA OF ARRIVAL')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
        personal_data['Place of birth (cato)'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'PLACE OF BIRTH (CATO)')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
        personal_data['Registration place (cato)'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'REGISTRATION PLACE (CATO)')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
        personal_data['Registration address'] = driver.find_element(By.NAME, 'address').get_attribute('value').strip()
        personal_data['Living place (cato)'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'LIVING PLACE (CATO)')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
        personal_data['Living address'] = driver.find_element(By.NAME, 'livingAddress').get_attribute('value').strip()
    except NoSuchElementException:
        pass
    return personal_data

def extract_documents_data(driver):
    documents_data = {}
    try:
        documents_data['Type of identity document'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'TYPE OF IDENTITY DOCUMENT')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
        documents_data['Identity number'] = driver.find_element(By.NAME, 'icNumber').get_attribute('value').strip()
        documents_data['Date of issuance'] = driver.find_element(By.NAME, 'icDate').get_attribute('value').strip()
        documents_data['Issuing authority'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SELECT THE AUTHORITY THAT ISSUED THE IDENTITY DOCUMENT')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
    except NoSuchElementException:
        pass
    return documents_data

def extract_contact_details(driver):
    contact_details = {}
    try:
        phone_elements = driver.find_elements(By.NAME, 'phone')
        if len(phone_elements) >= 1:
            contact_details['Home phone'] = phone_elements[0].get_attribute('value').strip()
        if len(phone_elements) >= 2:
            contact_details['Mobile phone'] = phone_elements[1].get_attribute('value').strip()
        else:
            contact_details['Mobile phone'] = ""
        contact_details['Mail'] = driver.find_element(By.NAME, 'mail').get_attribute('value').strip()
        contact_details['Additional mail'] = driver.find_element(By.NAME, 'additionalMail').get_attribute('value').strip()
        contact_details['VKontakte profile link'] = driver.find_element(By.NAME, 'vkLink').get_attribute('value').strip()
        contact_details['Facebook profile link'] = driver.find_element(By.NAME, 'fbLink').get_attribute('value').strip()
        contact_details['Instagram profile link'] = driver.find_element(By.NAME, 'instagramLink').get_attribute('value').strip()
    except NoSuchElementException:
        pass
    return contact_details

def extract_specialty_information(driver):
    specialty_info = {}
    try:
        specialty_info['Enrolled date'] = driver.find_element(By.NAME, 'startDate').get_attribute('value').strip()
        specialty_info['Form of education'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'FORM OF EDUCATION')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
        specialty_info['Specialization'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'SPECIALIZATION')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
        specialty_info['Course'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'COURSE')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
        # Curriculum
        curriculum_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'col-md-12 form-control ng-binding')]")
        for elem in curriculum_elements:
            text = elem.text.strip()
            if "curriculum" in text.lower():
                specialty_info['Curriculum'] = text
                break
        specialty_info['Form of payment'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'FORM OF PAYMENT')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
        specialty_info['Academic degree'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ACADEMIC DEGREE')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
        specialty_info['Profession/education program group'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'PROFESSION/EDUCATION PROGRAM GROUP')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
        specialty_info['Language of education'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'LANGUAGE OF EDUCATION')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
        specialty_info['Group'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'GROUP')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
        # Academic calendar
        for elem in curriculum_elements:
            text = elem.text.strip()
            if "academic calendar" in text.lower() or "академический календарь" in text.lower():
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
        education_info['Country where graduated school'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'THE COUNTRY WHERE GRADUATED SCHOOL')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
        education_info['Locality of the institution'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'LOCALITY OF THE INSTITUTION')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
        education_info['Place of finishing school'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'PLACE OF FINISHING SCHOOL')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
        education_info['Name of institution graduated'] = driver.find_element(By.XPATH, "//label[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'NAME(NUMBER) OF INSTITUTION WHICH HE/SHE GRADUATED')]/following-sibling::div//span[@class='select2-selection__rendered']").get_attribute('title').strip()
        education_info['Certificate number'] = driver.find_element(By.NAME, 'certificateNumber').get_attribute('value').strip()
        education_info['Given date'] = driver.find_element(By.NAME, 'certificateDate').get_attribute('value').strip()
        # GPA extraction
        try:
            gpa_element = driver.find_element(By.XPATH, "//h5[contains(@class, 'ng-binding')]")
            gpa_text = gpa_element.text
            gpa_start = gpa_text.find('GPA')
            if gpa_start != -1:
                gpa_substring = gpa_text[gpa_start:]
                gpa_value = gpa_substring.split(':')[1].split(',')[0].strip()
                education_info['GPA'] = gpa_value
            else:
                education_info['GPA'] = ""
        except NoSuchElementException:
            education_info['GPA'] = ""
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
