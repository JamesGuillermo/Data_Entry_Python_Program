from tkinter import END, Listbox, filedialog, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import pyautogui
import time
import pandas as pd
from datetime import datetime
import os
import threading
import keyboard

class AutoGuiApp(tb.Window):
    def __init__(self):
        super().__init__(title="Auto GUI Application", themename="darkly")
        self.geometry("1700x1000")
        self.resizable(True, True)
        
        # UI Components
        self.labels = {}
        self.entries = {}
        self.buttons = {}
        self.listboxes = {}
        self.comboboxes = {}
        self.checkbuttons = {}
        
        # Layout configuration
        self.anchor = "w"
        self.labelPosX = 30
        self.entryPosX = 300
        
        # Excel and batch processing
        self.excel_data = None
        self.current_row_index = 0
        self.is_batch_running = False
        
        # Automation control
        self.stop_automation_flag = False
        self.listener_active = False
        self._listener_thread = None
        
        # PyAutoGUI configuration
        pyautogui.PAUSE = 0.1
        pyautogui.FAILSAFE = True
        
        self.create_widgets()

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
            command=command
        )
        checkbutton.place(anchor=checkAnchor, x=checkPosX, y=checkPosY)
        return checkbutton

    def create_widgets(self):
        # Mouse position and screen info
        self.labels['mousePosition'] = self.add_label("Mouse Position: ", "center", 850, 100, ("Arial", 16), "white")
        self.labels['screenSize'] = self.add_label(self.screenSize(), "center", 850, 150, ("Arial", 16), "white")
        
        # Form labels
        self.labels['idNumber'] = self.add_label("ID Number: ", self.anchor, self.labelPosX, 250, ("Arial", 14), "white")
        self.labels['registrationType'] = self.add_label("Registration Type: ", self.anchor, self.labelPosX, 300, ("Arial", 14), "white")
        self.labels['transactionType'] = self.add_label("Transaction Type: ", self.anchor, self.labelPosX, 350, ("Arial", 14), "white")
        self.labels['serviceType'] = self.add_label("Service Type: ", self.anchor, self.labelPosX, 400, ("Arial", 14), "white")
        self.labels['companyName'] = self.add_label("Company Name: ", self.anchor, self.labelPosX, 450, ("Arial", 14), "white")
        self.labels['notesRemarks'] = self.add_label("Notes/Remarks: ", self.anchor, self.labelPosX, 500, ("Arial", 14), "white")

        # Form entries and comboboxes
        self.entries['idNumber'] = self.add_entry(self.anchor, self.entryPosX, 250, 50, ("Arial", 12))
        # Bind event to auto-set company when ID number changes
        self.entries['idNumber'].bind('<KeyRelease>', self.on_id_number_change)
        self.entries['idNumber'].bind('<FocusOut>', self.on_id_number_change)

        self.comboboxes['registrationType'] = self.add_combobox(
            self.anchor, self.entryPosX, 300, 50, 12,
            ["Consult", "FF Consult", "FTW", "Pre-Emp", "FF Pre-Emp", "Travel Clearance", "APE", "FF APE", "Lab request", "ftp"],
            state="readonly"
        )
        self.comboboxes['registrationType'].bind("<<ComboboxSelected>>", self.on_registration_type_change)

        self.comboboxes['transactionType'] = self.add_combobox(
            self.anchor, self.entryPosX, 350, 50, 12,
            ["consultation", "follow-up consultation", "fit to work", "pre-employment", "for entry", "annual physical examination", "laboratory", "fit to play"],
            state="readonly"
        )
        
        self.comboboxes['serviceType'] = self.add_combobox(
            self.anchor, self.entryPosX, 400, 50, 12,
            ["consultation", "clearance", "pre-employment", "annual physical examination", "laboratory", "tele-consult"],
            state="readonly"
        )
        
        self.comboboxes['companyName'] = self.add_combobox(
            self.anchor, self.entryPosX, 450, 50, 12,
            ["elixer", "philippine batteries inc", "ramcar technology inc", "evergreen", "sta. maria", "firstcore", "topspot", "poultrymax", "northpoint", "nutriforyou", "quantus", "san rafael", "subic"],
            state="readonly"
        )
        
        self.comboboxes['notesRemarks'] = self.add_combobox(
            self.anchor, self.entryPosX, 500, 50, 12,
            ["ape AM", "ape AF", "ape BM", "ape BF", "fc, consult", "fc, ff consult", "fc, consult, antigen", "fc, ftw", "lab req", "teleconsult", "fc, ff ape", "ftp"],
            state="normal"
        )

        # Excel file selection
        self.labels['excelFile'] = self.add_label("Excel File: ", self.anchor, self.labelPosX, 600, ("Arial", 14), "white")
        self.entries['excelFile'] = self.add_entry(self.anchor, self.entryPosX, 600, 50, ("Arial", 12))
        self.entries['excelFile'].config(state='readonly')
        self.buttons["browseExcel"] = self.add_button(
            self.anchor, self.entryPosX + 450, 600, "Browse...", self.browse_excel_file
        )

        # Control buttons
        self.buttons["startAutomation"] = self.add_button(
            self.anchor, self.entryPosX, 550, "Start Automation (Single)", self.automated_registration
        )
        self.buttons["startBatch"] = self.add_button(
            self.anchor, self.entryPosX, 650, "Start Automation (Batch)", self.start_batch_process
        )
        self.buttons["stopBatch"] = self.add_button(
            self.anchor, self.entryPosX + 200, 650, "Stop Batch", self.stop_batch_process
        )
        self.buttons["stopBatch"].config(state='disabled')
        
        self.buttons["saveEntry"] = self.add_button(
            self.anchor, self.entryPosX, 700, "Save Entry to Excel", self.save_entry_to_excel
        )

        # Auto remarks checkbuttons
        self.auto_remarks_vars = {
            'AM': tb.BooleanVar(value=False),
            'AF': tb.BooleanVar(value=False),
            'BM': tb.BooleanVar(value=False),
            'BF': tb.BooleanVar(value=False)
        }
        
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

        # Status label
        self.status_label = tb.Label(self, text="Ready", font=("Arial", 16), bootstyle="info")
        self.status_label.pack(pady=20)

        self.update_mouse_position()

    def get_mouse_position(self):
        try:
            x, y = pyautogui.position()
            r, g, b = pyautogui.pixel(x, y)
            return f"Mouse: ({x}, {y}) | Color: ({r}, {g}, {b})"
        except Exception as e:
            return f"Error reading pixel: {e}"

    def update_mouse_position(self):
        position_text = self.get_mouse_position()
        self.labels['mousePosition'].config(text=position_text)
        self.status_label.config(text=position_text)
        self.after(100, self.update_mouse_position)

    def screenSize(self):
        width, height = pyautogui.size()
        return f"Screen Size: {width}x{height}"

    def id_number_format(self, id_number):
        """Determine company based on ID number format"""
        if not id_number:
            return None
            
        id_number = str(id_number).strip()
        
        # Handle empty string after stripping
        if not id_number:
            return None
            
        id_number_length = len(id_number)
        
        # Define prefixes for different companies
        id_elixer_prefix = ['601', '602', '603', '604', '605', '606', '607', '608', '609']
        id_first_core_prefix = ['F1', 'F2', 'f1', 'f2']  # Added lowercase variants
        id_philippine_batteries_inc_prefix = ['1000', '5700']
        id_ramcar_technology_inc_prefix = ['4000']
        id_evergreen_prefix = ['6000']
        id_sta_maria_prefix = ['6800']

        # Convert to uppercase for case-insensitive comparison with letter prefixes
        id_number_upper = id_number.upper()

        if id_number_length == 7:
            if id_number.startswith(tuple(id_elixer_prefix)):
                return "elixer"
        elif id_number_length == 8:
            if id_number_upper.startswith(tuple(prefix.upper() for prefix in id_first_core_prefix)):
                return "firstcore"
            elif id_number.startswith(tuple(id_philippine_batteries_inc_prefix)):
                return "philippine batteries inc"
            elif id_number.startswith(tuple(id_ramcar_technology_inc_prefix)):
                return "ramcar technology inc"
            elif id_number.startswith(tuple(id_evergreen_prefix)):
                return "evergreen"
            elif id_number.startswith(tuple(id_sta_maria_prefix)):
                return "sta. maria"
        
        # Return None if no match found - let user choose manually
        return None

    def on_id_number_change(self, event=None):
        """Event handler for ID number changes - auto-sets company"""
        id_number = self.entries['idNumber'].get().strip()
        if id_number:
            company = self.id_number_format(id_number)
            if company:
                # Set the company in the combobox
                self.comboboxes['companyName'].set(company)
                print(f"Auto-set company to: {company} for ID: {id_number}")
            # If company is None, don't change the current selection

    def on_registration_type_change(self, event=None):
        """Event handler for registration type changes"""
        self.registration_type_dependent()

    def update_notes_remarks(self):
        """Update Notes/Remarks based on selected checkboxes"""
        selected = []
        for key, var in self.auto_remarks_vars.items():
            if var.get():
                selected.append(f"ape {key}")
        
        notes = ", ".join(selected) if selected else ""
        self.comboboxes['notesRemarks'].set(notes)

    def registration_type_dependent(self):
        """Update dependent comboboxes based on registration type"""
        try:
            selected_value = self.comboboxes['registrationType'].get()
            
            # Mapping for registration types
            type_mappings = {
                "Consult": {
                    "transactionType": "consultation",
                    "serviceType": "consultation",
                    "notesRemarks": "fc, consult"
                },
                "FF Consult": {
                    "transactionType": "follow-up consultation",
                    "serviceType": "consultation",
                    "notesRemarks": "fc, ff consult"
                },
                "FTW": {
                    "transactionType": "fit to work",
                    "serviceType": "clearance",
                    "notesRemarks": "fc, ftw"
                },
                "Pre-Emp": {
                    "transactionType": "pre-employment",
                    "serviceType": "pre-employment",
                    "notesRemarks": ""
                },
                "FF Pre-Emp": {
                    "transactionType": "follow-up consultation",
                    "serviceType": "pre-employment",
                    "notesRemarks": "fc, ff pre-employment"
                },
                "Travel Clearance": {
                    "transactionType": "for entry",
                    "serviceType": "clearance",
                    "notesRemarks": "fc, travel clearance"
                },
                "APE": {
                    "transactionType": "annual physical examination",
                    "serviceType": "annual physical examination",
                    "notesRemarks": ""
                },
                "FF APE": {
                    "transactionType": "annual physical examination",
                    "serviceType": "annual physical examination",
                    "notesRemarks": "fc, ff ape"
                },
                "Lab request": {
                    "transactionType": "laboratory",
                    "serviceType": "laboratory",
                    "notesRemarks": "lab req"
                },
                "ftp": {
                    "transactionType": "fit to play",
                    "serviceType": "clearance",
                    "notesRemarks": "ftp"
                },
            }
            
            if selected_value in type_mappings:
                mapping = type_mappings[selected_value]
                self.comboboxes['transactionType'].set(mapping["transactionType"])
                self.comboboxes['serviceType'].set(mapping["serviceType"])
                
                # Only set notes if no checkboxes are selected
                if not any(var.get() for var in self.auto_remarks_vars.values()):
                    self.comboboxes['notesRemarks'].set(mapping["notesRemarks"])
                    
        except Exception as e:
            print(f"Error in registration_type_dependent: {e}")

    def save_entry_to_excel(self):
        """Appends the current GUI data as a new row to the selected Excel file."""
        file_path = self.entries['excelFile'].get()
        if not file_path:
            messagebox.showerror("Error", "Please select an Excel file first.")
            return
            
        # Validate required fields
        if not self.entries['idNumber'].get().strip():
            messagebox.showerror("Error", "ID Number is required.")
            return
            
        new_data = {
            "ID Number": self.entries['idNumber'].get().strip(),
            "Registration Type": self.comboboxes['registrationType'].get(),
            "Transaction Type": self.comboboxes['transactionType'].get(),
            "Service Type": self.comboboxes['serviceType'].get(),
            "Company Name": self.comboboxes['companyName'].get(),
            "Notes/Remarks": self.comboboxes['notesRemarks'].get()
        }
        
        new_row_df = pd.DataFrame([new_data])
        
        try:
            if os.path.exists(file_path):
                existing_df = pd.read_excel(file_path)
                updated_df = pd.concat([existing_df, new_row_df], ignore_index=True)
            else:
                updated_df = new_row_df
                
            updated_df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", "Data saved to Excel file successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save to Excel file:\n{e}")

    def browse_excel_file(self):
        """Open file dialog to select Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=(("Excel Files", "*.xlsx *.xls"), ("All Files", "*.*"))
        )
        if file_path:
            self.entries['excelFile'].config(state='normal')
            self.entries['excelFile'].delete(0, END)
            self.entries['excelFile'].insert(0, file_path)
            self.entries['excelFile'].config(state='readonly')

    def load_excel_data(self):
        """Load data from the selected Excel file"""
        file_path = self.entries['excelFile'].get()
        if not file_path:
            messagebox.showerror("Error", "Please select an Excel file first.")
            return False
            
        try:
            self.excel_data = pd.read_excel(file_path)
            required_columns = ['ID Number', 'Registration Type', 'Transaction Type', 'Service Type', 'Company Name', 'Notes/Remarks']
            
            missing_columns = [col for col in required_columns if col not in self.excel_data.columns]
            if missing_columns:
                messagebox.showerror("Error", f"Missing columns in Excel file: {missing_columns}")
                self.excel_data = None
                return False
                
            # Remove rows with empty ID numbers
            self.excel_data = self.excel_data.dropna(subset=['ID Number'])
            self.excel_data = self.excel_data[self.excel_data['ID Number'].astype(str).str.strip() != '']
            
            if self.excel_data.empty:
                messagebox.showerror("Error", "No valid data found in Excel file.")
                return False
                
            self.current_row_index = 0
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
            return
            
        self.is_batch_running = True
        self.buttons["startBatch"].config(state='disabled')
        self.buttons["stopBatch"].config(state='normal')
        
        messagebox.showinfo("Info", f"Batch process started for {len(self.excel_data)} entries.\nPress 'ESC' to stop.")
        
        # Start ESC listener
        self.stop_automation_flag = False
        self.listener_active = True
        self.start_escape_listener()
        
        # Start processing first row
        self.process_next_row()

    def stop_batch_process(self):
        """Stop the batch process"""
        if self.is_batch_running:
            self.is_batch_running = False
            self.stop_automation_flag = True
            self.listener_active = False
            self.buttons["startBatch"].config(state='normal')
            self.buttons["stopBatch"].config(state='disabled')
            messagebox.showinfo("Info", "Batch process stopped.")

    def start_escape_listener(self):
        """Starts a thread to listen for the Escape key."""
        def listen_for_escape():
            try:
                keyboard.wait('esc')
                if self.listener_active:
                    print("ESC key pressed. Stopping automation.")
                    self.stop_automation_flag = True
                    # Trigger failsafe
                    try:
                        pyautogui.moveTo(0, 0)
                    except:
                        pass
            except Exception as e:
                print(f"Error in escape listener: {e}")

        # Check if listener thread exists and is alive
        if hasattr(self, '_listener_thread') and self._listener_thread is not None and self._listener_thread.is_alive():
            print("Listener thread already active.")
            return
            
        self._listener_thread = threading.Thread(target=listen_for_escape, daemon=True)
        self._listener_thread.start()

    def process_next_row(self):
        """Process the next row from the loaded Excel data"""
        if self.stop_automation_flag or not self.is_batch_running:
            self.finish_batch()
            return
            
        if self.current_row_index < len(self.excel_data):
            row = self.excel_data.iloc[self.current_row_index]
            
            details = {
                "idNumber": str(row['ID Number']).strip(),
                "registrationType": str(row['Registration Type']).strip(),
                "transactionType": str(row['Transaction Type']).strip(),
                "serviceType": str(row['Service Type']).strip(),
                "companyName": str(row['Company Name']).strip(),
                "notesRemarks": str(row['Notes/Remarks']).strip()
            }
            
            print(f"Processing Row {self.current_row_index + 1}/{len(self.excel_data)}: ID {details['idNumber']}")
            
            try:
                self.run_automation(details)
                self.current_row_index += 1
                # Schedule next row processing
                self.after(3000, self.process_next_row)  # 3 second delay between entries
            except Exception as e:
                print(f"Error processing row {self.current_row_index + 1}: {e}")
                self.current_row_index += 1
                self.after(2000, self.process_next_row)  # Continue with next row after error
        else:
            self.finish_batch()


    def finish_batch(self):
        """Called when all rows are processed or batch is stopped"""
        self.is_batch_running = False
        self.listener_active = False
        self.buttons["startBatch"].config(state='normal')
        self.buttons["stopBatch"].config(state='disabled')
        
        if self.current_row_index >= len(self.excel_data):
            messagebox.showinfo("Success", f"Batch automation completed! Processed {self.current_row_index} entries.")
        else:
            messagebox.showinfo("Info", f"Batch automation stopped. Processed {self.current_row_index} out of {len(self.excel_data)} entries.")

    def automated_registration(self):
        """Handles single manual run using GUI inputs"""
        if self.is_batch_running:
            messagebox.showwarning("Warning", "Batch process is running. Please wait or stop it.")
            return
            
        # Validate input
        if not self.entries['idNumber'].get().strip():
            messagebox.showerror("Error", "ID Number is required.")
            return

        details = {
            "idNumber": self.entries['idNumber'].get().strip(),
            "registrationType": self.comboboxes['registrationType'].get(),
            "transactionType": self.comboboxes['transactionType'].get(),
            "serviceType": self.comboboxes['serviceType'].get(),
            "companyName": self.comboboxes['companyName'].get(),
            "notesRemarks": self.comboboxes['notesRemarks'].get()
        }
        
        self.stop_automation_flag = False
        self.listener_active = True
        self.start_escape_listener()
        
        try:
            self.run_automation(details)
        finally:
            self.listener_active = False

    def run_automation(self, details):
        """Core automation logic"""
        print(f"Starting automation for ID: {details['idNumber']}")
        
        # Automation coordinates and configuration
        coordinates = {
            'xy1': (237, 890), 'xy2': (268, 881), 'xy3': (591, 182),
            'xy4': (215, 893), 'xy5': (249, 927), 'xy6': (561, 184),
            'xy7': (239, 966), 'transactionTypeLoc': (490, 582),
            'serviceTypeLoc': (925, 478), 'asdLoc': (260, 881),
            'asdLoc2': (592, 184), 'companyNameLoc': (265, 918),
            'companyNameLoc2': (611, 184), 'notesRemarksLoc': (269, 962),
        }
        
        config = {
            'defaultDelay': 0.1, 'tabDelay': 0.1,
            'moveDelay': 0.5, 'startUpDelay': 2
        }

        def safe_wait(duration=None):
            if self.stop_automation_flag:
                raise KeyboardInterrupt("Stopped by ESC key")
            time.sleep(duration or config['defaultDelay'])

        def press_tab_multiple(count, delay=None):
            for _ in range(count):
                if self.stop_automation_flag:
                    raise KeyboardInterrupt("Stopped by ESC key")
                pyautogui.press('tab')
                safe_wait(delay or config['tabDelay'])

        def click_at(coord_key, clicks=1):
            if self.stop_automation_flag:
                raise KeyboardInterrupt("Stopped by ESC key")
            if coord_key in coordinates:
                x, y = coordinates[coord_key]
                pyautogui.moveTo(x, y, duration=config['moveDelay'])
                for _ in range(clicks):
                    pyautogui.click()
                    if self.stop_automation_flag:
                        raise KeyboardInterrupt("Stopped by ESC key")

        def type_text(text, delay=None):
            if self.stop_automation_flag:
                raise KeyboardInterrupt("Stopped by ESC key")
            if text:
                # Handle numeric IDs that might be floats
                if isinstance(text, float) and text.is_integer():
                    text = str(int(text))
                elif not isinstance(text, str):
                    text = str(text)
                pyautogui.write(text, interval=delay or config['defaultDelay'])

        def continue_form_registration():
            try:
                print("Continuing with form registration...")
                safe_wait(0.2)
                
                # Transaction type
                click_at('transactionTypeLoc')
                safe_wait(0.2)
                type_text(details['transactionType'])
                
                # Service type
                press_tab_multiple(4)
                safe_wait(0.1)
                type_text(details['serviceType'])
                
                # Assign physician
                click_at('asdLoc', clicks=2)
                safe_wait(0.2)
                type_text("asd")
                pyautogui.press("enter")
                
                click_at('asdLoc2', clicks=2)
                safe_wait(0.2)
                
                # Company name
                click_at('companyNameLoc', clicks=2)
                safe_wait(0.2)
                type_text(details['companyName'])
                pyautogui.press("enter")
                
                click_at('companyNameLoc2', clicks=2)
                safe_wait(0.2)
                
                # Notes/remarks
                click_at('notesRemarksLoc', clicks=1)
                safe_wait(0.2)
                press_tab_multiple(1)
                type_text(details['notesRemarks'])
                press_tab_multiple(1)
                pyautogui.press('enter')
                type_text("1")
                press_tab_multiple(3)
                pyautogui.press('enter')
                
                print("Form registration completed successfully!")
                
            except Exception as e:
                print(f"Error in form registration: {e}")
                raise

        def handle_charging_services():
            try:
                print("Starting charging services...")
                pyautogui.click(1671, 564)
                safe_wait(1)
                
                type_text("nu")
                safe_wait(1)
                
                pyautogui.click(575, 187)
                pyautogui.click(575, 187)
                safe_wait(3)
                
                pyautogui.click(349, 859)
                safe_wait(1)
                pyautogui.click(592, 153)
                safe_wait(1)
                
                notes_remarks = details['notesRemarks']
                
                def final_step():
                    pyautogui.click(1473, 1010)
                    safe_wait(1)
                    type_text("1")
                    pyautogui.press('enter')
                    pyautogui.click(1117,548)
                    safe_wait(.5)
                    pyautogui.press('enter')
                
                # Handle different charge types
                consultation_charges = ["fc, consult", "fc, ff consult", "fc, ff pre-employment", "fc, ftw", "fc, ff ape","ftp"]
                antigen_charges = ["fc, consult, antigen", "fc, ftw, antigen"]
                
                if notes_remarks in consultation_charges:
                    type_text("consultation fee")
                    safe_wait(1)
                    pyautogui.click(283, 231)
                    safe_wait(1)
                    pyautogui.press('enter')
                    final_step()
                    safe_wait(0.5)
                    pyautogui.press('enter')

                    
                elif notes_remarks in antigen_charges:
                    # First charge: consultation fee
                    type_text("consultation fee")
                    safe_wait(1)
                    pyautogui.click(283, 231)
                    safe_wait(1)
                    
                    # Second charge: antigen
                    pyautogui.click(592, 153)
                    safe_wait(1)
                    pyautogui.hotkey('ctrl', 'a')
                    safe_wait(0.5)
                    type_text("( won")
                    safe_wait(1)
                    pyautogui.click(283, 231)
                    safe_wait(1)
                    pyautogui.press('enter')
                    final_step()
                    safe_wait(0.5)
                    pyautogui.press('enter')
                
                print("Charging services completed successfully!")
                
            except Exception as e:
                print(f"Error in charging services: {e}")

        # Main automation sequence
        try:
            print(f"Starting automated registration for ID: {details['idNumber']}")
            safe_wait(config['startUpDelay'])
            
            # Open new window
            pyautogui.hotkey('ctrl', 'n')
            safe_wait(0.5)
            
            # Navigate and enter ID
            press_tab_multiple(2)
            pyautogui.press('enter')
            press_tab_multiple(2)
            type_text(details['idNumber'])
            pyautogui.press('tab')
            safe_wait()
            press_tab_multiple(2, 0.2)
            pyautogui.press('enter')
            
            # Wait for system response
            print("Waiting for system response...")
            safe_wait(2)
            
            # Image detection and flow control
            try:
                # Check for different system states
                image_files = ['noRecordFound.png', 'useExistingRecord.png', 'withOutstandingBalance.png', 'outpatientRegistrationForm.png']
                found_images = {}
                
                for img_file in image_files:
                    try:
                        if os.path.exists(img_file):
                            location = pyautogui.locateOnScreen(img_file, confidence=0.8)
                            if location:
                                found_images[img_file] = location
                                print(f"Found {img_file} at {location}")
                    except pyautogui.ImageNotFoundException:
                        continue
                    except Exception as e:
                        print(f"Error checking {img_file}: {e}")
                
                # Handle different scenarios based on found images
                if 'noRecordFound.png' in found_images:
                    print("No record found - cancelling operation")
                    pyautogui.moveTo(0, 0)  # Trigger failsafe
                    return
                    
                elif 'useExistingRecord.png' in found_images:
                    print("Using existing record")
                    press_tab_multiple(1)
                    pyautogui.press('enter')
                    safe_wait(2)
                    
                    # Check for outstanding balance after using existing record
                    try:
                        balance_location = pyautogui.locateOnScreen('withOutstandingBalance.png', confidence=0.8)
                        if balance_location:
                            print("Outstanding balance found after existing record")
                            pyautogui.click(924, 641)
                            press_tab_multiple(1)
                            pyautogui.press('enter')
                            safe_wait(1)
                    except:
                        pass
                    
                    continue_form_registration()
                    safe_wait(4)
                    handle_charging_services()
                    return
                    
                elif 'withOutstandingBalance.png' in found_images:
                    print("Outstanding balance detected")
                    pyautogui.click(924, 641)
                    press_tab_multiple(1)
                    pyautogui.press('enter')
                    safe_wait(1)
                    continue_form_registration()
                    safe_wait(4)
                    handle_charging_services()
                    return
                    
                elif 'outpatientRegistrationForm.png' in found_images:
                    print("Outpatient registration form detected")
                    continue_form_registration()
                    safe_wait(4)
                    handle_charging_services()
                    return
                    
                else:
                    print("No recognized state found - proceeding with default registration")
                    safe_wait(2)
                    
                    # Try one more time with lower confidence
                    try:
                        for img_file in image_files:
                            if os.path.exists(img_file):
                                location = pyautogui.locateOnScreen(img_file, confidence=0.7)
                                if location:
                                    print(f"Found {img_file} on retry")
                                    if 'noRecordFound' in img_file:
                                        pyautogui.moveTo(0, 0)
                                        return
                                    elif 'useExistingRecord' in img_file:
                                        press_tab_multiple(1)
                                        pyautogui.press('enter')
                                        safe_wait(3)
                                    elif 'withOutstandingBalance' in img_file:
                                        pyautogui.click(924, 641)
                                        press_tab_multiple(1)
                                        pyautogui.press('enter')
                                        safe_wait(1)
                                    break
                    except:
                        pass
                    
                    continue_form_registration()
                    safe_wait(4)
                    handle_charging_services()
                    
            except Exception as e:
                print(f"Error in image detection: {e}")
                print("Proceeding with default registration")
                continue_form_registration()
                safe_wait(4)
                handle_charging_services()
                
        except pyautogui.FailSafeException:
            print("Automation stopped by failsafe (mouse moved to corner)")
            self.stop_batch_if_running()
            
        except KeyboardInterrupt as e:
            print(f"Automation interrupted: {e}")
            self.stop_batch_if_running()
            
        except Exception as e:
            print(f"Unexpected error in automation: {e}")
            # Continue with batch processing even if one entry fails
            
        finally:
            self.listener_active = False
            print(f"Automation completed for ID: {details['idNumber']}")

    def stop_batch_if_running(self):
        """Helper method to stop batch processing"""
        if self.is_batch_running:
            self.is_batch_running = False
            self.buttons["startBatch"].config(state='normal')
            self.buttons["stopBatch"].config(state='disabled')
            self.listener_active = False

if __name__ == "__main__":
    app = AutoGuiApp()
    app.mainloop()