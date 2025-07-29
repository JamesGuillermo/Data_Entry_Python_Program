import ttkbootstrap as tb
from ttkbootstrap.constants import *
from datetime import datetime

class DropdownExample(tb.Window):
    def __init__(self):
        super().__init__(title="Dropdown List Example", themename="darkly")
        self.geometry("600x500")
        
        # Create various dropdown examples
        self.create_comboboxes()
        
    def create_comboboxes(self):
        # Frame for layout
        main_frame = tb.Frame(self)
        main_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)
        
        # 1. Simple dropdown with string values
        label1 = tb.Label(main_frame, text="Select Monitor:", font=("Arial", 12))
        label1.pack(anchor=W, pady=(0, 5))
        
        self.monitor_combo = tb.Combobox(
            main_frame,
            values=["Primary Monitor", "Secondary Monitor", "Both Monitors"],
            state="readonly"  # Makes it dropdown-only (user can't type)
        )
        self.monitor_combo.pack(fill=X, pady=(0, 20))
        self.monitor_combo.set("Primary Monitor")  # Set default value
        self.monitor_combo.bind("<<ComboboxSelected>>", self.on_monitor_select)
        
        # 2. Dropdown with numeric values
        label2 = tb.Label(main_frame, text="Select Delay (seconds):", font=("Arial", 12))
        label2.pack(anchor=W, pady=(0, 5))
        
        self.delay_combo = tb.Combobox(
            main_frame,
            values=[0.1, 0.5, 1, 2, 5, 10],
            state="readonly"
        )
        self.delay_combo.pack(fill=X, pady=(0, 20))
        self.delay_combo.set(1)
        self.delay_combo.bind("<<ComboboxSelected>>", self.on_delay_select)
        
        # 3. Editable dropdown (user can type custom values)
        label3 = tb.Label(main_frame, text="Custom Command:", font=("Arial", 12))
        label3.pack(anchor=W, pady=(0, 5))
        
        self.command_combo = tb.Combobox(
            main_frame,
            values=["click", "doubleClick", "rightClick", "drag", "scroll"],
            state="normal"  # Allows typing
        )
        self.command_combo.pack(fill=X, pady=(0, 20))
        self.command_combo.set("click")
        
        # 4. Dropdown with dynamic content
        label4 = tb.Label(main_frame, text="Recent Actions:", font=("Arial", 12))
        label4.pack(anchor=W, pady=(0, 5))
        
        self.actions_combo = tb.Combobox(main_frame, state="readonly")
        self.actions_combo.pack(fill=X, pady=(0, 20))
        self.update_recent_actions()
        
        # Buttons to interact with dropdowns
        btn_frame = tb.Frame(main_frame)
        btn_frame.pack(fill=X, pady=10)
        
        get_btn = tb.Button(btn_frame, text="Get Selected Values", 
                           command=self.get_selected_values, bootstyle="primary")
        get_btn.pack(side=LEFT, padx=5)
        
        update_btn = tb.Button(btn_frame, text="Update Actions", 
                              command=self.update_recent_actions, bootstyle="success")
        update_btn.pack(side=LEFT, padx=5)
        
        # Result display
        self.result_label = tb.Label(main_frame, text="Select options above...", 
                                   font=("Arial", 10), foreground="yellow")
        self.result_label.pack(pady=20)
    
    def on_monitor_select(self, event):
        """Handle monitor selection"""
        selected = self.monitor_combo.get()
        print(f"Monitor selected: {selected}")
    
    def on_delay_select(self, event):
        """Handle delay selection"""
        selected = self.delay_combo.get()
        print(f"Delay selected: {selected}")
    
    def update_recent_actions(self):
        """Update dropdown with recent actions"""
        # Simulate recent actions
        recent_actions = [
            f"Click at (100, 200) - {datetime.now().strftime('%H:%M:%S')}",
            f"Move to (500, 300) - {datetime.now().strftime('%H:%M:%S')}",
            f"Type 'Hello' - {datetime.now().strftime('%H:%M:%S')}",
            f"Screenshot saved - {datetime.now().strftime('%H:%M:%S')}"
        ]
        self.actions_combo['values'] = recent_actions
        if recent_actions:
            self.actions_combo.set(recent_actions[0])
    
    def get_selected_values(self):
        """Get all selected values and display them"""
        monitor = self.monitor_combo.get()
        delay = self.delay_combo.get()
        command = self.command_combo.get()
        
        action = self.actions_combo.get()
        
        result_text = f"Monitor: {monitor}\nDelay: {delay}\nCommand: {command}\nAction: {action}"
        self.result_label.config(text=result_text)

# Usage
app = DropdownExample()
app.mainloop()