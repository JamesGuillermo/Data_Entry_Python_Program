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

app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=150, txtFont=labelEntryTxtFont)
app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=200, txtFont=labelEntryTxtFont)
app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=250, txtFont=labelEntryTxtFont)
app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=300, txtFont=labelEntryTxtFont)
app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=350, txtFont=labelEntryTxtFont)
app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=400, txtFont=labelEntryTxtFont)
app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=450, txtFont=labelEntryTxtFont)
app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=500, txtFont=labelEntryTxtFont)
app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=550, txtFont=labelEntryTxtFont)
app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=600, txtFont=labelEntryTxtFont)
app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=650, txtFont=labelEntryTxtFont)
app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=700, txtFont=labelEntryTxtFont)
app.entry_add(addEntryAnch=W, xEntryBoxPos=xEntryBoxPos, yEntryBoxPos=750, txtFont=labelEntryTxtFont)

app.mainloop()