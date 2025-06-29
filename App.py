from tkinter import *
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from ttkbootstrap.widgets import *

root = tb.Window(themename="superhero")
root.title("Data Entry")
root.geometry("1500x1000")

gender_var = StringVar()
company_var = StringVar()

#Labels for data entry

labelTitle = tb.Label(root, text="Data Entry", font=("Helvetica", 25))
labelTitle.pack(pady=15)

labelIDnumber = tb.Label(root, text="ID Number", font=("Helvetica", 15))
labelIDnumber.place(x=20, y=150, anchor="w")

labelLastName = tb.Label(root, text="Last Name", font=("Helvetica", 15))
labelLastName.place(x=20, y=200, anchor="w")

labelFirstName = tb.Label(root, text="First Name", font=("Helvetica", 15))
labelFirstName.place(x=20, y=250, anchor="w")

labelMiddleName = tb.Label(root, text="Middle Name", font=("Helvetica", 15))
labelMiddleName.place(x=20, y=300, anchor="w")

labelBirthDate = tb.Label(root, text="Birth Date", font=("Helvetica", 15))
labelBirthDate.place(x=20, y=350, anchor="w")

labelGender = tb.Label(root, text="Gender", font=("Helvetica", 15))
labelGender.place(x=20, y=400, anchor="w")

labelContactNumber = tb.Label(root, text="Contact Number", font=("Helvetica", 15))
labelContactNumber.place(x=20, y=450, anchor="w")

labelCompanyName = tb.Label(root, text="Company Name", font=("Helvetica", 15))
labelCompanyName.place(x=20, y=500, anchor="w")

#Entrl widgets for data entry

entryIDnumber = tb.Entry(root, width=30, bootstyle="primary")
entryIDnumber.place(x=250, y=150, anchor="w")

entryLastName = tb.Entry(root, width=30, bootstyle="primary")
entryLastName.place(x=250, y=200, anchor="w")

entryFirstName = tb.Entry(root, width=30, bootstyle="primary")
entryFirstName.place(x=250, y=250, anchor="w")

entryMiddleName = tb.Entry(root, width=30, bootstyle="primary")
entryMiddleName.place(x=250, y=300, anchor="w")

entryBirthDate = DateEntry(root, width=30, bootstyle="primary", dateformat="%Y-%m-%d")
entryBirthDate.place(x=250, y=350, anchor="w")

entryGender = tb.Combobox(root, textvariable=gender_var, values=["Male", "Female"], width=28, bootstyle="primary")
entryGender.place(x=250, y=400, anchor="w")

entryContactNumber = tb.Entry(root, width=30, bootstyle="primary")
entryContactNumber.place(x=250, y=450, anchor="w")

entryCompanyName = tb.Combobox(root, textvariable=company_var, values=["Company A", "Company B", "Company C"], width=28, bootstyle="primary")
entryCompanyName.place(x=250, y=500, anchor="w")



root.mainloop()