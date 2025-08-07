import ttkbootstrap as tb
from ttkbootstrap.constants import *

# Create main app window
app = tb.Window(themename="cosmo")
app.title("Toggle UI Elements Example")
app.geometry("400x300")

# Create a parent frame (like a <div> in HTML)
container = tb.Frame(app)
container.pack(fill=BOTH, expand=YES, padx=10, pady=10)

# Create two different frames (blocks) that we will toggle
frame1 = tb.Frame(container)
label1 = tb.Label(frame1, text="This is Frame 1", font=("Helvetica", 16))
label1.pack(pady=20)

frame2 = tb.Frame(container)
label2 = tb.Label(frame2, text="This is Frame 2", font=("Helvetica", 16))
label2.pack(pady=20)

# Function to show only one frame
def show_frame(frame_to_show):
    # Hide all frames first
    for widget in container.winfo_children():
        widget.pack_forget()
    # Show the selected frame
    frame_to_show.pack(fill=BOTH, expand=YES)

# Buttons to toggle between frames
btn_frame = tb.Frame(app)
btn_frame.pack(pady=10)

btn1 = tb.Button(btn_frame, text="Show Frame 1", command=lambda: show_frame(frame1))
btn1.pack(side=LEFT, padx=5)

btn2 = tb.Button(btn_frame, text="Show Frame 2", command=lambda: show_frame(frame2))
btn2.pack(side=LEFT, padx=5)

# Start with frame1 visible
show_frame(frame1)

app.mainloop()
