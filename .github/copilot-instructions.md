# Copilot Instructions for Data_Entry_Python_Program

## Project Overview
- Desktop automation and data entry tool built with Python, Tkinter, and ttkbootstrap.
- Main UI logic is in `autoGui20.py` (class `AutoGuiApp`).
- Selenium scripts (e.g., `testing05.py`) automate browser-based login and form submission for external web systems.
- Data is managed via Excel files (using pandas) and optionally SQLite (`app1.db`).

## Key Components
- `autoGui20.py`: Main GUI, batch automation, Excel integration, PyAutoGUI for screen automation.
- `App.py`, `App1.py`: Alternative or legacy app entry points.
- `testing05.py`: Selenium-based login automation for web forms.
- `GoogleSheetAPI.py`, `OpenpyXL.py`: Integrations for Google Sheets and Excel.
- `chromedriver.exe`: Required for Selenium Chrome automation.

## Developer Workflows
- **Run GUI app:** `python autoGui20.py` (main recommended entry point)
- **Run Selenium automation:** `python testing05.py` (for web login automation)
- **Install dependencies:** `pip install -r requirements.txt` (includes `ttkbootstrap`, `selenium`, `pandas`, etc.)
- **Excel file selection:** GUI allows browsing and selecting Excel files for batch processing.
- **Batch automation:** Use GUI buttons to start/stop batch; ESC key stops automation (see `start_escape_listener`).

## Patterns & Conventions
- All UI widgets are created via helper methods (`add_label`, `add_entry`, etc.) for consistency.
- Data flows: Excel → GUI → Automated entry (via PyAutoGUI or Selenium).
- Company name auto-selection based on ID number format (see `id_number_format`).
- Automation coordinates and logic are hardcoded for specific screen layouts; update coordinates if UI changes.
- Use `pyautogui.locateOnScreen` for image-based flow control (e.g., detecting popups).
- Batch automation is interruptible via ESC key and PyAutoGUI failsafe (mouse to corner).

## Integration Points
- **Excel:** Read/write via pandas; columns must match expected names.
- **Selenium:** Requires `chromedriver.exe` in project root; update path if needed.
- **Google Sheets:** See `GoogleSheetAPI.py` for API usage.
- **Images:** PNG files in root used for screen detection (e.g., `noRecordFound.png`).

## Troubleshooting
- If automation fails, check for popups or overlays blocking UI elements.
- Update hardcoded coordinates if running on different screen resolutions.
- Ensure all required dependencies are installed and up to date.

## Example: Adding a New Data Field
- Update `create_widgets` in `autoGui20.py` to add new label, entry, and combobox.
- Update Excel column handling in `save_entry_to_excel` and `load_excel_data`.

---

For questions or unclear sections, please provide feedback to improve these instructions.
