from pywinauto import Application, Desktop
import time

# Step 1: Get all matching top-level windows using Desktop
windows = Desktop(backend="uia").windows()

# Step 2: Filter windows matching "Hospital Information System"
his_windows = [w for w in windows if "Hospital Information System" in w.window_text()]

# Step 3: Show available windows
for i, win in enumerate(his_windows):
    print(f"[{i}] Title: {win.window_text()} - Control Type: {win.friendly_class_name()}")

# Step 4: Choose the correct window (adjust index after running the script)
main_win = his_windows[1]  # Replace with the correct index based on print

# Step 5: Set focus and navigate
main_win.set_focus()
time.sleep(1)

# Optional: Explore structure
main_win.print_control_identifiers()

# Step 6: Interact with the app's controls
# (Replace these with the actual titles printed from print_control_identifiers())
core_components = main_win.child_window(title="Core Components", control_type="MenuItem")
core_components.click_input()
time.sleep(0.5)

outpatients = main_win.child_window(title="Outpatients", control_type="MenuItem")
outpatients.click_input()
