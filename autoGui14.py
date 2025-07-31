import pyautogui
import time
import os

time.sleep(2)  # Wait for 2 seconds before starting

try:
    location = pyautogui.locateOnScreen('noRecordFound.png', confidence=0.8)
    if location:
        print("No Record found!")
        print(f"Image located at: {location}")
        # Click on the found image
        # pyautogui.click(pyautogui.center(location))
    else:
        print("Image not found on screen!")
        
except pyautogui.ImageNotFoundException:
    print("Error: Image file 'noRecordFound.png' not found or cannot be located!")
except FileNotFoundError:
    print("Error: Image file 'noRecordFound.png' does not exist!")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


time.sleep(1)  # Wait for 2 seconds before starting
try:
    location = pyautogui.locateOnScreen('outpatientRegistrationForm.png', confidence=0.8)
    if location:
        print("Outpatient Registration Form")
        print(f"Image located at: {location}")
        # Click on the found image
        # pyautogui.click(pyautogui.center(location))
    else:
        print("Image not found on screen!")
        
except pyautogui.ImageNotFoundException:
    print("Error: Image file 'noRecordFound.png' not found or cannot be located!")
except FileNotFoundError:
    print("Error: Image file 'noRecordFound.png' does not exist!")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

time.sleep(1)  # Wait for 2 seconds before starting
try:
    location = pyautogui.locateOnScreen('withOutstandingBalance.png', confidence=0.8)
    if location:
        print("With outsanding balance!")
        print(f"Image located at: {location}")
        # Click on the found image
        # pyautogui.click(pyautogui.center(location))
    else:
        print("Image not found on screen!")
        
except pyautogui.ImageNotFoundException:
    print("Error: Image file 'withOutstandingBalance.png' not found or cannot be located!")
except FileNotFoundError:
    print("Error: Image file 'withOutstandingBalance.png' does not exist!")
except Exception as e:
    print(f"An unexpected error occurred: {e}")



print("Current working directory:", os.getcwd())
print("Looking for images in this directory.")

# Test with a lower confidence first
try:
    loc1 = pyautogui.locateOnScreen('noRecordFound.png', confidence=0.7)
    print(f"'noRecordFound.png' found at: {loc1}")
except pyautogui.ImageNotFoundException:
    print("'noRecordFound.png' NOT found with confidence 0.7")

try:
    loc2 = pyautogui.locateOnScreen('outpatientRegistrationForm.png', confidence=0.7)
    print(f"'outpatientRegistrationForm.png' found at: {loc2}")
except pyautogui.ImageNotFoundException:
     print("'outpatientRegistrationForm.png' NOT found with confidence 0.7")

try:
    loc3 = pyautogui.locateOnScreen('withOutstandingBalance.png', confidence=0.7)
    print(f"'withOutstandingBalance.png' found at: {loc3}")
except pyautogui.ImageNotFoundException:
     print("'withOutstandingBalance.png' NOT found with confidence 0.7")

# If 0.7 doesn't work, try 0.8. If 0.8 works in the test but not in the main script,
# the timing or screen state in the main script is likely the issue.