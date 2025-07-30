import pyautogui
import threading
import time
from pynput import mouse, keyboard

class BackgroundMouseController:
    def __init__(self):
        self.running = False
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()
        
    def start_background_monitoring(self):
        """Start monitoring mouse/keyboard in background"""
        self.running = True
        # Start listener threads
        mouse_listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click)
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        
        mouse_listener.start()
        keyboard_listener.start()
        
        return mouse_listener, keyboard_listener
    
    def on_move(self, x, y):
        # Handle mouse movement
        if self.running:
            print(f"Mouse moved to ({x}, {y})")
    
    def on_click(self, x, y, button, pressed):
        # Handle mouse clicks
        if self.running and pressed:
            print(f"Mouse clicked at ({x}, {y})")
    
    def on_press(self, key):
        # Handle key presses
        if key == keyboard.Key.esc:
            self.running = False

# Usage
controller = BackgroundMouseController()
mouse_listener, keyboard_listener = controller.start_background_monitoring()

# Your main program continues here
try:
    while controller.running:
        time.sleep(1)
        # Do other work here
except KeyboardInterrupt:
    controller.running = False

mouse_listener.join()
keyboard_listener.join()