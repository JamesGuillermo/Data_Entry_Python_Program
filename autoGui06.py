from tkinter import END, Listbox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import *
import pyautogui
import time

import pyautogui
from datetime import datetime

class AutoGuiApp(tb.Window):
    def __init__(self):
        super().__init__(title="Auto GUI Application", themename="darkly")
        self.geometry("1700x1000")
        self.resizable(True, True)
        
        self.labels = {}
        self.entries = {}
        self.buttons = {}
        self.listboxes = {}
        self.comboboxes = {}

        self.anchor = "w"
        self.labelPosX = 30
        self.entryPosX = 300

        self.create_widgets()
        # Don't call registrationTypeDependent here - it will be called by event binding

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
        entry = Entry(
            self,  
            width=entryWidth, 
            font=entryFont
        )
        entry.place(anchor=entryAnchor, x=entryPosX, y=entryPosY)
        return entry
    
    def add_button(self, buttonAnchor, buttonPosX, buttonPosY, buttonText, buttonCommand):
        button = tb.Button(
            self, 
            text=buttonText, 
            command=buttonCommand
        )
        button.place(anchor=buttonAnchor, x=buttonPosX, y=buttonPosY)
        return button
    
    def add_listbox(self, listboxAnchor, listboxPosX, listboxPosY, listboxWidth, listboxHeight):
        listbox = Listbox(
            self, 
            width=listboxWidth, 
            height=listboxHeight
        )
        listbox.place(anchor=listboxAnchor, x=listboxPosX, y=listboxPosY)
        return listbox
    
    def add_combobox(self, comboAnchor, comboPosX, comboPosY, comboWidth, comboHeight, values, state="normal"):
        combobox = tb.Combobox(
            self, 
            width=comboWidth, 
            height=comboHeight, 
            values=values, 
            state=state
        )
        combobox.place(anchor=comboAnchor, x=comboPosX, y=comboPosY)
        return combobox

    def create_widgets(self):
        # Use ttkbootstrap Label for theming
        self.labels['mousePosition'] = self.add_label("Mouse Position: ", "center", 850, 100, ("Arial", 16), "white")
        self.labels['screenSize'] = self.add_label(self.screenSize(), "center", 850, 150, ("Arial", 16), "white")
        self.labels['idNumber'] = self.add_label("ID Number: ", self.anchor, self.labelPosX, 250, ("Arial", 14), "white")
        self.labels['registrationType'] = self.add_label("Registration Type: ", self.anchor, self.labelPosX, 300, ("Arial", 14), "white")
        self.labels['transactionType'] = self.add_label("Transaction Type: ", self.anchor, self.labelPosX, 350, ("Arial", 14), "white")  # Fixed typo
        self.labels['serviceType'] = self.add_label("Service Type: ", self.anchor, self.labelPosX, 400, ("Arial", 14), "white")
        self.labels['companyName'] = self.add_label("Company Name: ", self.anchor, self.labelPosX, 450, ("Arial", 14), "white")
        self.labels['notesRemarks'] = self.add_label("Notes/Remarks: ", self.anchor, self.labelPosX, 500, ("Arial", 14), "white")

        self.entries['idNumber'] = self.add_entry(self.anchor, self.entryPosX, 250, 50, ("Arial", 12))
        
        # Registration Type Combobox with event binding
        self.comboboxes['registrationType'] = self.add_combobox(
            self.anchor, self.entryPosX, 300, 50, 12,
            ["Consult", "FF Consult", "FTW", "Pre-Emp", "FF Pre-Emp", "Travel Clearance", "APE", "FF APE"], 
            state="readonly"
        )
        # Bind the event - this is the key fix!
        self.comboboxes['registrationType'].bind("<<ComboboxSelected>>", self.on_registration_type_change)
        
        self.comboboxes['transactionType'] = self.add_combobox(  # Fixed typo
            self.anchor, self.entryPosX, 350, 50, 12,
            ["consultation", "follow-up consultation", "fit to work", "pre-employment", "for entry", "annual physical examination"], 
            state="readonly"
        )
        self.comboboxes['serviceType'] = self.add_combobox(
            self.anchor, self.entryPosX, 400, 50, 12,
            ["consultation", "clearance", "pre-employment", "annual physical examination"], 
            state="readonly"
        )
        self.comboboxes['companyName'] = self.add_combobox(
            self.anchor, self.entryPosX, 450, 50, 12,
            ["elixer", "philippine batteries inc", "ramcar technology inc", "evergreen", "sta. maria", "firstcore", "topspot", "poultrymax", "northpoint", "nutriforyou", "quantus"], 
            state="readonly"
        )
        self.comboboxes['notesRemarks'] = self.add_combobox(
            self.anchor, self.entryPosX, 500, 50, 12,
            ["fc, consult", "fc, ff consult", "fc, consult, antigen", "fc, ftw"], 
            state="normal"
        )

        self.buttons["startAutomation"] = self.add_button(
            self.anchor, self.entryPosX, 550, "Start Automation", self.automatedRegistration
        )

        self.label = tb.Label(self, text="", font=("Arial", 16), bootstyle="info")
        self.label.pack(pady=20)

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
        self.labels['mousePosition'].config(text=self.get_mouse_position())
        self.label.config(text=self.get_mouse_position())
        # Schedule next update after 100ms
        self.after(100, self.update_mouse_position)

    def screenSize(self):
        width, height = pyautogui.size()
        return f"Screen Size: {width}x{height}"
    
    def on_registration_type_change(self, event=None):
        """Event handler for registration type changes"""
        print("Registration type changed!")  # Debug print
        self.registrationTypeDependent()
    
    def registrationTypeDependent(self):
        """Update dependent comboboxes based on registration type"""
        try:
            selected_value = self.comboboxes['registrationType'].get()
            print(f"Selected registration type: {selected_value}")  # Debug print
            
            if selected_value == "Consult":
                self.comboboxes['transactionType'].set("consultation")  # Fixed typo
                self.comboboxes['serviceType'].set("consultation")
                self.comboboxes['notesRemarks'].set("fc, consult")
                print("Set transaction and service types to consultation")  # Debug print
            elif selected_value == "FF Consult":
                self.comboboxes['transactionType'].set("follow-up consultation")
                self.comboboxes['serviceType'].set("consultation")
                self.comboboxes['notesRemarks'].set("fc, ff consult")
            elif selected_value == "FTW":
                self.comboboxes['transactionType'].set("fit to work")
                self.comboboxes['serviceType'].set("clearance")
                self.comboboxes['notesRemarks'].set("fc, ftw")
            elif selected_value == "Pre-Emp":
                self.comboboxes['transactionType'].set("pre-employment")
                self.comboboxes['serviceType'].set("pre-employment")
                self.comboboxes['notesRemarks'].set("")  # Clear notes for pre-employment
            elif selected_value == "FF Pre-Emp":
                self.comboboxes['transactionType'].set("follow-up pre-employment")
                self.comboboxes['serviceType'].set("pre-employment")
                self.comboboxes['notesRemarks'].set("fc, ff pre-employment")
            elif selected_value == "Travel Clearance":
                self.comboboxes['transactionType'].set("for entry")
                self.comboboxes['serviceType'].set("clearance")
                self.comboboxes['notesRemarks'].set("fc, travel clearance")
            elif selected_value == "APE":
                self.comboboxes['transactionType'].set("annual physical examination")
                self.comboboxes['serviceType'].set("annual physical examination")
                self.comboboxes['notesRemarks'].set("")
            elif selected_value == "FF APE":
                self.comboboxes['transactionType'].set("annual physical examination")
                self.comboboxes['serviceType'].set("annual physical examination")
                self.comboboxes['notesRemarks'].set("fc, ff annual physical examination")
            # Add more conditions as needed
            
        except Exception as e:
            print(f"Error in registrationTypeDependent: {e}")

    def automatedRegistration(self):

        DETAILS = {
            "idNumber": self.entries['idNumber'].get(),
            "registrationType": self.comboboxes['registrationType'].get(),
            "transactionType": self.comboboxes['transactionType'].get(),
            "serviceType": self.comboboxes['serviceType'].get(),
            "companyName": self.comboboxes['companyName'].get(),
            "notesRemarks": self.comboboxes['notesRemarks'].get()
        }

        COORDINATES = {
            'xy1': (237, 890),
            'xy2': (268, 881),
            'xy3': (591, 182),
            'xy4': (215, 893),
            'xy5': (249, 927),
            'xy6': (561, 184),
            'xy7': (239, 966)
        }

        CONFIG = {
            'defaultDelay': 0.1,
            'tabDelay': 0.1,
            'moveDelay': 0.5,
            'startUpDelay': 2
        }

        def wait(duration=None):
            time.sleep(duration or CONFIG['defaultDelay'])
        def pressTabMultiple(count, delay=None):
            for _ in range(count):
                pyautogui.press('tab')
                wait(delay or CONFIG['tabDelay'])
        def clickAt(coordinates, clicks=1):
            if coordinates in COORDINATES:
                x, y = COORDINATES[coordinates]
                pyautogui.moveTo(x, y, duration=CONFIG['moveDelay'])
                for _ in range(clicks):
                    pyautogui.click()
            else:
                print(f"Invalid coordinates: {coordinates}")
        def typeText(text, delay=None):
            if text:
                pyautogui.write(text, interval=delay or CONFIG['defaultDelay'])
            else:
                print("No text to type")

        def main():
            try:
                print("Starting automated registration in 2 seconds...")
                time.sleep(CONFIG['startUpDelay'])

                print("Step 1: Opening new window")
                pyautogui.hotkey('ctrl', 'n')
                time.sleep(1)

                print("Step 2: Navigatingn initial fields")
                pressTabMultiple(2)
                pyautogui.press('enter')
                pressTabMultiple(2)

                print("Step 3: Entering ID Number")
                typeText(DETAILS['idNumber'])
                pyautogui.press('tab')
                wait()

                print("Step 4: Navigating form fields")
                pressTabMultiple(2, 0.3)
                pyautogui.press('enter')
                wait(0.3)

                pyautogui.press("tab")
                pyautogui.press("enter")
                wait(0.3)

                pyautogui.press("tab")
                pyautogui.press("enter")

                print("Step 5: Navigating transaction fields")
                pressTabMultiple(28)

                print("Step 6: Entering Transaction and Service Types")
                typeText(DETAILS['transactionType'])
                pressTabMultiple(4)
                typeText(DETAILS['serviceType'])

                print("Step 7: Assigning physician")
                clickAt('xy1')
                clickAt('xy2')

                typeText("asd")
                pyautogui.press("enter")
                clickAt('xy3', clicks=2)
                clickAt('xy4', clicks=2)

                print("Step 8: Entering Company Name")
                clickAt('xy5', clicks=2)
                typeText(DETAILS['companyName'])
                pyautogui.press("enter")
                wait()

                clickAt('xy6', clicks=2)
                clickAt('xy7', clicks=2)

                print("Step 9: Remarks and Notes")
                typeText(DETAILS['notesRemarks'])
                pressTabMultiple(3)
                pyautogui.press('enter')
                wait()

                typeText("1")
                pyautogui.press('enter')

                print("Automation completed successfully!")

            except pyautogui.FailSafeException:
                print("Automation stopped by user (mouse moved to corner).")
            except KeyboardInterrupt:
                print("Automation interrupted by user (Ctrl+C).")
            except Exception as e:
                print(f"An error occurred during automation: {e}")

        main()

if __name__ == "__main__":
    app = AutoGuiApp()
    app.mainloop()