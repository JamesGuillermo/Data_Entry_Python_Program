from pywinauto import Desktop
import time

# Step 1: Find all "Hospital Information System" windows
windows = Desktop(backend="uia").windows()
his_windows = [w for w in windows if "Hospital Information System" in w.window_text()]

# Step 2: Print window list to verify
for i, win in enumerate(his_windows):
    print(f"[{i}] Title: {win.window_text()} - Control Type: {win.friendly_class_name()}")

# Step 3: Choose the correct window (update index if needed)
main_win = his_windows[3]  # You selected index 1

# Step 4: Set focus and convert to wrapper object
main_win.set_focus()
time.sleep(1)
dlg = main_win.wrapper_object()  # ✅ This is required to access advanced methods

# Step 5: Print control identifiers
dlg.print_control_identifiers()  # ✅ Now it should work
