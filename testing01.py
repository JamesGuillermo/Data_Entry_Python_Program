import ttkbootstrap as tb
import pyautogui
import sqlite3
import json
import uuid

class AutoGuiApp(tb.Window):
    def __init__(self):
        super().__init__(title="Auto GUI Application", themename="darkly")
        self.geometry("1700x1000")
        self.resizable(True, True)
        self.labels = {}
        self.buttons = {}
        self.functions = {}
        self.function_counter = 0

        self.create_widgets()

        # Initialize database
        self.accessingDatabaseOfFunctions(
            "functions.db", "create", "functions_table",
            ["id INTEGER PRIMARY KEY AUTOINCREMENT", "name TEXT", "function_data TEXT"],
            []
        )

    def create_widgets(self):
        # Example of adding a label
        self.labels['example'] = self.add_label(
            "Example Label", "w", 100, 100, ("Arial", 16), "white"
        )
        
        # Example of adding a button that executes and saves function
        self.buttons['example_button'] = self.add_button(
            "w", 100, 150, "Execute & Save Function", self.on_button_click_and_save
        )
        
        # Button to save current function to database
        self.buttons['save_function'] = self.add_button(
            "w", 300, 150, "Save Function to DB", self.save_current_function
        )
        
        # Button to load all functions from database
        self.buttons['load_functions'] = self.add_button(
            "w", 500, 150, "Load All Functions", self.load_all_functions
        )
        
        # Status label
        self.labels['status'] = self.add_label(
            "Ready", "w", 100, 50, ("Arial", 12), "yellow"
        )
    
    def on_button_click(self):
        """Handle button click event"""
        print("Button clicked!")
        # Example action: Move mouse to a specific position
        pyautogui.moveTo(200, 200, duration=0.5)

        self.function_counter += 1
        function_name = f"function_{self.function_counter}"
        
        # Create a label showing function execution
        label = self.add_label(
            f"Function {self.function_counter} executed", 
            "w", 100, 200 + (self.function_counter - 1) * 30, 
            ("Arial", 12), "green"
        )
        
        # Store function data
        self.functions[function_name] = {
            'name': function_name,
            'action': 'move_mouse',
            'parameters': {'x': 200, 'y': 200, 'duration': 0.5},
            'label_text': f"Function {self.function_counter} executed",
            'label_position': {'x': 100, 'y': 200 + (self.function_counter - 1) * 30}
        }
        
        return function_name
    
    def on_button_click_and_save(self):
        """Execute function and automatically save to database"""
        function_name = self.on_button_click()
        self.save_function_to_database(function_name)
        self.update_status(f"Function {function_name} executed and saved!")
    
    def save_current_function(self):
        """Save the most recent function to database"""
        if self.functions:
            latest_function = list(self.functions.keys())[-1]
            self.save_function_to_database(latest_function)
            self.update_status(f"Function {latest_function} saved to database!")
        else:
            self.update_status("No functions to save!")
    
    def save_function_to_database(self, function_name):
        """Save a specific function to the database"""
        if function_name in self.functions:
            function_data = self.functions[function_name]
            
            # Convert function data to JSON string for storage
            function_json = json.dumps(function_data)
            
            # Save to database
            self.savingFunctionsToDatabase(
                "functions.db", 
                "functions_table", 
                ["name", "function_data"],
                [function_name, function_json]
            )
            print(f"Saved function {function_name} to database")
    
    def load_all_functions(self):
        """Load all functions from database and display them"""
        try:
            # Get all functions from database
            functions_data = self.accessingDatabaseOfFunctionsToGet(
                "functions.db", "functions_table", ["name", "function_data"]
            )
            
            if not functions_data:
                self.update_status("No functions found in database!")
                return
            
            # Clear existing loaded function labels
            self.clear_loaded_functions()
            
            # Load and display each function
            y_offset = 300
            for name, function_json in functions_data:
                try:
                    function_data = json.loads(function_json)
                    
                    # Create label showing loaded function
                    loaded_label = self.add_label(
                        f"Loaded: {function_data.get('label_text', name)}", 
                        "w", 700, y_offset, 
                        ("Arial", 10), "cyan"
                    )
                    
                    # Create button to execute loaded function
                    execute_button = self.add_button(
                        "w", 900, y_offset, f"Execute {name}", 
                        lambda func_data=function_data, func_name=name: self.execute_loaded_function(func_data, func_name)
                    )
                    
                    y_offset += 35
                    
                except json.JSONDecodeError:
                    print(f"Error loading function {name}: Invalid JSON data")
            
            self.update_status(f"Loaded {len(functions_data)} functions from database!")
            
        except Exception as e:
            self.update_status(f"Error loading functions: {str(e)}")
    
    def execute_loaded_function(self, function_data, function_name):
        """Execute a loaded function"""
        try:
            action = function_data.get('action')
            parameters = function_data.get('parameters', {})
            
            if action == 'move_mouse':
                pyautogui.moveTo(
                    parameters.get('x', 200), 
                    parameters.get('y', 200), 
                    duration=parameters.get('duration', 0.5)
                )
                
                # Display execution confirmation
                self.add_label(
                    f"Executed loaded function: {function_name}", 
                    "w", 100, 400 + len(self.functions) * 20, 
                    ("Arial", 10), "orange"
                )
                
            self.update_status(f"Executed loaded function: {function_name}")
            
        except Exception as e:
            self.update_status(f"Error executing function: {str(e)}")
    
    def clear_loaded_functions(self):
        """Clear loaded function display elements"""
        # This is a simple implementation - in a more complex app, 
        # you'd want to track and properly remove specific widgets
        pass
    
    def update_status(self, message):
        """Update the status label"""
        if 'status' in self.labels:
            self.labels['status'].config(text=message)
        print(message)
    
    def accessingDatabaseOfFunctions(self, dbName, dbmode, dbTable, dbColumnNamesOrDefs, dbColumnValues):
        """Access a database and perform operations"""
        conn = sqlite3.connect(dbName)
        cursor = conn.cursor()
        
        try:
            if dbmode == "create":
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {dbTable} ({', '.join(dbColumnNamesOrDefs)})")
                conn.commit()
                print(f"Table {dbTable} created with columns: {dbColumnNamesOrDefs}")
            
            elif dbmode == "insert":
                placeholders = ', '.join(['?'] * len(dbColumnValues))
                cursor.execute(f"INSERT INTO {dbTable} (name, function_data) VALUES (?, ?)", dbColumnValues)
                conn.commit()
                print(f"Inserted values into {dbTable}: {dbColumnValues}")
            
            elif dbmode == "select":
                cursor.execute(f"SELECT * FROM {dbTable}")
                rows = cursor.fetchall()
                print(f"Data from {dbTable}: {rows}")
                return rows
        
        except Exception as e:
            print(f"Database error: {e}")
        
        finally:
            conn.close()
    
    def accessingDatabaseOfFunctionsToGet(self, dbName, dbTable, dbColumnNamesOrDefs):
        """Get data from a database"""
        conn = sqlite3.connect(dbName)
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"SELECT {', '.join(dbColumnNamesOrDefs)} FROM {dbTable}")
            rows = cursor.fetchall()
            return rows
        
        except Exception as e:
            print(f"Database error: {e}")
            return []
        
        finally:
            conn.close()

    def savingFunctionsToDatabase(self, dbName, dbTable, dbColumnNamesOrDefs, dbColumnValues):
        """Save function data to a database"""
        self.accessingDatabaseOfFunctions(
            dbName, "insert", dbTable, dbColumnNamesOrDefs, dbColumnValues
        )

    def add_label(self, text, labelAnchor, labelPosX, labelPosY, txtFont, txtColor):
        label = tb.Label(
            self, 
            text=text, 
            font=txtFont, 
            foreground=txtColor
        )
        label.place(anchor=labelAnchor, x=labelPosX, y=labelPosY)
        return label
    
    def add_button(self, buttonAnchor, buttonPosX, buttonPosY, text, command):
        button = tb.Button(
            self, 
            text=text, 
            command=command
        )
        button.place(anchor=buttonAnchor, x=buttonPosX, y=buttonPosY)
        return button

if __name__ == "__main__":
    app = AutoGuiApp()
    app.mainloop()