from pywinauto import Desktop

# List all visible windows using UIA backend
windows = Desktop(backend="uia").windows()

for win in windows:
    print(win.window_text())
