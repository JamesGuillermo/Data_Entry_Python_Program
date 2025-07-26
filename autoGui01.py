import pyautogui
import time
import sys

time.sleep(2)

pyautogui.hotkey("ctrl", "n")  # Paste clipboard content
time.sleep(1)  # Wait for the new window to open
pyautogui.press("tab")  # Press Enter to confirm
pyautogui.press("tab")
pyautogui.press("enter")
pyautogui.press("tab")  # Press Enter to confirm
pyautogui.press("tab")
pyautogui.write("6083568", interval=0.1)  # ID Number
pyautogui.press("tab")  # Press Enter to confirm
time.sleep(.3)  # Wait for the next field
pyautogui.press("tab")
time.sleep(.3)  # Wait for the next field
pyautogui.press("tab")
pyautogui.press("enter")
time.sleep(.3)  # Wait for the next field
pyautogui.press("tab")
pyautogui.press("enter")
time.sleep(.3)  # Wait for the next field
pyautogui.press("tab")
pyautogui.press("enter")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.write("consultation", interval=0.1)
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.write("consultation", interval=0.1)
pyautogui.moveTo(237, 890, duration=.5)  # Move mouse to a specific position
pyautogui.click()  # Click at the current mouse position
pyautogui.moveTo(268, 881, duration=.5)
pyautogui.click() 

pyautogui.write("asd", interval=0.1)
pyautogui.press("enter")
pyautogui.moveTo(591, 182, duration=.5)  # Move mouse to a specific position
pyautogui.click()  # Click at the current mouse position
pyautogui.click()
pyautogui.moveTo(215, 893, duration=.5)  # Move mouse to a specific position
pyautogui.click()  # Click at the current mouse position
pyautogui.click()


pyautogui.moveTo(249, 927, duration=.5)  # Move mouse to a specific position
pyautogui.click()  # Click at the current mouse position
pyautogui.click()
pyautogui.write("elixer", interval=0.1)
pyautogui.press("enter")
time.sleep(.1)
pyautogui.moveTo(561, 184, duration=.5)  # Move mouse to a specific position
pyautogui.click()  # Click at the current mouse position
pyautogui.click()

pyautogui.moveTo(239, 966, duration=.5)  # Move mouse to a specific position
pyautogui.click()
pyautogui.click()

pyautogui.write("fc, consult", interval=0.1)

time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("tab")
time.sleep(.1)
pyautogui.press("enter")

time.sleep(.1)
pyautogui.write("1", interval=0.1)
pyautogui.press("enter")

pyautogui.displayMousePosition()

#while True:
    # Get current mouse position
#    x, y = pyautogui.position()
#    print(f"Mouse position: X={x}, Y={y}", end="\r")  # overwrite line
#    time.sleep(0.1)  # update every 0.1 second