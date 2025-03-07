# Import Module
from tkinter import *

from matplotlib import pyplot as plt


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


from functions import *

# create root window
root = Tk()

# root window title and dimension
root.title("Biometria - Projekt 1 - przetwarzanie obrazów")

# Set geometry (widthxheight)
root.geometry('800x500')

menu = Menu(root)
upload = Menu(menu)
pixels = Menu(menu)
filters = Menu(menu)
upload.add_command(label='File')
pixels.add_command(label="Brightness")
filters.add_command(label="Roberts cross")
menu.add_cascade(label='New', menu=upload)
menu.add_cascade(label='Pixel transformations', menu=pixels)
menu.add_cascade(label='Filters', menu=filters)

root.config(menu=menu)

lbl = Label(root, text="Wybierz obraz do przetworzenia")
lbl.grid()


def clicked():
    lbl.configure(text="I just got clicked")




# button widget with red color text
# inside
btn = Button(root, text="Załaduj zdjęcie",
             fg="red", command=clicked)
# set Button grid
btn.grid(column=1, row=0)

sl = Scale(root, from_=-255, to=255, orient=HORIZONTAL)

sl.grid(column=1, row=1)

fig = Figure(figsize=(5, 4), dpi=100)
#
# Embed the Figure into Tkinter using FigureCanvasTkAgg
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=TOP, fill=BOTH, expand=True)

# Add a button to re-plot the graph (for demonstration purposes)
button = tk.Button(root, text="Plot Graph", command=plot_graph)
button.pack(side=BOTTOM)



#
# # fig = Figure(figsize=(5, 4), dpi=100)
# fig, axes = plt.subplots(2,2, figsize=(10, 10))
# # Embed the Figure into Tkinter using FigureCanvasTkAgg
# canvas = FigureCanvasTkAgg(fig, master=root)
# canvas_widget = canvas.get_tk_widget()
# canvas_widget.pack(side=TOP, fill=BOTH, expand=True)
# pixel_matrix = read_image('cat2.bmp')
# # Add a button to re-plot the graph (for demonstration purposes)
# button = Button(root, text="Plot Graph", command=show_image(pixel_matrix))
# button.pack(side=BOTTOM)
#
#
#
#


# all widgets will be here
# Execute Tkinter
root.mainloop()


#
# #
# def plot_graph():
#     # Clear the figure if there's a previous plot
#     fig.clear()
#
#     # Add a new plot to the figure
#     ax = fig.add_subplot(111)
#     x = np.linspace(0, 10, 100)
#     y = np.sin(x)
#     ax.plot(x, y, label="sin(x)", color="blue")
#     ax.set_title("Sine Wave")
#     ax.set_xlabel("X-axis")
#     ax.set_ylabel("Y-axis")
#     ax.legend()
#
#     # Redraw the canvas with the updated figure
#     canvas.draw()
# #
# # # Create the main Tkinter window
# # root = tk.Tk()
# # root.title("Matplotlib in Tkinter Example")
# #
# # # Create a Figure object for Matplotlib
# # fig = Figure(figsize=(5, 4), dpi=100)
# #
# # # Embed the Figure into Tkinter using FigureCanvasTkAgg
# # canvas = FigureCanvasTkAgg(fig, master=root)
# # canvas_widget = canvas.get_tk_widget()
# # canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
# #
# # # Add a button to re-plot the graph (for demonstration purposes)
# # button = tk.Button(root, text="Plot Graph", command=plot_graph)
# # button.pack(side=tk.BOTTOM)
# #
# # # Run the Tkinter main loop
# # root.mainloop()
# #
