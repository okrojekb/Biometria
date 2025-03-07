# Python program to remove widgets
# from grid in tkinter

# Import the library tkinter
from tkinter import *

# Create a GUI app
app = Tk()

# Creating a function for removing widgets from grid
def remove(widget1, widget2):
	widget1.grid_remove()
	widget2.grid_remove()

# Creating a function for making widget visible again
def display(widget1, widget2):
	widget1.grid(column=0, row=3, padx=10, pady=10)
	widget2.grid(column=0, row=4, padx=10, pady=10)

# Button widgets
b1 = Button(app, text="Vinayak")
b1.grid(column=0, row=3, padx=10, pady=10)

# Label Widgets
l1 = Label(app, text="Rai")
l1.grid(column=0, row=4, padx=10, pady=10)

# Create and show button with remove() function
remove_btn = Button(app, text="Remove widgets",
					command=lambda: remove(b1, l1))
remove_btn.grid(column=0, row=0, padx=10, pady=10)

# Create and show button with display() function
display_btn = Button(app, text="Display widgets",
					command=lambda: display(b1, l1))
display_btn.grid(column=0, row=1, padx=10, pady=10)

# Make infinite loop for displaying app on screen
app.mainloop()
