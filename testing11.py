from pywinauto import Application, Desktop

# Step 1: Find the target window
windows = Desktop(backend="uia").windows(title="Hospital Information System 8")

# Step 2: Choose the correct one (e.g., main login window)
target_window = windows[3]  # or [1] or [2] based on behavior

# Step 3: Attach using handle (get control back as WindowSpecification)
app = Application(backend="uia").connect(handle=target_window.handle)

# Step 4: Get window object
dlg = app.window(handle=target_window.handle)

# Now you can inspect
dlg.print_control_identifiers(depth=2)
