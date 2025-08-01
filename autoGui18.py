from tkinter import END, Listbox, filedialog, messagebox # Import filedialog and messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import pyautogui
import time
import pandas as pd # Import pandas for Excel handling
from datetime import datetime
import os
import threading
import keyboard # Import keyboard for ESC key listening

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
        self.checkbuttons = {}
        self.anchor = "w"
        self.labelPosX = 30
        self.entryPosX = 300
        self.excel_data = None  # Store loaded DataFrame
        self.current_row_index = 0 # Track current row for batch processing
        self.is_batch_running = False # Flag to control batch process
        # --- Add Stop Flag for ESC key ---
        self.stop_automation_flag = False
        # --- Add Flag for Listener ---
        self.listener_active = False
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

    def add_checkbutton(self, checkAnchor, checkPosX, checkPosY, text, variable, command=None):
        checkbutton = tb.Checkbutton(
            self,
            text=text,
            variable=variable,
            command=command # Add command parameter
        )
        checkbutton.place(anchor=checkAnchor, x=checkPosX, y=checkPosY)
        return checkbutton

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
            ["Consult", "FF Consult", "FTW", "Pre-Emp", "FF Pre-Emp", "Travel Clearance", "APE", "FF APE","Lab request"],
            state="readonly"
        )
        self.comboboxes['registrationType'].bind("<<ComboboxSelected>>", self.on_registration_type_change)

        self.comboboxes['transactionType'] = self.add_combobox(
            self.anchor, self.entryPosX, 350, 50, 12,
            ["consultation", "follow-up consultation", "fit to work", "pre-employment", "for entry", "annual physical examination", "laboratory"],
            state="readonly"
        )
        self.comboboxes['serviceType'] = self.add_combobox(
            self.anchor, self.entryPosX, 400, 50, 12,
            ["consultation", "clearance", "pre-employment", "annual physical examination","laboratory", "tele-consult"],
            state="readonly"
        )
        self.comboboxes['companyName'] = self.add_combobox(
            self.anchor, self.entryPosX, 450, 50, 12,
            ["elixer", "philippine batteries inc", "ramcar technology inc", "evergreen", "sta. maria", "firstcore", "topspot", "poultrymax", "northpoint", "nutriforyou", "quantus", "san rafael", "subic"],
            state="readonly"
        )
        self.comboboxes['notesRemarks'] = self.add_combobox(
            self.anchor, self.entryPosX, 500, 50, 12,
            ["ape AM","ape AF","ape BM","ape BF","fc, consult", "fc, ff consult", "fc, consult, antigen", "fc, ftw", "lab req", "teleconsult", "fc, ff ape"],
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
        self.buttons["saveEntry"] = self.add_button(
            self.anchor, self.entryPosX, 700, "Save Entry to Excel", self.save_entry_to_excel
        )

        # --- Checkbuttons for Auto Remarks ---
        # Create individual variables for each checkbutton
        self.auto_remarks_vars = {
            'AM': tb.BooleanVar(value=False),
            'AF': tb.BooleanVar(value=False),
            'BM': tb.BooleanVar(value=False),
            'BF': tb.BooleanVar(value=False)
        }
        # Create checkbuttons with unique names and variables
        self.checkbuttons['AM'] = self.add_checkbutton(
            self.anchor, 1000, 250, "AM", self.auto_remarks_vars['AM'], command=self.update_notes_remarks
        )
        self.checkbuttons['AF'] = self.add_checkbutton(
            self.anchor, 1000, 300, "AF", self.auto_remarks_vars['AF'], command=self.update_notes_remarks
        )
        self.checkbuttons['BM'] = self.add_checkbutton(
            self.anchor, 1000, 350, "BM", self.auto_remarks_vars['BM'], command=self.update_notes_remarks
        )
        self.checkbuttons['BF'] = self.add_checkbutton(
            self.anchor, 1000, 400, "BF", self.auto_remarks_vars['BF'], command=self.update_notes_remarks
        )

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

    def update_notes_remarks(self):
        """Update Notes/Remarks based on selected checkboxes"""
        selected = []
        for key, var in self.auto_remarks_vars.items():
            if var.get():
                selected.append(f"ape {key}")
        # Join selected items with a comma and space, or set to empty string if none
        notes = ", ".join(selected) if selected else ""
        self.comboboxes['notesRemarks'].set(notes)
        print(f"Notes/Remarks updated to: {notes}")

    def registrationTypeDependent(self):
        """Update dependent comboboxes based on registration type"""
        try:
            selected_value = self.comboboxes['registrationType'].get()
            print(f"Selected registration type: {selected_value}")
            # --- Logic remains the same ---
            if selected_value == "Consult":
                self.comboboxes['transactionType'].set("consultation")
                self.comboboxes['serviceType'].set("consultation")
                # Only set notes if no checkboxes are selected
                if not any(var.get() for var in self.auto_remarks_vars.values()):
                    self.comboboxes['notesRemarks'].set("fc, consult")
                print("Set transaction and service types to consultation")
            elif selected_value == "FF Consult":
                self.comboboxes['transactionType'].set("follow-up consultation")
                self.comboboxes['serviceType'].set("consultation")
                if not any(var.get() for var in self.auto_remarks_vars.values()):
                    self.comboboxes['notesRemarks'].set("fc, ff consult")
            elif selected_value == "FTW":
                self.comboboxes['transactionType'].set("fit to work")
                self.comboboxes['serviceType'].set("clearance")
                if not any(var.get() for var in self.auto_remarks_vars.values()):
                    self.comboboxes['notesRemarks'].set("fc, ftw")
            elif selected_value == "Pre-Emp":
                self.comboboxes['transactionType'].set("pre-employment")
                self.comboboxes['serviceType'].set("pre-employment")
                if not any(var.get() for var in self.auto_remarks_vars.values()):
                    self.comboboxes['notesRemarks'].set("")
            elif selected_value == "FF Pre-Emp":
                self.comboboxes['transactionType'].set("follow-up pre-employment") # Adjusted based on your list
                self.comboboxes['serviceType'].set("pre-employment")
                if not any(var.get() for var in self.auto_remarks_vars.values()):
                    self.comboboxes['notesRemarks'].set("fc, ff pre-employment") # Adjusted
            elif selected_value == "Travel Clearance":
                self.comboboxes['transactionType'].set("for entry")
                self.comboboxes['serviceType'].set("clearance")
                if not any(var.get() for var in self.auto_remarks_vars.values()):
                    self.comboboxes['notesRemarks'].set("fc, travel clearance") # Adjusted
            elif selected_value == "APE":
                self.comboboxes['transactionType'].set("annual physical examination")
                self.comboboxes['serviceType'].set("annual physical examination")
                if not any(var.get() for var in self.auto_remarks_vars.values()):
                    self.comboboxes['notesRemarks'].set("")
            elif selected_value == "FF APE":
                self.comboboxes['transactionType'].set("annual physical examination")
                self.comboboxes['serviceType'].set("annual physical examination")
                if not any(var.get() for var in self.auto_remarks_vars.values()):
                    self.comboboxes['notesRemarks'].set("fc, ff ape") # Adjusted
            elif selected_value == "Lab request":
                self.comboboxes['transactionType'].set("laboratory")
                self.comboboxes['serviceType'].set("laboratory")
                if not any(var.get() for var in self.auto_remarks_vars.values()):
                    self.comboboxes['notesRemarks'].set("lab req")
        except Exception as e:
            print(f"Error in registrationTypeDependent: {e}")

    # --- New Methods for Excel Integration ---
    def save_entry_to_excel(self):
        """Appends the current GUI data as a new row to the selected Excel file."""
        file_path = self.entries['excelFile'].get()
        if not file_path:
            messagebox.showerror("Error", "Please select an Excel file first.")
            return
        # Gather data from GUI fields
        new_data = {
            "ID Number": self.entries['idNumber'].get(),
            "Registration Type": self.comboboxes['registrationType'].get(),
            "Transaction Type": self.comboboxes['transactionType'].get(),
            "Service Type": self.comboboxes['serviceType'].get(),
            "Company Name": self.comboboxes['companyName'].get(),
            "Notes/Remarks": self.comboboxes['notesRemarks'].get()
        }
        # Create a DataFrame for the new row
        new_row_df = pd.DataFrame([new_data])
        try:
            # Check if file exists
            if os.path.exists(file_path):
                # If file exists, read it, append the new row, and save
                try:
                    # Load existing data
                    existing_df = pd.read_excel(file_path)
                    # Ensure columns match or handle discrepancies if necessary
                    # This simple approach assumes the structure is correct
                    # A more robust version might check column names and order
                    # Append the new row using concat (recommended over append)
                    updated_df = pd.concat([existing_df, new_row_df], ignore_index=True)
                    # Save the updated DataFrame back to Excel
                    updated_df.to_excel(file_path, index=False)
                    messagebox.showinfo("Success", "Data appended to Excel file successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update existing Excel file:\n{e}")
            else:
                 # If file doesn't exist, create it with the new data
                 # Ensure column order matches the expected structure
                 new_row_df.to_excel(file_path, index=False)
                 messagebox.showinfo("Success", "New Excel file created and data saved!")
        except Exception as e:
             messagebox.showerror("Error", f"An error occurred while saving:\n{e}")

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
            messagebox.showinfo("Info", "Batch process started. Please do not move the mouse or use the keyboard until completion.\nPress 'ESC' to attempt to stop.")
            # --- Add ESC listener for batch ---
            self.stop_automation_flag = False
            self.listener_active = True
            self.start_escape_listener()
            # --- End Add ESC listener ---
            self.process_next_row() # Start processing
        else:
             messagebox.showwarning("Warning", "No data found in the Excel file.")

    def stop_batch_process(self):
        """Stop the batch process (sets flag, actual stop happens at next iteration)"""
        if self.is_batch_running:
            self.is_batch_running = False
            self.buttons["startBatch"].config(state='normal')
            self.buttons["stopBatch"].config(state='disabled')
            # --- Signal stop for ESC listener ---
            self.listener_active = False
            # --- End Signal stop ---
            messagebox.showinfo("Info", "Batch process stop requested. It will finish the current entry.")

    # --- Add ESC Key Listener ---
    def start_escape_listener(self):
        """Starts a thread to listen for the Escape key."""
        def listen_for_escape():
            print("Escape listener started for batch. Press 'ESC' to stop automation.")
            keyboard.wait('esc') # This blocks the listener thread until 'esc' is pressed
            if self.listener_active: # Only act if automation was supposed to be running
                print("'ESC' key pressed. Setting stop flag for batch.")
                self.stop_automation_flag = True
                # Move mouse to corner to trigger pyautogui failsafe as a backup
                # This is a crude way to try and interrupt pyautogui actions
                try:
                    pyautogui.moveTo(0, 0)
                except:
                    pass # Ignore errors if pyautogui is busy

        # Run the listener in a separate thread so it doesn't block the GUI
        if hasattr(self, '_listener_thread') and self._listener_thread.is_alive():
            # If a listener thread is already running, don't start another one
             print("Listener thread already active.")
        else:
            self._listener_thread = threading.Thread(target=listen_for_escape, daemon=True)
            self._listener_thread.start()
    # --- End Add ESC Key Listener ---

    def process_next_row(self):
        """Process the next row from the loaded Excel data"""
        # --- Check stop flag ---
        if self.stop_automation_flag:
            print("Batch process stopped by ESC key.")
            self.finish_batch()
            return
        # --- End Check stop flag ---
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
        # --- Signal stop for ESC listener ---
        self.listener_active = False
        # --- End Signal stop ---
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

        # --- Add ESC listener for single run ---
        self.stop_automation_flag = False
        self.listener_active = True
        self.start_escape_listener()
        # --- End Add ESC listener ---

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
            'xy7': (239, 966),
            'transactionTypeLoc': (490, 582),
            'serviceTypeLoc': (925, 478),
            'asdLoc': (260, 881),
            'asdLoc2': (592, 184),
            'companyNameLoc': (265, 918),
            'comanyNameLoc2': (611, 184), # Typo in variable name, but keeping for consistency with original
            'notesRemarksLoc': (269, 962),
        }
        CONFIG = {
            'defaultDelay': 0.1,
            'tabDelay': 0.1,
            'moveDelay': 0.5,
            'startUpDelay': 2
        }

        def wait(duration=None):
            # --- Check stop flag during wait ---
            if self.stop_automation_flag:
                 print("Automation stop requested via ESC key (during wait).")
                 raise KeyboardInterrupt("Stopped by ESC key")
            # --- End Check stop flag ---
            time.sleep(duration or CONFIG['defaultDelay'])

        def pressTabMultiple(count, delay=None):
            for _ in range(count):
                # --- Check stop flag ---
                if self.stop_automation_flag:
                    print("Automation stop requested via ESC key (during tab press).")
                    raise KeyboardInterrupt("Stopped by ESC key")
                # --- End Check stop flag ---
                pyautogui.press('tab')
                wait(delay or CONFIG['tabDelay'])

        def clickAt(coordinates, clicks=1):
            # --- Check stop flag ---
            if self.stop_automation_flag:
                 print("Automation stop requested via ESC key (before click).")
                 raise KeyboardInterrupt("Stopped by ESC key")
            # --- End Check stop flag ---
            if coordinates in COORDINATES:
                x, y = COORDINATES[coordinates]
                pyautogui.moveTo(x, y, duration=CONFIG['moveDelay'])
                for _ in range(clicks):
                    # --- Check stop flag ---
                    if self.stop_automation_flag:
                        print("Automation stop requested via ESC key (during click).")
                        raise KeyboardInterrupt("Stopped by ESC key")
                    # --- End Check stop flag ---
                    pyautogui.click()
            else:
                print(f"Invalid coordinates: {coordinates}")

        def typeText(text, delay=None):
            # --- Check stop flag ---
            if self.stop_automation_flag:
                 print("Automation stop requested via ESC key (before typing).")
                 raise KeyboardInterrupt("Stopped by ESC key")
            # --- End Check stop flag ---
            if text:
                # Handle potential float values from Excel (e.g., ID 12345.0)
                if isinstance(text, float) and text.is_integer():
                     text = str(int(text))
                elif not isinstance(text, str):
                     text = str(text)
                # Note: pyautogui.write is blocking, so checking the flag *inside* it is hard.
                # The checks before/after calling typeText and during wait() are the main methods.
                pyautogui.write(text, interval=delay or CONFIG['defaultDelay'])
            else:
                print("No text to type or text is None")

        def cancelOperation():
            print("Operation cancelled by user.")
            # Move mouse to corner to trigger failsafe
            pyautogui.moveTo(0, 0)

        def withOutstandingBalanceProceed():
            pyautogui.click(924,641)
            print("Proceeding with outstanding balance...")
            pressTabMultiple(1)
            pyautogui.press('enter')

        def continueFormRegistaration(): # Keeping typo for consistency
            
            time.sleep(0.2)  # Wait for 0.5 seconds before starting
            print("Continuing with form registration...")
            time.sleep(0.2)  # Wait for 1 second before starting
            print("Clicking on transaction type field")
            clickAt('transactionTypeLoc')
            time.sleep(0.2)
            print("Typing transaction type")
            typeText(DETAILS['transactionType'])
            print("Clicking on service type field")
            #clickAt('serviceTypeLoc')
            pressTabMultiple(4)
            time.sleep(0.1)
            print("Typing service type")
            typeText(DETAILS['serviceType'])
            print("assigning physician")
            clickAt('asdLoc', clicks=2)
            time.sleep(0.2)
            print("Typing 'asd' in the field")
            typeText("asd")
            pyautogui.press("enter")
            clickAt('asdLoc2', clicks=2)
            time.sleep(0.2)
            print("Clicking on company name field")
            clickAt('companyNameLoc', clicks=2)
            time.sleep(0.2)
            print("Typing company name")
            typeText(DETAILS['companyName'])
            pyautogui.press("enter")
            clickAt('comanyNameLoc2', clicks=2) # Typo in variable name
            time.sleep(0.2)
            print("Clicking on notes/remarks field")
            clickAt('notesRemarksLoc', clicks=1)
            time.sleep(0.2)
            pressTabMultiple(1)
            print("Typing notes/remarks")
            time.sleep(0.2)
            typeText(DETAILS['notesRemarks'])
            pressTabMultiple(1)
            pyautogui.press('enter')
            typeText("1")  # Assuming this is a fixed value?
            pressTabMultiple(3)
            pyautogui.press('enter')
            print("Automation completed successfully for current entry!")

        def useExistingRecord():
            pressTabMultiple(1)
            pyautogui.press('enter')

        def chargingServices():
            """Handle charging services with proper delays and error handling"""
            print("Starting charging services...")
            
            try:
                # Click on charging services area
                print("Clicking charging services button...")
                pyautogui.click(1671, 564)
                time.sleep(1)  # Increased delay
                
                # Check if stop flag is set
                if self.stop_automation_flag:
                    raise KeyboardInterrupt("Stopped by ESC key")
                
                # Type "nu" (presumably for nurse or something similar)
                print("Typing 'nu'...")
                typeText("nu")
                time.sleep(1)  # Add delay after typing
                
                # Double click on coordinates (575,187)
                print("Double clicking on selection...")
                pyautogui.click(575, 187)
                pyautogui.click(575, 187)
                time.sleep(3)  # Increased delay
                
                # Check stop flag again
                if self.stop_automation_flag:
                    raise KeyboardInterrupt("Stopped by ESC key")
                
                # Click on another area
                print("Clicking on form area...")
                pyautogui.click(349, 859)
                time.sleep(1)  # Increased delay
                
                # Click on input field
                print("Clicking on input field...")
                pyautogui.click(592, 153)
                time.sleep(1)  # Increased delay
                
                # Check stop flag before processing charges
                if self.stop_automation_flag:
                    raise KeyboardInterrupt("Stopped by ESC key")
                
                # Get the notes/remarks for processing
                notes_remarks = DETAILS['notesRemarks']
                print(f"Processing charges for: {notes_remarks}")

                #final step
                def finalStep():
                    pyautogui.click(1473, 1010)
                    time.sleep(1)  # Increased delay
                    typeText("1")
                    pyautogui.press('enter')
                
                # Process different types of charges based on notes/remarks
                if notes_remarks == "fc, consult" or notes_remarks == "fc, ff consult" or notes_remarks == "fc, ff pre-employment" or notes_remarks == "fc, ftw" or notes_remarks == "fc, ff ape":
                    print("Adding consultation fee...")
                    typeText("consultation fee")
                    time.sleep(1)  # Add delay after typing
                    
                    pyautogui.click(283, 231)
                    time.sleep(1)  # Increased delay
                    
                    pyautogui.press('enter')
                    time.sleep(1)  # Add delay after enter
                    print("Consultation fee added successfully")
                    time.sleep(1)  # Increased delay
                    finalStep()
                    print("Final step completed successfully")
                    return
                    
                elif notes_remarks == "fc, consult, antigen" or notes_remarks == "fc, ftw, antigen":
                    print("Adding consultation fee with antigen...")
                    
                    # First charge: consultation fee
                    typeText("consultation fee")
                    time.sleep(1)
                    pyautogui.click(283, 231)
                    time.sleep(1)  # Increased delay
                    
                    # Check stop flag before second charge
                    if self.stop_automation_flag:
                        raise KeyboardInterrupt("Stopped by ESC key")
                    
                    # Second charge: antigen
                    print("Adding second charge (antigen)...")
                    
                    pyautogui.click(592, 153)
                    time.sleep(1)
                    pyautogui.hotkey('ctrl', 'a')  # Select all text in the input field
                    time.sleep(0.5)  # Short delay to ensure selection
                    
                    typeText("( won")
                    time.sleep(1)
                    pyautogui.click(283, 231)
                    time.sleep(1)
                    
                    pyautogui.press('enter')
                    time.sleep(1)
                    print("Consultation fee and antigen added successfully")

                    time.sleep(1)  # Increased delay
                    finalStep()
                    print("Final step completed successfully")
                    return
                
                # If no matching condition, don't add any charges
                else:
                    print(f"No charging rule found for '{notes_remarks}', skipping charges...")
                    return
                    
            except KeyboardInterrupt as e:
                if "ESC" in str(e):
                    print("Charging services interrupted by user (ESC key)")
                else:
                    print("Charging services interrupted by user (Ctrl+C)")
                raise  # Re-raise to be handled by the main automation function
                
            except Exception as e:
                print(f"Error in charging services: {e}")
                print("Continuing with automation despite charging services error...")
                return


            

        def main():
            try:
                print("Starting automated registration in 2 seconds...")
                print("Press 'ESC' to attempt to stop automation.")
                time.sleep(CONFIG['startUpDelay'])
                # --- Check stop flag ---
                if self.stop_automation_flag: raise KeyboardInterrupt("Stopped by ESC key")
                # --- End Check stop flag ---
                print("Step 1: Opening new window")
                pyautogui.hotkey('ctrl', 'n')
                time.sleep(0.5)
                # --- Check stop flag ---
                if self.stop_automation_flag: raise KeyboardInterrupt("Stopped by ESC key")
                # --- End Check stop flag ---
                print("Step 2: Navigating initial fields")
                pressTabMultiple(2)
                pyautogui.press('enter')
                pressTabMultiple(2)
                print("Step 3: Entering ID Number")
                typeText(DETAILS['idNumber'])
                pyautogui.press('tab')
                wait()
                print("Step 4: Navigating form fields")
                pressTabMultiple(2, 0.2)
                pyautogui.press('enter')

                                # --- Check stop flag ---
                if self.stop_automation_flag: raise KeyboardInterrupt("Stopped by ESC key")
                # --- End Check stop flag ---
                # --- SIGNIFICANT DELAY - Increase if necessary ---
                print("Waiting for application to respond after ID entry... (6 seconds)")
                time.sleep(1.5) # Try increasing this to 3, 4, or 5 seconds
                # --- END DELAY ---
                # --- Debug: Print current directory and check if files exist ---
                #import os
                current_dir = os.getcwd()
                print(f"Current working directory: {current_dir}")
                for img_file in ['noRecordFound.png', 'outpatientRegistrationForm.png', 'withOutstandingBalance.png', 'useExistingRecord.png']:
                    if os.path.exists(os.path.join(current_dir, img_file)):
                        print(f"Found image file: {img_file}")
                    else:
                        print(f"WARNING: Image file NOT found: {img_file}")
                # --- End Debug ---

                # Add this function if it doesn't exist in your class


                # Replace the image detection section in your main() function with this improved version:
                try:
                    # Note: These image files need to exist in your script's directory
                    # Using lower confidence (0.8) for more reliable detection
                    print("Attempting to locate images on screen...")
                    
                    # Check each image individually with proper error handling
                    noRecordFoundLoc = None
                    outpatientRegistrationFormLoc = None
                    withOutstandingBalanceLoc = None
                    useExistingRecordLoc = None

                    try:
                        useExistingRecordLoc = pyautogui.locateOnScreen('useExistingRecord.png', confidence=0.8)
                        print("Found 'Use Existing Record' image")
                    except pyautogui.ImageNotFoundException:
                        print("'Use Existing Record' image not detected")
                    except Exception as e:
                        print(f"Error searching for 'Use Existing Record': {e}")
                    
                    try:
                        noRecordFoundLoc = pyautogui.locateOnScreen('noRecordFound.png', confidence=0.8)
                        print("Found 'No Record Found' image")
                    except pyautogui.ImageNotFoundException:
                        print("'No Record Found' image not detected")
                    except Exception as e:
                        print(f"Error searching for 'No Record Found': {e}")
                    
                    try:
                        outpatientRegistrationFormLoc = pyautogui.locateOnScreen('outpatientRegistrationForm.png', confidence=0.8)
                        print("Found 'Outpatient Registration Form' image")
                    except pyautogui.ImageNotFoundException:
                        print("'Outpatient Registration Form' image not detected")
                    except Exception as e:
                        print(f"Error searching for 'Outpatient Registration Form': {e}")
                    
                    try:
                        withOutstandingBalanceLoc = pyautogui.locateOnScreen('withOutstandingBalance.png', confidence=0.8)
                        print("Found 'With Outstanding Balance' image")
                    except pyautogui.ImageNotFoundException:
                        print("'With Outstanding Balance' image not detected")
                    except Exception as e:
                        print(f"Error searching for 'With Outstanding Balance': {e}")
                    
                    print("Image search completed.")

                    # Check for each image and act (in priority order)
                    # Priority 1: No record found - highest priority
                    if noRecordFoundLoc:
                        print("No Record found!")
                        print(f"Image located at: {noRecordFoundLoc}")
                        cancelOperation()
                        return # Stop processing this entry
                    
                    # Priority 2: Use existing record
                    elif useExistingRecordLoc:
                        print("Use Existing Record found!")
                        print(f"Image located at: {useExistingRecordLoc}")
                        
                        # First, use the existing record
                        useExistingRecord()
                        
                        # Wait for the screen to update after using existing record
                        print("Waiting for screen to update after using existing record...")
                        time.sleep(2)
                        
                        # Now check for outstanding balance AFTER using existing record
                        try:
                            print("Checking for outstanding balance after using existing record...")
                            withOutstandingBalanceLocAfter = pyautogui.locateOnScreen('withOutstandingBalance.png', confidence=0.8)
                            if withOutstandingBalanceLocAfter:
                                print("With outstanding balance found after using existing record!")
                                print(f"Image located at: {withOutstandingBalanceLocAfter}")
                                withOutstandingBalanceProceed()
                                time.sleep(1)
                            else:
                                print("No outstanding balance after using existing record")
                        except Exception as e:
                            print(f"Error checking for outstanding balance after existing record: {e}")
                        
                        # Finally, continue with form registration
                        print("Continuing with form registration after using existing record...")
                        continueFormRegistaration()
                        time.sleep(4)
                        chargingServices()
                        return
                    
                    # Priority 3: Outstanding balance (without existing record)
                    elif withOutstandingBalanceLoc:
                        time.sleep(1)  # Wait a bit before clicking
                        print("With outstanding balance!")
                        print(f"Image located at: {withOutstandingBalanceLoc}")
                        withOutstandingBalanceProceed()
                        time.sleep(1) # Give time after clicking proceed
                        continueFormRegistaration()
                        time.sleep(4)
                        chargingServices()
                        return
                    
                    # Priority 4: Normal registration form
                    elif outpatientRegistrationFormLoc:
                        print("Outpatient Registration Form")
                        print(f"Image located at: {outpatientRegistrationFormLoc}")
                        continueFormRegistaration()
                        time.sleep(4)
                        chargingServices()
                        return
                    
                    else:
                        # If none of the expected images were found
                        print("None of the expected state images were found on the screen.")
                        print("This might mean:")
                        print("1. The application is still loading")
                        print("2. The screen looks different than expected")
                        print("3. The image files don't match the current screen")
                        
                        # Optional: Add a small delay and try again
                        print("Waiting 2 more seconds and trying again...")
                        time.sleep(2)
                        
                        # Try one more time with even lower confidence
                        try:
                            noRecordFoundLoc = pyautogui.locateOnScreen('noRecordFound.png', confidence=0.7)
                            if noRecordFoundLoc:
                                print("Found 'No Record Found' on retry")
                                cancelOperation()
                                return
                        except:
                            pass
                        
                        try:
                            useExistingRecordLoc = pyautogui.locateOnScreen('useExistingRecord.png', confidence=0.7)
                            if useExistingRecordLoc:
                                print("Found 'Use Existing Record' on retry")
                                useExistingRecord()
                                time.sleep(3)
                                # Check for outstanding balance after retry
                                try:
                                    withOutstandingBalanceLocAfter = pyautogui.locateOnScreen('withOutstandingBalance.png', confidence=0.7)
                                    if withOutstandingBalanceLocAfter:
                                        withOutstandingBalanceProceed()
                                        time.sleep(1)
                                except:
                                    pass
                                continueFormRegistaration()
                                return
                        except:
                            pass
                            
                        try:
                            withOutstandingBalanceLoc = pyautogui.locateOnScreen('withOutstandingBalance.png', confidence=0.7)
                            if withOutstandingBalanceLoc:
                                print("Found 'With Outstanding Balance' on retry")
                                withOutstandingBalanceProceed()
                                time.sleep(1)
                                continueFormRegistaration()
                                return
                        except:
                            pass
                            
                        try:
                            outpatientRegistrationFormLoc = pyautogui.locateOnScreen('outpatientRegistrationForm.png', confidence=0.7)
                            if outpatientRegistrationFormLoc:
                                print("Found 'Outpatient Registration Form' on retry")
                                continueFormRegistaration()
                                return
                        except:
                            pass
                        
                        print("Still no images found. Proceeding with default form registration.")
                        continueFormRegistaration()
                        return

                except Exception as e:
                    print(f"Unexpected error during image detection: {type(e).__name__}: {e}")
                    print("Proceeding with default form registration.")
                    continueFormRegistaration()
                    return
            except pyautogui.FailSafeException:
                print("Automation stopped by user (mouse moved to corner).")
                self.is_batch_running = False # Stop batch if failsafe triggered
                self.buttons["startBatch"].config(state='normal')
                self.buttons["stopBatch"].config(state='disabled')
                # --- Signal stop for ESC listener ---
                self.listener_active = False
                # --- End Signal stop ---
            except KeyboardInterrupt as e: # Catch the custom exception
                if "ESC" in str(e):
                    print("Automation interrupted by user (ESC key).")
                else:
                    print("Automation interrupted by user (Ctrl+C).")
                self.is_batch_running = False
                self.buttons["startBatch"].config(state='normal')
                self.buttons["stopBatch"].config(state='disabled')
                # --- Signal stop for ESC listener ---
                self.listener_active = False
                # --- End Signal stop ---
            except Exception as e:
                print(f"An error occurred during automation: {e}")
                # Optionally stop batch on error
                # self.is_batch_running = False
                # self.buttons["startBatch"].config(state='normal')
                # self.buttons["stopBatch"].config(state='disabled')
                # --- Signal stop for ESC listener ---
                self.listener_active = False
                # --- End Signal stop ---
            finally:
                # Ensure listener is deactivated when main exits
                self.listener_active = False

        main()

if __name__ == "__main__":
    app = AutoGuiApp()
    app.mainloop()