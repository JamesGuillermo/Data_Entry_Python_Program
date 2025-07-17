import gspread

ss = gspread.service_account(filename=r"C:\Users\Lifecare IT Admin\Downloads\GoogleSheetAPI.json")
sh = ss.open("GoogleSheetAPI")
sheet = sh.worksheet("Sheet1")

sheet.update('A1', [['Hello, World!']])