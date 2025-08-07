from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup Chrome driver
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Open the login page
driver.get("http://172.28.85.153:83/app/index/index.html#/login")

# Wait for the username field to be visible and interactable
input_username = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "username"))
)
input_username.send_keys("BlcnLifecare")  # Replace with your actual username

# Wait for the password field to be visible and interactable
input_password = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "password"))
)
input_password.send_keys("abcdE@123")  # Replace with your actual password

# Wait for the login button to be clickable
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "loginFormSubmitButton"))
)


# Scroll to the login button to ensure it's in view
driver.execute_script("arguments[0].scrollIntoView();", login_button)

WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.ID, "loginFormSubmitButton"))
)
# Click the login button
login_button.click()

try:
    WebDriverWait(driver, 10).until(EC.alert_is_present())  # Wait for the alert to appear
    alert = Alert(driver)  # Switch to the alert
    alert.accept()  # Accept the alert (click "OK")
    print("Alert was handled successfully")
except Exception as e:
    print("No alert present or error:", str(e))


# Find the anchor tag by link text and click
link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Reubal, Joanne DAPITAN"))
)
link.click()


# Wait for 20 seconds to see the result (optional, for debugging)
time.sleep(20)

# Quit the browser after operation
driver.quit()
