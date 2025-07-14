from tkinter import *
from ttkbootstrap import *
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import *
from tkinter import END, Listbox
import ttkbootstrap as tb
import datetime
import os, pandas as pd
import sqlite3

xLabelPlaceEntry = 20
yLabelPlaceEntry = 0
labelEntryTxtFont = "times new roman"
labelEntryTxtSize = 15

xEntryBoxPos = 300
yEntryBoxPos = 0

'''companies = sqlite3.connect("companies.db")
companiesCursor = companies.cursor()
companiesCursor.execute("CREATE TABLE IF NOT EXISTS companies (id INTEGER PRIMARY KEY, companyName TEXT)")
companies.commit()
companies.close()'''

def insert_company(name):
    conn = sqlite3.connect("companies.db")  # Open the DB
    cursor = conn.cursor()                  # Get the pen to write

    cursor.execute("INSERT INTO companies (companyName) VALUES (?)", (name,))
    # The ? is a placeholder to prevent SQL injection
    # (name,) is a tuple

    conn.commit()  # Save the changes
    conn.close()


class MyApp(tb.Window):
    def __init__(self, xHeaderPos=0, yHeaderPos=0):
        super().__init__(title="Data Entry Application", themename="darkly")
        self.geometry("1500x1000")
        self.label = Label(self, text="Hello yeeeeeee", font=("Arial", 15))
        self.label.place(anchor=CENTER,x=xHeaderPos, y=yHeaderPos)
        

    def label_add(self, text, addLabelAnch, xAddLabelPos=0, yAddLabelPos=0, txtFont="", txtSize=0):
        self.label_new= Label(self, text=text, font=(txtFont, txtSize))
        self.label_new.place(anchor=addLabelAnch, x=xAddLabelPos, y=yAddLabelPos)
        return self.label_new
    
    def entry_add(self, addEntryAnch, xEntryBoxPos=0, yEntryBoxPos=0, txtFont=""):
        self.entry_new = Entry(self, font=(txtFont, 10))
        self.entry_new.place(anchor=addEntryAnch, x=xEntryBoxPos, y=yEntryBoxPos)
        return self.entry_new
    
    def listbox_add(self, addListboxAnch, xListboxPos=0, yListboxPos=0, width=0, height=0):
        self.listbox_new = Listbox(self, width=width, height=height)
        self.listbox_new.place(anchor=addListboxAnch, x=xListboxPos, y=yListboxPos)
        return self.listbox_new
    
    def accessingDatabase(self, db_mode, db_name, db_table_name, db_column_defs_or_names, db_values=None):
        if not db_name.endswith(".db"):
            db_name += ".db"

        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        if db_mode.lower() == "create":
        # Expecting full column definitions like ["companyName TEXT", "industry TEXT"]
            columns_sql = ", ".join(db_column_defs_or_names)
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {db_table_name} (
                    id INTEGER PRIMARY KEY,
                    {columns_sql})""")
    
        elif db_mode.lower() == "insert":
        # Expecting just column names like ["companyName", "industry"]
            if not db_values:
                raise ValueError("Insert mode requires db_values")

            column_names = ", ".join(db_column_defs_or_names)
            placeholders = ", ".join(["?"] * len(db_values))
            sql = f"INSERT INTO {db_table_name} ({column_names}) VALUES ({placeholders})"
            cursor.execute(sql, db_values)

        conn.commit()
        conn.close()

    
    def load_companies(self):
        # Connect to DB and get company names
        conn = sqlite3.connect("companies.db")
        cursor = conn.cursor()
        cursor.execute("SELECT companyName FROM companies")
        company_names = [row[0] for row in cursor.fetchall()]
        conn.close()

        # Clear the listbox
        self.listbox_new.delete(0, END)
        # Insert company names into the listbox
        for name in company_names:
            self.listbox_new.insert(END, name)

    def empty_listbox(self):
        self.listbox_new.delete(0, END)

    def load_transactions(self):
        return



app = MyApp(xHeaderPos=750, yHeaderPos=50)

app.label_add("ID Number",addLabelAnch=W, xAddLabelPos=xLabelPlaceEntry, yAddLabelPos=150, txtFont=labelEntryTxtFont, txtSize=labelEntryTxtSize)
app.label_add("LastName",addLabelAnch=W, xAddLabelPos=xLabelPlaceEntry, yAddLabelPos=200, txtFont=labelEntryTxtFont, txtSize=labelEntryTxtSize)
app.label_add("FirstName",addLabelAnch=W, xAddLabelPos=xLabelPlaceEntry, yAddLabelPos=250, txtFont=labelEntryTxtFont, txtSize=labelEntryTxtSize)
app.label_add("MiddleName",addLabelAnch=W, xAddLabelPos=xLabelPlaceEntry, yAddLabelPos=300, txtFont=labelEntryTxtFont, txtSize=labelEntryTxtSize)
app.label_add("Date of Birth",addLabelAnch=W, xAddLabelPos=xLabelPlaceEntry, yAddLabelPos=350, txtFont=labelEntryTxtFont, txtSize=labelEntryTxtSize)
app.label_add("Gender",addLabelAnch=W, xAddLabelPos=xLabelPlaceEntry, yAddLabelPos=400, txtFont=labelEntryTxtFont, txtSize=labelEntryTxtSize)
app.label_add("Contact Number",addLabelAnch=W, xAddLabelPos=xLabelPlaceEntry, yAddLabelPos=450, txtFont=labelEntryTxtFont, txtSize=labelEntryTxtSize)
app.label_add("Address",addLabelAnch=W, xAddLabelPos=xLabelPlaceEntry, yAddLabelPos=500, txtFont=labelEntryTxtFont, txtSize=labelEntryTxtSize)
app.label_add("Email",addLabelAnch=W, xAddLabelPos=xLabelPlaceEntry, yAddLabelPos=550, txtFont=labelEntryTxtFont, txtSize=labelEntryTxtSize)
app.label_add("Company",addLabelAnch=W, xAddLabelPos=xLabelPlaceEntry, yAddLabelPos=600, txtFont=labelEntryTxtFont, txtSize=labelEntryTxtSize)
app.label_add("Transaction",addLabelAnch=W, xAddLabelPos=xLabelPlaceEntry, yAddLabelPos=650, txtFont=labelEntryTxtFont, txtSize=labelEntryTxtSize)
app.label_add("Date of Transaction",addLabelAnch=W, xAddLabelPos=xLabelPlaceEntry, yAddLabelPos=700, txtFont=labelEntryTxtFont, txtSize=labelEntryTxtSize)
charges = app.label_add("Charges",addLabelAnch=W, xAddLabelPos=xLabelPlaceEntry, yAddLabelPos=750, txtFont=labelEntryTxtFont, txtSize=labelEntryTxtSize)
charges.config(text="Charges (in PHP)")

entryIDnumber = app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=150, txtFont=labelEntryTxtFont)
entryLastName = app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=200, txtFont=labelEntryTxtFont)
entryFirstName = app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=250, txtFont=labelEntryTxtFont)
entryMiddleName = app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=300, txtFont=labelEntryTxtFont)
entyrDateOfBirth = app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=350, txtFont=labelEntryTxtFont)
entryGender = app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=400, txtFont=labelEntryTxtFont)
entryContactNumber = app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=450, txtFont=labelEntryTxtFont)
entryAddress = app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=500, txtFont=labelEntryTxtFont)
entryEmail = app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=550, txtFont=labelEntryTxtFont)
entryEmail.bind("<FocusIn>", lambda event: app.empty_listbox())

entryCompanies = app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=600, txtFont=labelEntryTxtFont)
entryCompanies.bind("<FocusIn>", lambda event: app.load_companies())
#entryCompanies.bind("<FocusOut>", lambda event: app.empty_listbox())

entryTransaction = app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=650, txtFont=labelEntryTxtFont)
transactionDateValue = app.label_add("", addLabelAnch=W, xAddLabelPos=xEntryBoxPos, yAddLabelPos=700, txtFont=labelEntryTxtFont, txtSize=labelEntryTxtSize)
transactionDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
transactionDateValue.config(text=transactionDate)
entryCharges = app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=750, txtFont=labelEntryTxtFont)

app.listbox_add(addListboxAnch=NW, xListboxPos=600, yListboxPos=130, width=50, height=3)

#app.accessingDatabase("create", "companies.db", "companies", ["companyName TEXT"], db_values=None)
db_companies = ["OpenAir", "Google", "Microsoft", "Amazon", "Apple", "Meta Platforms Inc", "Tesla Inc", "Nvidia Corp"]
for company in db_companies:
    app.accessingDatabase("insert", "companies.db", "companies", ["companyName"], db_values=(company,))



app.mainloop()