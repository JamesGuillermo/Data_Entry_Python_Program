import pyautogui
import pytesseract
from PIL import Image
import time

# Set the path to tesseract executable (Windows only)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def find_text_on_screen(text_to_scan, region=None):
    """
    Capture screenshot and search for specific text
    region: (left, top, width, height) - optional area to search
    """
    try:
        # Capture screenshot of entire screen or specific region
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()
        
        # Use OCR to extract text
        extracted_text = pytesseract.image_to_string(screenshot)
        
        # Check if target text exists
        if text_to_scan.lower() in extracted_text.lower():
            print(f"Text '{text_to_scan}' found!")
            return True
        else:
            print(f"Text '{text_to_scan}' not found!")
            return False
            
    except Exception as e:
        print(f"Error in OCR: {e}")
        return False

# Usage
time.sleep(2)
textToScan = "1118"

if find_text_on_screen(textToScan):
    print("Text found on screen!")
    # Do something when text is found
else:
    print("Text not found on screen!")