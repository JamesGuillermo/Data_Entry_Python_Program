import pyautogui
import threading
import time
import queue
from pynput import mouse, keyboard
import tkinter as tk
from tkinter import ttk

class BackgroundAutomation:
    def __init__(self):
        self.running = False
        self.event_queue = queue.Queue()
        self.root = None
        
    def create_system_tray_interface(self):
        """Create a minimal GUI for system tray control"""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide main window
        
        # Create system tray menu
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Start", command=self.start_automation)
        menu.add_command(label="Stop", command=self.stop_automation)
        menu.add_separator()
        menu.add_command(label="Exit", command=self.exit_program)
        
        return menu
    
    def start_automation(self):
        """Start background automation"""
        if not self.running:
            self.running = True
            # Start background threads
            threading.Thread(target=self.background_worker, daemon=True).start()
            threading.Thread(target=self.input_listener, daemon=True).start()
            print("Background automation started")
    
    def stop_automation(self):
        """Stop background automation"""
        self.running = False
        print("Background automation stopped")
    
    def exit_program(self):
        """Exit the program"""
        self.running = False
        if self.root:
            self.root.quit()
    
    def background_worker(self):
        """Main background automation loop"""
        while self.running:
            try:
                # Process events from queue
                if not self.event_queue.empty():
                    event = self.event_queue.get_nowait()
                    self.handle_event(event)
                
                # Perform background tasks
                self.perform_background_tasks()
                
                time.sleep(0.1)  # Small delay to prevent high CPU usage
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error in background worker: {e}")
    
    def input_listener(self):
        """Listen for input events in background"""
        def on_move(x, y):
            if self.running:
                self.event_queue.put(('mouse_move', x, y))
        
        def on_click(x, y, button, pressed):
            if self.running and pressed:
                self.event_queue.put(('mouse_click', x, y, button))
        
        def on_press(key):
            if self.running:
                self.event_queue.put(('key_press', key))
                if key == keyboard.Key.esc:
                    self.stop_automation()
        
        # Start listeners
        mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
        keyboard_listener = keyboard.Listener(on_press=on_press)
        
        mouse_listener.start()
        keyboard_listener.start()
        
        # Keep listeners running
        try:
            while self.running:
                time.sleep(0.1)
        except:
            pass
        finally:
            mouse_listener.stop()
            keyboard_listener.stop()
    
    def handle_event(self, event):
        """Handle queued events"""
        event_type = event[0]
        if event_type == 'mouse_move':
            x, y = event[1], event[2]
            # Handle mouse movement
            pass
        elif event_type == 'mouse_click':
            x, y, button = event[1], event[2], event[3]
            # Handle mouse click
            pass
        elif event_type == 'key_press':
            key = event[1]
            # Handle key press
            pass
    
    def perform_background_tasks(self):
        """Perform your automation tasks here"""
        # Example: Check for specific conditions and automate
        pass
    
    def run(self):
        """Run the background automation system"""
        self.start_automation()
        
        # Keep the program running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.exit_program()

# Usage
if __name__ == "__main__":
    automation = BackgroundAutomation()
    automation.run()