import pyautogui
import time
import sys

# Wait for you to switch to Excel
time.sleep(3)

'''pyautogui.write("Name, Age, Country", interval=0.1)
pyautogui.press("enter")
pyautogui.write("Alice, 25, USA", interval=0.1)
pyautogui.press("enter")
pyautogui.write("Bob, 30, UK", interval=0.1)'''
#pyautogui.write("6083568", interval=0.1)  # ID Number
#pyautogui.hotkey("ctrl", "v")  # Save

print("Press Ctrl + C in the terminal to stop.\n")

# Print screen resolution once
#print("Screen size:", pyautogui.size())

'''while True:
    # Get current mouse position
    x, y = pyautogui.position()
    print(f"Mouse position: X={x}, Y={y}", end="\r")  # overwrite line
    time.sleep(0.1)  # update every 0.1 second

'''
print(sys.path)
print(pyautogui.__file__)

import sys
sys.path.insert(0, r"C:\Users\James Cachero\OneDrive\Documents\PythonProgramming\Data_Entry_Python_Program\.venv\Lib\site-packages")

print(sys.executable)