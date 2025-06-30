from tkinter import *
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from ttkbootstrap.widgets import *
from ttkbootstrap.widgets import DateEntry

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

labePrintData = tb.Label(root, text="", font=("Helvetica", 15))
labePrintData.place(x=800, y=100, anchor="w")

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

#Button to submit data

saved_data = []

def save_data():
    id_number = entryIDnumber.get()
    last_name = entryLastName.get()
    first_name = entryFirstName.get()
    middle_name = entryMiddleName.get()
    birth_date_str = entryBirthDate.entry.get()  # Use .value to get the date
    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
    contact_number = entryContactNumber.get()
    company_name = entryCompanyName.get()

    saved_data.append({
        "ID Number": id_number,
        "Last Name": last_name,
        "First Name": first_name,
        "Middle Name": middle_name,
        "Birth Date": birth_date,
        "Contact Number": contact_number,
        "Company Name": company_name})
    
def print_saved_data():
    if saved_data:
        # Show only the last entry, or format as needed
        last = saved_data[-1]
        text = (
            f"ID: {last['ID Number']}, "
            f"Name: {last['First Name']} {last['Middle Name']} {last['Last Name']}, "
            f"Birth: {last['Birth Date']}, "
            f"Contact: {last['Contact Number']}, "
            f"Company: {last['Company Name']}"
        )
    else:
        text = "No data saved."
    labePrintData.config(text=text)

buttonSave = tb.Button(root, text="Save Data", bootstyle="success", command=save_data)
buttonSave.place(x=250, y=600, anchor="w")

buttonPrint = tb.Button(root, text="Print Data", bootstyle="info", command=print_saved_data)
buttonPrint.place(x=370, y=600, anchor="w")





root.mainloop()