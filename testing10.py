from pywinauto import Desktop

# Get all windows with the same title
windows = Desktop(backend="uia").windows(title="Hospital Information System 8")

# Show them
for i, w in enumerate(windows):
    print(f"[{i}] Title: {w.window_text()} - Control Type: {w.element_info.control_type}")

# If you're sure you want the first window:
dlg = windows[2]  # or windows[1], depending on which one is the login/main window

# Instead of dlg.wait(), use this:
dlg.set_focus()  # optional - brings it to front
dlg.print_control_identifiers()
