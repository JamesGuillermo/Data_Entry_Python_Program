from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://cms.multilifecare.ph/Account/Login/")

input_username = driver.find_element(By.ID, "Username")
input_username.send_keys("James")
input_password = driver.find_element(By.ID, "Password")
input_password.send_keys("Life@123")



wait = WebDriverWait(driver, 10)
login_button = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "button")))
login_button.click()



time.sleep(60)  # Wait for 5 seconds to see the page

driver.quit()  # Close the browser after the operation