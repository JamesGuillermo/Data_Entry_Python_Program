import os
import sys
import time
from typing import Optional

try:
    from pywinauto import Application, timings
    from pywinauto.findwindows import ElementNotFoundError
except Exception:
    Application = None

try:
    import pyautogui
except Exception:
    pyautogui = None


# Configuration
DEFAULT_APP_PATH = r"C:\Users\Lifecare IT Admin\Desktop\Bizbox 8.26.14.38 02132024\HIS_8.26.14.38-OR-12142023\BizBox Hospital Information System 8.0.application"
WINDOW_TITLE_RE = r"Hospital Information System.*"

# Credentials: prefer environment variables, fallback to system keyring if available
USERNAME = "JAM"
PASSWORD = "1"

try:
    import keyring
except Exception:
    keyring = None

# If env vars aren't set, try reading from keyring
if not USERNAME and keyring:
    try:
        USERNAME = keyring.get_password("auto_login", "username")
    except Exception:
        USERNAME = None

if not PASSWORD and keyring:
    try:
        PASSWORD = keyring.get_password("auto_login", "password")
    except Exception:
        PASSWORD = None


def print_instructions():
    print("auto_login.py: credentials should be provided via environment variables:\n  AUTO_LOGIN_USER and AUTO_LOGIN_PASS")


def login_with_pywinauto(app_path: Optional[str] = None, title_re: str = WINDOW_TITLE_RE) -> bool:
    """Attempt to connect to the application window with pywinauto and fill credentials.
    Returns True if login action was attempted, False otherwise.
    """
    if Application is None:
        print("pywinauto is not installed. Install with: pip install pywinauto")
        return False

    try:
        # Try to connect to an existing window first
        app = Application(backend="uia")
        try:
            app.connect(title_re=title_re, timeout=5)
            print("Connected to running application.")
        except Exception:
            # If not running, try to start it
            path = app_path or DEFAULT_APP_PATH
            if not os.path.exists(path):
                print(f"Application not found at: {path}")
                return False
            print(f"Starting application: {path}")
            # If it's an .exe, use pywinauto start; otherwise use os.startfile (ClickOnce .application, shortcuts, etc.)
            try:
                if path.lower().endswith('.exe'):
                    app.start(path)
                else:
                    # Use os.startfile for non-exe handlers (ClickOnce .application, .lnk, etc.)
                    os.startfile(path)
                # allow time for the UI to appear
                time.sleep(4)
                app.connect(title_re=title_re, timeout=20)
            except Exception as e:
                print(f"Failed to start/connect application: {e}")
                return False

        dlg = app.window(title_re=title_re)
        dlg.wait('visible', timeout=20)

        # Save control identifiers to file for inspection
        try:
            with open('control_ids.txt', 'w', encoding='utf-8') as f:
                dlg.print_control_identifiers(file=f)
            print("Wrote control identifiers to control_ids.txt")
        except Exception as e:
            print(f"Could not write control identifiers: {e}")

        # If username/password provided, attempt to set them
        if USERNAME and PASSWORD:
            # Strategy: find Edit controls under the dialog and set text
            try:
                edits = dlg.descendants(control_type="Edit")
                if len(edits) >= 2:
                    print("Found Edit controls via UIA, setting username/password")
                    edits[0].set_text(USERNAME)
                    edits[1].set_text(PASSWORD)
                else:
                    # Try common automation ids / names
                    candidates = [
                        ("txtUsercode", "Edit"), ("Usercode", "Edit"), ("txtUsername", "Edit"),
                        ("txtPassword", "Edit"), ("Password", "Edit")
                    ]
                    set_count = 0
                    for auto_id, _ in candidates:
                        try:
                            ctl = dlg.child_window(auto_id=auto_id)
                            ctl.set_text(USERNAME if set_count == 0 else PASSWORD)
                            set_count += 1
                            if set_count >= 2:
                                break
                        except Exception:
                            continue

                    if set_count < 2:
                        print("Could not locate Edit controls reliably via automation ids.")

            except Exception as e:
                print(f"Error locating edit controls: {e}")

            # Try to click the Login button
            try:
                btn = None
                # common button titles
                for title in ["Login", "Log in", "OK", "Sign in"]:
                    try:
                        btn = dlg.child_window(title=title, control_type="Button")
                        if btn.exists():
                            btn.click_input()
                            print(f"Clicked button '{title}'")
                            break
                    except Exception:
                        continue

                if btn is None:
                    # fallback: click first button
                    buttons = dlg.descendants(control_type="Button")
                    if buttons:
                        buttons[0].click_input()
                        print("Clicked first button as fallback")

            except Exception as e:
                print(f"Error clicking login button: {e}")

            return True
        else:
            print("USERNAME/PASSWORD not set in env vars; printed control IDs only.")
            return False

    except Exception as e:
        print("pywinauto error:", e)
        return False


def login_with_pyautogui(username: str, password: str) -> bool:
    """Fallback image/coordinate-based automation using pyautogui.
    Requires prepared screenshots: user_field.png, pass_field.png, login_button.png
    """
    if pyautogui is None:
        print("pyautogui is not installed. Install with: pip install pyautogui")
        return False

    time.sleep(1)
    try:
        # locate username field image
        u = pyautogui.locateOnScreen('user_field.png', confidence=0.8)
        if u:
            pyautogui.click(pyautogui.center(u))
            pyautogui.write(username, interval=0.03)
        else:
            print('user_field.png not found on screen')

        p = pyautogui.locateOnScreen('pass_field.png', confidence=0.8)
        if p:
            pyautogui.click(pyautogui.center(p))
            pyautogui.write(password, interval=0.03)
        else:
            print('pass_field.png not found on screen')

        b = pyautogui.locateOnScreen('login_button.png', confidence=0.8)
        if b:
            pyautogui.click(pyautogui.center(b))
            print('Clicked login button')
        else:
            print('login_button.png not found on screen')

        return True
    except Exception as e:
        print('pyautogui error:', e)
        return False


def perform_pyautogui_sequence():
    """Perform the fixed sequence the user requested using pyautogui.

    Steps:
    - wait 30s
    - type 'JAM'
    - wait 1s
    - Tab
    - type '1'
    - wait 1s
    - Enter
    - wait 10s
    - two clicks at (46, 867)
    - wait 30s
    """
    if pyautogui is None:
        print("pyautogui is not available. Install with: pip install pyautogui")
        return False

    try:
        print('Waiting 30s for the application to be ready...')
        time.sleep(30)

        print("Typing 'JAM'")
        pyautogui.write('JAM', interval=0.05)
        time.sleep(1)

        print('Pressing Tab')
        pyautogui.press('tab')
        time.sleep(0.1)

        print("Typing '1'")
        pyautogui.write('1', interval=0.05)
        time.sleep(1)

        print('Pressing Enter')
        pyautogui.press('enter')
        time.sleep(10)

        print('Performing two clicks at (46, 867)')
        pyautogui.click(46, 867)
        time.sleep(0.2)
        pyautogui.click(46, 867)

        print('Waiting final 30s')
        time.sleep(30)

        print('pyautogui sequence finished')
        return True
    except Exception as e:
        print('Error during pyautogui sequence:', e)
        return False


def main():
    print_instructions()
    # If called with --pyautogui-sequence, run the fixed sequence (explicit request)
    if '--pyautogui-sequence' in sys.argv:
        perform_pyautogui_sequence()
        return

    # Try pywinauto first
    attempted = login_with_pywinauto()
    if attempted:
        return

    # If credentials available, try pyautogui fallback
    if USERNAME and PASSWORD:
        print('Attempting fallback with pyautogui')
        login_with_pyautogui(USERNAME, PASSWORD)
    else:
        print('No credentials provided; nothing more to do.')


if __name__ == '__main__':
    main()
