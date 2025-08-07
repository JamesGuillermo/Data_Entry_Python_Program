import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import inspect
import os

# -------------------
# Initial Function (Default)
# -------------------
def greetings(name):
    print(f"Hello {name}! This is the default greeting.")

# -------------------
# Save Function
# -------------------
def save_function():
    func_code = inspect.getsource(greetings)

    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )
    if filepath:
        with open(filepath, "w") as file:
            file.write(func_code)
        messagebox.showinfo("Saved", f"Function saved to:\n{filepath}")

# -------------------
# Load Function
# -------------------
def load_function():
    global greetings

    filepath = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt")]
    )
    if filepath and os.path.exists(filepath):
        with open(filepath, "r") as file:
            func_code = file.read()

        namespace = {}
        exec(func_code, namespace)

        if "greetings" in namespace:
            greetings = namespace["greetings"]
            messagebox.showinfo("Loaded", "Function replaced successfully!")
        else:
            messagebox.showerror("Error", "No function named 'greetings' found.")

# -------------------
# Call Function with Argument
# -------------------
def call_function():
    # Ask user for argument value
    arg = simpledialog.askstring("Input", "Enter a name:")
    if arg is not None:
        try:
            greetings(arg)
        except TypeError as e:
            messagebox.showerror("Error", f"Function call failed:\n{e}")

# -------------------
# GUI Setup
# -------------------
root = tk.Tk()
root.title("Function Hot-Swapper with Arguments")

btn_save = tk.Button(root, text="Save Function", command=save_function)
btn_save.pack(pady=5)

btn_load = tk.Button(root, text="Load Function", command=load_function)
btn_load.pack(pady=5)

btn_call = tk.Button(root, text="Call Function", command=call_function)
btn_call.pack(pady=5)

root.mainloop()
