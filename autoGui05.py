from tkinter import END, Listbox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import *

import pyautogui
from datetime import datetime

# Optional imports (remove if not used later)
# import os
# import pandas as pd
# import sqlite3
# import sys


class AutoGuiApp(tb.Window):
    def __init__(self):
        super().__init__(title="Auto GUI Application", themename="darkly")
        self.geometry("1700x1000")
        self.resizable(True, True)
        self.create_widgets()
        self.add_label("Mouse Position Tracker", "w", 0, 500, ("Arial", 16), "white")
        self.add_entry("w", 0, 570, 200, ("Arial", 12))

    def add_label(self, text, labelAnchor, labelPosX, labelPosY, txtFont, txtColor):
        label = Label(
            self, 
            text=text, 
            font=txtFont, 
            foreground=txtColor
        )
        label.place(anchor=labelAnchor, x=labelPosX, y=labelPosY)
        return label
    
    def add_entry(self, entryAnchor, entryPosX, entryPosY, entryWidth, entryFont):
        entry =Entry(
            self,  
            width=entryWidth, 
            font=entryFont
        )
        entry.place(anchor=entryAnchor,x=entryPosX, y=entryPosY)
        return entry

    def create_widgets(self):
        # Use ttkbootstrap Label for theming
        self.label = tb.Label(self, text="", font=("Arial", 16), bootstyle="info")
        self.label.pack(pady=20)

        self.start_button = tb.Button(
            self, 
            text="Start Automation", 
            bootstyle="success", 
            command=self.start_automation
        )
        self.start_button.pack(pady=10)

        # Optional: Add a stop button or log box later
        self.log_text = tb.Text(self, height=10)
        self.log_text.pack(padx=20, pady=10, fill="x")

        # Start updating mouse position
        self.update_mouse_position()

    def get_mouse_position(self):
        try:
            x, y = pyautogui.position()
            r, g, b = pyautogui.pixel(x, y)
            return f"Mouse: ({x}, {y}) | Color: ({r}, {g}, {b})"
        except Exception as e:
            return f"Error reading pixel: {e}"

    def update_mouse_position(self):
        # Update label with current mouse info
        self.label.config(text=self.get_mouse_position())
        # Schedule next update after 100ms
        self.after(100, self.update_mouse_position)

    def start_automation(self):
        # Avoid blocking the main thread
        self.log_message("Automation started... (Press Ctrl+C in console to stop if needed)")
        # Example: Move mouse in a square (non-blocking example)
        self.after(100, self.demo_automation)  # Run in GUI-safe way

    def demo_automation(self):
        """Example automation - move mouse in a small square"""
        try:
            original_pos = pyautogui.position()

            # Small movement (safe)
            pyautogui.moveTo(original_pos[0] + 10, original_pos[1], duration=0.1)
            pyautogui.moveTo(original_pos[0] + 10, original_pos[1] + 10, duration=0.1)
            pyautogui.moveTo(original_pos[0], original_pos[1] + 10, duration=0.1)
            pyautogui.moveTo(original_pos[0], original_pos[1], duration=0.1)

            self.log_message(f"Moved mouse in square near ({original_pos[0]}, {original_pos[1]})")
        except Exception as e:
            self.log_message(f"Automation error: {e}")

    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(END, f"[{timestamp}] {message}\n")
        self.log_text.see(END)  # Auto-scroll


if __name__ == "__main__":
    app = AutoGuiApp()
    app.mainloop()