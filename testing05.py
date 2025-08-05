from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup Chrome driver
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Open the login page
driver.get("https://cms.multilifecare.ph/Account/Login/")

# Find and fill in username and password
input_username = driver.find_element(By.ID, "Username")
input_username.send_keys("James")
input_password = driver.find_element(By.ID, "Password")
input_password.send_keys("Life@123")  # Assuming empty password

# Wait for the login button to be clickable
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@class='btn btn-primary center-block btn-flat']"))
)

# Scroll to the login button to ensure it's in view
driver.execute_script("arguments[0].scrollIntoView();", login_button)

# Click the login button
login_button.click()
login_button.click()

# Wait for 20 seconds to see the result (optional)
time.sleep(20)

# Quit the browser after operation
driver.quit()
