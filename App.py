from tkinter import *
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from ttkbootstrap.widgets import *
from tkinter import END, Listbox
import datetime

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
labePrintData.place(x=600, y=250, anchor="w")

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

company_values = [
    "Company A", "Alpha Corp",
    "Beta Logistics", "Company B",
    "Gamma Solutions", "Delta Manufacturing",
    "Company C", "Echo Energy"
]

entryCompanyName = tb.Entry(root, textvariable=company_var, width=28, bootstyle="primary")
entryCompanyName.place(x=250, y=500, anchor="w")

listbox = Listbox(root, height=2)
listbox.place_forget()

def update_list(event=None):
    typed = entryCompanyName.get().lower()        # what the user has typed
    listbox.delete(0, END)                        # clear old options

    # Add back only items that contain the typed text
    for item in company_values:
        if typed in item.lower():                 # simple case-insensitive match
            listbox.insert(END, item)

    # Show or hide the list depending on whether we have matches
    if listbox.size() > 0:
        listbox.place(x=250, y=530, width=220)
    else:
        listbox.place_forget()

entryCompanyName.bind("<KeyRelease>", update_list)    # run after every keystroke

# ---------- 5. When the user clicks an option ----------
def fill_out(event):
    if listbox.curselection():
        selected = listbox.get(listbox.curselection())
        entryCompanyName.delete(0, END)           # clear the entry
        entryCompanyName.insert(0, selected)      # insert the selected value
        listbox.place_forget()                  # hide the dropdown

listbox.bind("<<ListboxSelect>>", fill_out)

# ---------- 6. Populate dropdown once at start ----------
update_list()

#Button to submit data

saved_data = []

def save_data():

    id_number = entryIDnumber.get()
    last_name = entryLastName.get()
    first_name = entryFirstName.get()
    middle_name = entryMiddleName.get()
    birth_date_str = entryBirthDate.entry.get()  # Use .value to get the date
    
    try:
        birth_date = datetime.datetime.strptime(birth_date_str, "%Y-%m-%d").date()
    except ValueError:
        labePrintData.config(text="Invalid birth date format. Use YYYY-MM-DD.")
        return
   
    gender = entryGender.get()
    contact_number = entryContactNumber.get()
    company_name = entryCompanyName.get()
    date_registered = datetime.date.today()

    if id_number in [entry["ID Number"] for entry in saved_data]:
        labePrintData.config(text="ID Number already exists.")
        return
    elif id_number == "":
        labePrintData.config(text="Please enter ID number or click Auto Generate ID number.")
        return

    saved_data.append({
        "ID Number": id_number,
        "Last Name": last_name,
        "First Name": first_name,
        "Middle Name": middle_name,
        "Birth Date": birth_date,
        "Gender": gender,
        "Contact Number": contact_number,
        "Company Name": company_name,
        "Date Registered": date_registered})
    
    entryIDnumber.delete(0, END)
    entryLastName.delete(0, END)
    entryFirstName.delete(0, END)
    entryMiddleName.delete(0, END)
    entryBirthDate.entry.delete(0, END)  # Clear the date entry
    entryGender.set('')  # Clear the
    entryContactNumber.delete(0, END)
    entryCompanyName.delete(0, END)  # Clear the company name combobox
    
def print_saved_data():
    if saved_data:
        # Show only the last entry, or format as needed
        last = saved_data[-1]
        text = (
            f"ID: {last['ID Number']}\n"
            f"Last Name: {last['First Name']}\n"
            f"First Name: {last['Last Name']}\n"
            f"Middle Name: {last['Middle Name']}\n"
            f"Birth: {last['Birth Date']}\n"
            f"Gender: {last['Gender']}\n"
            f"Contact: {last['Contact Number']}\n"
            f"Company: {last['Company Name']}\n"
            f"Date Registered: {last['Date Registered']}"
        )
    else:
        text = "No data saved."
    labePrintData.config(text=text)

def SearchData():
    input_id = entryIDnumber.get()
    for entry in saved_data:
        if entry["ID Number"] == input_id:
            text = (
                f"ID: {entry['ID Number']}\n"
                f"Last Name: {entry['Last Name']}\n"
                f"First Name: {entry['First Name']}\n"
                f"Middle Name: {entry['Middle Name']}\n"
                f"Birth: {entry['Birth Date']}\n"
                f"Gender: {entry['Gender']}\n"
                f"Contact: {entry['Contact Number']}\n"
                f"Company: {entry['Company Name']}\n"
                f"Date Registered: {entry['Date Registered']}")
            
            entryLastName.delete(0, END)
            entryFirstName.delete(0, END)
            entryMiddleName.delete(0, END)
            entryBirthDate.entry.delete(0, END)  # Clear the date entry
            entryGender.set('')  # Clear the
            entryContactNumber.delete(0, END)
            entryCompanyName.delete(0, END)  # Clear the company name combobox

            labePrintData.config(text=text)

            entryLastName.insert(0, entry["Last Name"])
            entryFirstName.insert(0, entry["First Name"])
            entryMiddleName.insert(0, entry["Middle Name"])
            entryBirthDate.entry.insert(0, entry["Birth Date"].strftime("%Y-%m-%d"))  # Format date for entry
            entryGender.set(entry["Gender"])
            entryContactNumber.insert(0, entry["Contact Number"])
            entryCompanyName.insert(0, entry["Company Name"])           
            break
    else:
        labePrintData.config(text="ID Number not found.")
        entryLastName.delete(0, END)
        entryFirstName.delete(0, END)
        entryMiddleName.delete(0, END)
        entryBirthDate.entry.delete(0, END)  # Clear the date entry
        entryGender.set('')  # Clear the
        entryContactNumber.delete(0, END)
        entryCompanyName.delete(0, END)  # Clear the company name combobox

def update_data():
    input_id = entryIDnumber.get()
    for entry in saved_data:
        if entry["ID Number"] == input_id:
            entry["Last Name"] = entryLastName.get()
            entry["First Name"] = entryFirstName.get()
            entry["Middle Name"] = entryMiddleName.get()

            birth_date_str = entryBirthDate.entry.get()  # Use .value to get the date
            try:
                entry["Birth Date"] = datetime.datetime.strptime(birth_date_str, "%Y-%m-%d").date()
            except ValueError:
                labePrintData.config(text="Invalid birth date format. Use YYYY-MM-DD.")
                return
            
            entry["Gender"] = entryGender.get()
            entry["Contact Number"] = entryContactNumber.get()
            entry["Company Name"] = entryCompanyName.get()
            labePrintData.config(text="Data updated successfully.")
    return

def auto_generate_id():
    entryIDnumber.delete(0, END)  # Clear the entry field
    formatted_id = f"ID{len(saved_data) + 1:04d}" # Generate ID in the format ID-0001, ID-0002, etc.
    return formatted_id




buttonSave = tb.Button(root, text="Save Data", bootstyle="success", command=save_data)
buttonSave.place(x=250, y=900, anchor="w")

buttonPrint = tb.Button(root, text="Print Data", bootstyle="info", command=print_saved_data)
buttonPrint.place(x=370, y=900, anchor="w")

buttonSearch = tb.Button(root, text="Search Data", bootstyle="warning", command=SearchData)
buttonSearch.place(x=500, y=900, anchor="w")

buttonUpdate = tb.Button(root, text="Update Data", bootstyle="primary", command=update_data)
buttonUpdate.place(x=620, y=900, anchor="w")

buttonAutoID = tb.Button(root, text="Auto Generate ID Number", bootstyle="secondary", command=lambda: entryIDnumber.insert(0, auto_generate_id()))
buttonAutoID.place(x=250, y=100, anchor="w")

root.mainloop()

'''
- DONE = Fix the search function to populate the form with the found data.
- Add an update function to modify existing records.
- Ensure the form clears after saving or updating data.
- Add error handling for date parsing and empty fields.
- Use a global list to store saved data.
- Fix saving duplicate ID numbers.
'''