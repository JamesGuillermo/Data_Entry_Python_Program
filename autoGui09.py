from tkinter import END, Listbox, filedialog, messagebox # Import filedialog and messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import pyautogui
import time
import pandas as pd # Import pandas for Excel handling
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
        self.excel_data = None  # Store loaded DataFrame
        self.current_row_index = 0 # Track current row for batch processing
        self.is_batch_running = False # Flag to control batch process
        self.create_widgets()

    # --- Existing add_* methods remain the same ---

    def add_label(self, text, labelAnchor, labelPosX, labelPosY, txtFont, txtColor):
        label = tb.Label(
            self, 
            text=text, 
            font=txtFont, 
            foreground=txtColor
        )
        label.place(anchor=labelAnchor, x=labelPosX, y=labelPosY)
        return label
    
    def add_entry(self, entryAnchor, entryPosX, entryPosY, entryWidth, entryFont):
        entry = tb.Entry(
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
        # Existing labels, entries, comboboxes (excluding ID Number input if using Excel)
        # You might want to disable or hide the ID entry field if using Excel for IDs
        # Or keep it for manual single entry testing

        self.labels['mousePosition'] = self.add_label("Mouse Position: ", "center", 850, 100, ("Arial", 16), "white")
        self.labels['screenSize'] = self.add_label(self.screenSize(), "center", 850, 150, ("Arial", 16), "white")
        # Keep ID Number label for clarity, even if input might be ignored during batch
        self.labels['idNumber'] = self.add_label("ID Number: ", self.anchor, self.labelPosX, 250, ("Arial", 14), "white")
        self.labels['registrationType'] = self.add_label("Registration Type: ", self.anchor, self.labelPosX, 300, ("Arial", 14), "white")
        self.labels['transactionType'] = self.add_label("Transaction Type: ", self.anchor, self.labelPosX, 350, ("Arial", 14), "white")
        self.labels['serviceType'] = self.add_label("Service Type: ", self.anchor, self.labelPosX, 400, ("Arial", 14), "white")
        self.labels['companyName'] = self.add_label("Company Name: ", self.anchor, self.labelPosX, 450, ("Arial", 14), "white")
        self.labels['notesRemarks'] = self.add_label("Notes/Remarks: ", self.anchor, self.labelPosX, 500, ("Arial", 14), "white")

        # Keep ID Entry for manual testing/single run
        self.entries['idNumber'] = self.add_entry(self.anchor, self.entryPosX, 250, 50, ("Arial", 12))

        self.comboboxes['registrationType'] = self.add_combobox(
            self.anchor, self.entryPosX, 300, 50, 12,
            ["Consult", "FF Consult", "FTW", "Pre-Emp", "FF Pre-Emp", "Travel Clearance", "APE", "FF APE"],
            state="readonly"
        )
        self.comboboxes['registrationType'].bind("<<ComboboxSelected>>", self.on_registration_type_change)

        self.comboboxes['transactionType'] = self.add_combobox(
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

        # --- File Selection Widgets ---
        self.labels['excelFile'] = self.add_label("Excel File: ", self.anchor, self.labelPosX, 600, ("Arial", 14), "white")
        self.entries['excelFile'] = self.add_entry(self.anchor, self.entryPosX, 600, 50, ("Arial", 12))
        # Make entry read-only to prevent manual typing
        self.entries['excelFile'].config(state='readonly')
        self.buttons["browseExcel"] = self.add_button(
            self.anchor, self.entryPosX + 450, 600, "Browse...", self.browse_excel_file
        )

        # --- Automation Control Buttons ---
        # Button for single manual run (uses GUI inputs)
        self.buttons["startAutomation"] = self.add_button(
            self.anchor, self.entryPosX, 550, "Start Automation (Single)", self.automatedRegistration # Rename button text
        )
        # Button to start batch process (uses Excel data)
        self.buttons["startBatch"] = self.add_button(
            self.anchor, self.entryPosX, 650, "Start Automation (Batch)", self.start_batch_process
        )
        # Button to stop batch process (optional, requires careful handling)
        self.buttons["stopBatch"] = self.add_button(
            self.anchor, self.entryPosX + 200, 650, "Stop Batch", self.stop_batch_process
        )
        # Initially disable Stop button
        self.buttons["stopBatch"].config(state='disabled')

        self.label = tb.Label(self, text="", font=("Arial", 16), bootstyle="info")
        self.label.pack(pady=20)

        self.update_mouse_position()

    # --- Existing helper methods remain the same ---
    def get_mouse_position(self):
        try:
            x, y = pyautogui.position()
            r, g, b = pyautogui.pixel(x, y)
            return f"Mouse: ({x}, {y}) | Color: ({r}, {g}, {b})"
        except Exception as e:
            return f"Error reading pixel: {e}"

    def update_mouse_position(self):
        self.labels['mousePosition'].config(text=self.get_mouse_position())
        self.label.config(text=self.get_mouse_position())
        self.after(100, self.update_mouse_position)

    def screenSize(self):
        width, height = pyautogui.size()
        return f"Screen Size: {width}x{height}"

    def on_registration_type_change(self, event=None):
        """Event handler for registration type changes"""
        print("Registration type changed!")
        self.registrationTypeDependent()

    def registrationTypeDependent(self):
        """Update dependent comboboxes based on registration type"""
        try:
            selected_value = self.comboboxes['registrationType'].get()
            print(f"Selected registration type: {selected_value}")
            # --- Logic remains the same ---
            if selected_value == "Consult":
                self.comboboxes['transactionType'].set("consultation")
                self.comboboxes['serviceType'].set("consultation")
                self.comboboxes['notesRemarks'].set("fc, consult")
                print("Set transaction and service types to consultation")
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
                self.comboboxes['notesRemarks'].set("")
            elif selected_value == "FF Pre-Emp":
                self.comboboxes['transactionType'].set("follow-up pre-employment") # Adjusted based on your list
                self.comboboxes['serviceType'].set("pre-employment")
                self.comboboxes['notesRemarks'].set("fc, ff pre-employment") # Adjusted
            elif selected_value == "Travel Clearance":
                self.comboboxes['transactionType'].set("for entry")
                self.comboboxes['serviceType'].set("clearance")
                self.comboboxes['notesRemarks'].set("fc, travel clearance") # Adjusted
            elif selected_value == "APE":
                self.comboboxes['transactionType'].set("annual physical examination")
                self.comboboxes['serviceType'].set("annual physical examination")
                self.comboboxes['notesRemarks'].set("")
            elif selected_value == "FF APE":
                self.comboboxes['transactionType'].set("annual physical examination")
                self.comboboxes['serviceType'].set("annual physical examination")
                self.comboboxes['notesRemarks'].set("fc, ff annual physical examination") # Adjusted
        except Exception as e:
            print(f"Error in registrationTypeDependent: {e}")

    # --- New Methods for Excel Integration ---

    def browse_excel_file(self):
        """Open file dialog to select Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=(("Excel Files", "*.xlsx *.xls"), ("All Files", "*.*"))
        )
        if file_path:
            self.entries['excelFile'].config(state='normal') # Enable to modify
            self.entries['excelFile'].delete(0, END)
            self.entries['excelFile'].insert(0, file_path)
            self.entries['excelFile'].config(state='readonly') # Make read-only again

    def load_excel_data(self):
        """Load data from the selected Excel file"""
        file_path = self.entries['excelFile'].get()
        if not file_path:
            messagebox.showerror("Error", "Please select an Excel file first.")
            return False

        try:
            # Load Excel file, assuming data is on the first sheet
            self.excel_data = pd.read_excel(file_path)
            # Optional: Display column names for verification
            print("Excel Columns:", self.excel_data.columns.tolist())
            # Ensure required columns exist (adjust names as per your Excel)
            required_columns = ['ID Number', 'Registration Type', 'Transaction Type', 'Service Type', 'Company Name', 'Notes/Remarks']
            if not all(col in self.excel_data.columns for col in required_columns):
                 missing_cols = [col for col in required_columns if col not in self.excel_data.columns]
                 messagebox.showerror("Error", f"Missing columns in Excel file: {missing_cols}")
                 self.excel_data = None
                 return False

            self.current_row_index = 0 # Reset index
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Excel file:\n{e}")
            self.excel_data = None
            return False

    def start_batch_process(self):
        """Start the automated process for all rows in the Excel file"""
        if self.is_batch_running:
            messagebox.showwarning("Warning", "Batch process is already running.")
            return

        if not self.load_excel_data():
            return # Stop if loading failed

        if self.excel_data is not None and not self.excel_data.empty:
            self.is_batch_running = True
            self.buttons["startBatch"].config(state='disabled')
            self.buttons["stopBatch"].config(state='normal')
            messagebox.showinfo("Info", "Batch process started. Please do not move the mouse or use the keyboard until completion.")
            self.process_next_row() # Start processing
        else:
             messagebox.showwarning("Warning", "No data found in the Excel file.")

    def stop_batch_process(self):
        """Stop the batch process (sets flag, actual stop happens at next iteration)"""
        if self.is_batch_running:
            self.is_batch_running = False
            self.buttons["startBatch"].config(state='normal')
            self.buttons["stopBatch"].config(state='disabled')
            messagebox.showinfo("Info", "Batch process stop requested. It will finish the current entry.")

    def process_next_row(self):
        """Process the next row from the loaded Excel data"""
        if not self.is_batch_running:
            self.finish_batch()
            return

        if self.current_row_index < len(self.excel_data):
            row = self.excel_data.iloc[self.current_row_index]
            # Prepare DETAILS dictionary from the current row
            DETAILS = {
                "idNumber": str(row['ID Number']), # Ensure ID is string
                "registrationType": row['Registration Type'],
                "transactionType": row['Transaction Type'],
                "serviceType": row['Service Type'],
                "companyName": row['Company Name'],
                "notesRemarks": row['Notes/Remarks']
            }
            print(f"Processing Row {self.current_row_index + 1}: {DETAILS}")
            # Call the core automation logic with the current row's data
            self.run_automation(DETAILS)

            self.current_row_index += 1
            # Schedule the next row processing after a delay to allow the previous action to complete
            # Adjust delay as needed based on how long each automation run takes
            self.after(5000, self.process_next_row) # e.g., wait 5 seconds between entries
        else:
            self.finish_batch()

    def finish_batch(self):
        """Called when all rows are processed or batch is stopped"""
        self.is_batch_running = False
        self.buttons["startBatch"].config(state='normal')
        self.buttons["stopBatch"].config(state='disabled')
        if self.current_row_index >= len(self.excel_data):
            messagebox.showinfo("Success", "Batch automation completed for all entries!")
        else:
             messagebox.showinfo("Info", "Batch automation stopped.")

    # --- Modified Automation Method ---

    def automatedRegistration(self):
        """Handles single manual run using GUI inputs"""
        # Check if batch is running to prevent conflict
        if self.is_batch_running:
             messagebox.showwarning("Warning", "Batch process is running. Please wait or stop it.")
             return

        DETAILS = {
            "idNumber": self.entries['idNumber'].get(),
            "registrationType": self.comboboxes['registrationType'].get(),
            "transactionType": self.comboboxes['transactionType'].get(),
            "serviceType": self.comboboxes['serviceType'].get(),
            "companyName": self.comboboxes['companyName'].get(),
            "notesRemarks": self.comboboxes['notesRemarks'].get()
        }
        # Call the core automation logic
        self.run_automation(DETAILS)

    def run_automation(self, DETAILS):
        """Core automation logic that can be called with different data sources"""
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
                # Handle potential float values from Excel (e.g., ID 12345.0)
                if isinstance(text, float) and text.is_integer():
                     text = str(int(text))
                elif not isinstance(text, str):
                     text = str(text)
                pyautogui.write(text, interval=delay or CONFIG['defaultDelay'])
            else:
                print("No text to type or text is None")

        def main():
            try:
                print("Starting automated registration in 2 seconds...")
                time.sleep(CONFIG['startUpDelay'])
                print("Step 1: Opening new window")
                pyautogui.hotkey('ctrl', 'n')
                time.sleep(1)
                print("Step 2: Navigating initial fields")
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
                # Ensure types are strings before typing
                typeText(str(DETAILS['transactionType']))
                pressTabMultiple(4)
                typeText(str(DETAILS['serviceType']))
                print("Step 7: Assigning physician")
                clickAt('xy1')
                clickAt('xy2')
                typeText("asd") # Assuming this is a fixed value?
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
                typeText("1") # Assuming this is a fixed value?
                pyautogui.press('enter')
                print("Automation completed successfully for current entry!")
            except pyautogui.FailSafeException:
                print("Automation stopped by user (mouse moved to corner).")
                self.is_batch_running = False # Stop batch if failsafe triggered
                self.buttons["startBatch"].config(state='normal')
                self.buttons["stopBatch"].config(state='disabled')
            except KeyboardInterrupt:
                print("Automation interrupted by user (Ctrl+C).")
                self.is_batch_running = False
                self.buttons["startBatch"].config(state='normal')
                self.buttons["stopBatch"].config(state='disabled')
            except Exception as e:
                print(f"An error occurred during automation: {e}")
                # Optionally stop batch on error
                # self.is_batch_running = False
                # self.buttons["startBatch"].config(state='normal')
                # self.buttons["stopBatch"].config(state='disabled')

        main()

if __name__ == "__main__":
    app = AutoGuiApp()
    app.mainloop()