import ttkbootstrap as tb
import pyautogui
import sqlite3

class AutoGuiApp(tb.Window):
    def __init__(self):
        super().__init__(title="Auto GUI Application", themename="darkly")
        self.geometry("1700x1000")
        self.resizable(True, True)
        self.labels = {}
        self.buttons = {}
        self.functions = {}

        self.create_widgets()

        self.accessingDatabaseOfFunctions(
            "functions.db", "create", "functions_table",
            ["id INTEGER PRIMARY KEY", "name TEXT", "function TEXT"],
            []
        )

    def create_widgets(self):
        # Example of adding a label
        self.labels['example'] = self.add_label(
            "Example Label", "w", 100, 100, ("Arial", 16), "white"
        )
        
        # Example of adding a button
        self.buttons['example_button'] = self.add_button(
            "w", 100, 150, "Click Me", self.on_button_click
        )
    
    def on_button_click(self):
        """Handle button click event"""
        print("Button clicked!")
        # Example action: Move mouse to a specific position
        pyautogui.moveTo(200, 200, duration=0.5)

        self.functions[f"function_{len(self.functions) + 1}"] = self.add_label(
            f"Function {len(self.functions) + 1} executed", "w", 100, 200 + len(self.functions) * 30, ("Arial", 12), "green"
        )

    
    def accessingDatabaseOfFunctions(self, dbName, dbmode, dbTable, dbColumnNamesOrDefs, dbColumnValues):
        """Access a database and perform operations"""
        conn = sqlite3.connect(dbName)
        cursor = conn.cursor()
        
        if dbmode == "create":
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {dbTable} ({', '.join(dbColumnNamesOrDefs)})")
            conn.commit()
            print(f"Table {dbTable} created with columns: {dbColumnNamesOrDefs}")
        
        elif dbmode == "insert":
            placeholders = ', '.join(['?'] * len(dbColumnValues))
            cursor.execute(f"INSERT INTO {dbTable} VALUES ({placeholders})", dbColumnValues)
            conn.commit()
            print(f"Inserted values into {dbTable}: {dbColumnValues}")
        
        elif dbmode == "select":
            cursor.execute(f"SELECT * FROM {dbTable}")
            rows = cursor.fetchall()
            print(f"Data from {dbTable}: {rows}")
        
        conn.close()
    
    def accessingDatabaseOfFunctionsToGet(self, dbName, dbTable, dbColumnNamesOrDefs):
        """Get data from a database"""
        conn = sqlite3.connect(dbName)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT {', '.join(dbColumnNamesOrDefs)} FROM {dbTable}")
        rows = cursor.fetchall()
        
        conn.close()
        return rows

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

app = AutoGuiApp()
app.mainloop()