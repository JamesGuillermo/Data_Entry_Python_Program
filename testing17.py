import subprocess
import os
import time

# File path from the image you provided
file_path = r"C:\Users\Lifecare IT Admin\Desktop\Bizbox 8.26.14.38 02132024\HIS_8.26.14.38-OR-12142023\BizBox Hospital Information System 8.0.application"

# Open the file using subprocess
import sys
try:
	import pyautogui
except Exception:
	pyautogui = None

# Path can be provided as the first CLI argument. Otherwise the hardcoded path is used.
DEFAULT_PATH = r"C:\Users\Lifecare IT Admin\Desktop\Bizbox 8.26.14.38 02132024\HIS_8.26.14.38-OR-12142023\BizBox Hospital Information System 8.0.application"


def open_file(path: str) -> None:
	"""Try to open the given file on Windows. Uses os.startfile if available, falls back to subprocess.run."""
	if not os.path.exists(path):
		print(f"File not found: {path}")
		return

	# Prefer os.startfile on Windows (will use default handler)
	try:
		os.startfile(path)
		print(f"Opened file with os.startfile: {path}")
		return
	except Exception as e:
		print(f"os.startfile failed: {e}")

	# Fallback: try running via subprocess (shell=True helps run .application/registered handlers)
	try:
		subprocess.run(path, check=True, shell=True)
		print(f"Opened file via subprocess.run: {path}")
		return
	except Exception as e:
		print(f"subprocess.run failed: {e}")


if __name__ == "__main__":
	path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
	open_file(path)

	# After opening the application, perform the exact requested sequence using pyautogui
	def perform_sequence():
		if pyautogui is None:
			print('pyautogui not installed. Install with: pip install pyautogui')
			return

		try:
			print('Sequence start: waiting 30s')
			time_to_wait = 30
			# simple countdown printouts (optional)
			for _ in range(3):
				time.sleep(time_to_wait/3)
			# follow the exact requested steps
			pyautogui.write('JAM', interval=0.05)
			time.sleep(1)
			pyautogui.press('tab')
			time.sleep(0.1)
			pyautogui.write('1', interval=0.05)
			time.sleep(1)
			pyautogui.press('enter')
			time.sleep(10)
			pyautogui.click(46, 867)
			time.sleep(0.2)
			pyautogui.click(46, 867)
			time.sleep(30)
			print('Sequence finished')
		except Exception as e:
			print('Error during sequence:', e)

	perform_sequence()
