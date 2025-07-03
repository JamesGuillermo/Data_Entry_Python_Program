# live_filter_demo.py
# A very small Tkinter/ttkbootstrap app that filters a dropdown list
# as you type, mimicking the modern “search‑inside‑dropdown” behavior.

import ttkbootstrap as tb                  # pip install ttkbootstrap
from ttkbootstrap.widgets import *          # for themed widgets
from tkinter import END, Listbox                     # constant for Listbox ops

# ---------- 1. Basic window setup ----------
root = tb.Window(themename="superhero")
root.title("Live‑Filter Combobox Demo")

# Data you want to choose from
COMPANIES = [
    "Company A", "Company B", "Company C",
    "Alpha Corp", "Beta Logistics", "Gamma Solutions",
    "Delta Manufacturing", "Echo Energy"
]

# ---------- 2. Entry box where the user types ----------
entry_var = tb.StringVar()                 # keeps track of what’s typed
entry = tb.Entry(root, textvariable=entry_var,
                 width=30, bootstyle="primary")
entry.pack(pady=10)

# ---------- 3. Listbox that shows possible matches ----------
listbox = Listbox(root, height=6)       # sits under the Entry
listbox.pack_forget()                      # start hidden

# ---------- 4. Core logic: filter as you type ----------
def update_list(event=None):
    typed = entry_var.get().lower()        # what the user has typed
    listbox.delete(0, END)                 # clear old options

    # Add back only items that contain the typed text
    for item in COMPANIES:
        if typed in item.lower():          # simple case‑insensitive match
            listbox.insert(END, item)

    # Show or hide the list depending on whether we have matches
    if listbox.size() > 0:
        listbox.pack(after=entry, padx=10)
    else:
        listbox.pack_forget()

entry.bind("<KeyRelease>", update_list)    # run after every keystroke

# ---------- 5. When the user clicks an option ----------
def fill_out(event):
    if listbox.curselection():
        selected = listbox.get(listbox.curselection())
        entry_var.set(selected)            # copy chosen text into Entry
        listbox.pack_forget()              # hide the dropdown

listbox.bind("<<ListboxSelect>>", fill_out)

# ---------- 6. Populate dropdown once at start ----------
update_list()
root.mainloop()
