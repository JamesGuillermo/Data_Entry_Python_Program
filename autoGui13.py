import pyautogui
import threading
import time
from pynput import mouse
import sys

class SimpleBackgroundMonitor:
    def __init__(self):
        self.running = True
        self.click_count = 0
        
    def on_click(self, x, y, button, pressed):
        """This runs in background when you click anywhere"""
        if pressed and self.running:
            self.click_count += 1
            print(f"Click #{self.click_count} at position ({x}, {y})")
            
            # Example automation: Move mouse to top-left after every 5 clicks
            if self.click_count % 5 == 0:
                print("Moving mouse to (100, 100)!")
                pyautogui.moveTo(100, 100, duration=0.5)
    
    def start_monitoring(self):
        """Start listening for mouse clicks in background"""
        print("Background monitoring started...")
        print("Click anywhere on your screen to see it work!")
        print("Press Ctrl+C to stop")
        
        # Start mouse listener in background
        listener = mouse.Listener(on_click=self.on_click)
        listener.start()
        return listener
    
    def run(self):
        """Main program loop"""
        listener = self.start_monitoring()
        
        try:
            # Keep program running
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping...")
            self.running = False
            listener.stop()

# Run the program
if __name__ == "__main__":
    monitor = SimpleBackgroundMonitor()
    monitor.run()