import pyautogui
import time
import sys

# Configuration - Easy to modify
CONFIG = {
    'id_number': '6083568',
    'consultation_text': 'consultation',
    'default_delay': 0.1,
    'tab_delay': 0.1,
    'movement_duration': 0.5,
    'startup_delay': 2
}

# Coordinates - Easy to update if screen changes
COORDINATES = {
    'field_1': (237, 890),
    'field_2': (268, 881),
    'submit_button': (591, 182),
    'next_field': (215, 893),
    'medicine_field': (249, 927),
    'confirm_button': (561, 184),
    'final_field': (239, 966)
}

def wait(duration=None):
    """Standard wait function"""
    time.sleep(duration or CONFIG['default_delay'])

def press_tab_multiple(count, delay=None):
    """Press tab multiple times with delay"""
    tab_delay = delay or CONFIG['tab_delay']
    for _ in range(count):
        pyautogui.press("tab")
        time.sleep(tab_delay)

def click_at(coordinate_name, clicks=1):
    """Click at named coordinates"""
    if coordinate_name in COORDINATES:
        x, y = COORDINATES[coordinate_name]
        pyautogui.moveTo(x, y, duration=CONFIG['movement_duration'])
        for _ in range(clicks):
            pyautogui.click()
    else:
        print(f"Warning: Coordinate '{coordinate_name}' not found")

def type_text(text, interval=None):
    """Type text with standard interval"""
    pyautogui.write(text, interval=interval or CONFIG['default_delay'])

def main():
    """Main automation function"""
    try:
        # Initial setup
        print("Starting automation in 2 seconds...")
        time.sleep(CONFIG['startup_delay'])
        
        # Step 1: Open new window and navigate
        print("Step 1: Opening new window...")
        pyautogui.hotkey("ctrl", "n")
        time.sleep(1)
        
        # Step 2: Navigate through initial fields
        print("Step 2: Navigating initial fields...")
        press_tab_multiple(2)
        pyautogui.press("enter")
        press_tab_multiple(2)
        
        # Step 3: Enter ID number
        print("Step 3: Entering ID number...")
        type_text(CONFIG['id_number'])
        pyautogui.press("tab")
        wait(0.3)
        
        # Step 4: Navigate through form fields
        print("Step 4: Navigating form fields...")
        press_tab_multiple(2, 0.3)
        pyautogui.press("enter")
        wait(0.3)
        
        pyautogui.press("tab")
        pyautogui.press("enter")
        wait(0.3)
        
        pyautogui.press("tab")
        pyautogui.press("enter")
        
        # Step 5: Navigate to consultation field (lots of tabs)
        print("Step 5: Navigating to consultation field...")
        press_tab_multiple(28)  # Consolidated the 28 individual tab presses
        
        # Step 6: Enter consultation information
        print("Step 6: Entering consultation information...")
        type_text(CONFIG['consultation_text'])
        press_tab_multiple(4)
        type_text(CONFIG['consultation_text'])
        
        # Step 7: Handle form interactions
        print("Step 7: Handling form interactions...")
        click_at('field_1')
        click_at('field_2')
        
        type_text("asd")
        pyautogui.press("enter")
        
        click_at('submit_button', clicks=2)
        click_at('next_field', clicks=2)
        
        # Step 8: Enter medicine information
        print("Step 8: Entering medicine information...")
        click_at('medicine_field', clicks=2)
        type_text("elixer")
        pyautogui.press("enter")
        wait()
        
        click_at('confirm_button', clicks=2)
        click_at('final_field', clicks=2)
        
        # Step 9: Final consultation entry
        print("Step 9: Final consultation entry...")
        type_text("fc, consult")
        press_tab_multiple(3)
        pyautogui.press("enter")
        wait()
        
        type_text("1")
        pyautogui.press("enter")
        
        print("Automation completed successfully!")
        
        # Uncomment next line if you want to see mouse position
        # pyautogui.displayMousePosition()
        
    except pyautogui.FailSafeException:
        print("Automation stopped by fail-safe (mouse moved to corner)")
    except KeyboardInterrupt:
        print("Automation stopped by user (Ctrl+C)")
    except Exception as e:
        print(f"An error occurred: {e}")

def test_coordinates():
    """Test function to verify coordinates are correct"""
    print("Testing coordinates...")
    for name, (x, y) in COORDINATES.items():
        print(f"{name}: ({x}, {y})")
        pyautogui.moveTo(x, y, duration=1)
        input(f"Press Enter if {name} position is correct, or Ctrl+C to stop...")

if __name__ == "__main__":
    # Uncomment next line to test coordinates first
    # test_coordinates()
    
    main()