import win32print
import win32api
import os

def print_file_to_printer(filepath, printer_name=None):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    if not printer_name:
        printer_name = win32print.GetDefaultPrinter()
    print(f"Printing to: {printer_name}")

    try:
        win32api.ShellExecute(
            0,
            "print",
            filepath,
            None,
            ".",
            0
        )
        print("Print command sent.")
    except Exception as e:
        print(f"Printing failed: {e}")

# Example usage
print_file_to_printer(r"C:\Users\Lifecare IT Admin\Downloads\Arabejo Abiel MedCert 07282025.pdf")