import ttkbootstrap as tb

class AutoGuiApp(tb.Window):
    def __init__(self):
        super().__init__(title="Auto GUI Application", themename="darkly")
        self.geometry("1700x1000")
        self.resizable(True, True)
        self.saveFunctions = {}
        self.labels = {}
        self.buttons = {}
        self.entries = {}
        self.functionCounter = 0

        self.createWidgets()

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
    def add_entry(self, entryAnchor, entryPosX, entryPosY, entryWidth, entryFont):
        entry = tb.Entry(
            self,  
            width=entryWidth, 
            font=entryFont
        )
        entry.place(anchor=entryAnchor, x=entryPosX, y=entryPosY)
        return entry
    
    def createWidgets(self):
        # Example of creating a label and button
        self.labels['exampleLabel'] = self.add_label(
            "Example Label", "w", 100, 100, ("Arial", 12), "white"
        )
        self.buttons['exampleButton'] = self.add_button(
            "w", 100, 150, "Click Me", self.saveFunctionsCommand
        )
        self.buttons['displayFunctions'] = self.add_button(
            "w", 100, 200, "Display Functions", self.displayFunctions
        )
        self.labels['chooseFunction'] = self.add_label(
            "Choose Function:", "w", 100, 250, ("Arial", 12), "white"
        )
        self.entries['functionEntry'] = self.add_entry(
            "w", 100, 300, 200, ("Arial", 12)
        )
        self.buttons['getChoosenFunction'] = self.add_button(
            "w", 100, 350, "Get Function", self.getChoosenFunction
        )
    def printFunctions(self):
        return f"Functions: {self.functionCounter}"

    def functionToSave(self):
        """Example function to be saved"""
        self.functionCounter += 1
        print(f"Function {self.functionCounter} executed")
        self.saveFunctions[f"function_{self.functionCounter}"] = self.printFunctions()

    def saveFunctionsCommand(self):

        # This is a placeholder for actual saving logic
        self.functionToSave()
        return f"Function {self.functionCounter} saved successfully!"
    
    def displayFunctions(self):
        """Display all saved functions"""
        if not self.saveFunctions:
            print("No functions saved yet.")
            return
        
        print("Saved Functions:")
        for name, code in self.saveFunctions.items():
            print(f"{name}: {code}")
    def getChoosenFunction(self):
        """Get the chosen function from the entry"""
        function_name = self.entries['functionEntry'].get()
        if f"function_{function_name}" in self.saveFunctions:
            print(f"Chosen Function: {self.saveFunctions[f'function_{function_name}']}")
        else:
            print(f"Function {function_name} not found in saved functions.")
        



app = AutoGuiApp()
app.mainloop()