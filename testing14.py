from pywinauto.application import Application
from pywinauto.findwindows import find_windows
import time

# Step 1: Find all windows matching the title
matches = find_windows(title_re=".*Hospital Information System.*", backend="uia")

# Step 2: Print all handles to choose from
for i, handle in enumerate(matches):
    print(f"[{i}] Handle: {handle}")

# Step 3: Choose the correct handle
chosen_index = 1  # Update this as needed
target_handle = matches[chosen_index]

# Step 4: Connect using handle
app = Application(backend="uia").connect(handle=target_handle)

# Step 5: Get the window spec
main_win_spec = app.window(handle=target_handle)

# Step 6: Get the UIAWrapper object (full window object)
main_win = main_win_spec.wrapper_object()

# Step 7: Set focus
main_win.set_focus()

# Step 8: Print control identifiers
main_win.print_control_identifiers()  # ✅ This should now work
