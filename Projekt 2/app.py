from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from functions import *

root = Tk()
root.title("Biometria - Projekt 2 - Rozpoznawanie człowieka na podstawie obrazu tęczówki")
root.geometry('1000x700')

iris1 = None
iris2 = None

kod1 = None
kod2 = None

frame = Frame(root)
frame.pack(pady=20, padx=20)

load_button1 = Button(frame, text="Load Iris 1", command=lambda: left(canvas1, fig1, canvas2, fig2, canvas3, fig3, label))
load_button1.grid(row=0, column=0, padx=10, pady=10)

load_button2 = Button(frame, text="Load Iris 2", command=lambda: right(canvas4, fig4, canvas5, fig5, canvas6, fig6, label))
load_button2.grid(row=0, column=1, padx=10, pady=10)

plot_button = Button(frame, text="Compare", command= lambda: compare(label))
plot_button.grid(row=0, column=2, padx=10, pady=10)

label = Label(frame, text="")
label.grid(row=1, column=2, padx=10, pady=10)

col1 = Frame(frame)
col1.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

fig1 = Figure(figsize=(5, 4), dpi=100)
canvas1 = FigureCanvasTkAgg(fig1, master=col1)
canvas_widget1 = canvas1.get_tk_widget()
canvas_widget1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

fig2 = Figure(figsize=(5, 4), dpi=100)
canvas2 = FigureCanvasTkAgg(fig2, master=col1)
canvas_widget2 = canvas2.get_tk_widget()
canvas_widget2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

fig3 = Figure(figsize=(5, 4), dpi=100)
canvas3 = FigureCanvasTkAgg(fig3, master=col1)
canvas_widget3 = canvas3.get_tk_widget()
canvas_widget3.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

col1.grid_rowconfigure(0, weight=1)
col1.grid_rowconfigure(1, weight=1)
col1.grid_rowconfigure(2, weight=1)

col2 = Frame(frame)
col2.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

fig4 = Figure(figsize=(5, 4), dpi=100)
canvas4 = FigureCanvasTkAgg(fig4, master=col2)
canvas_widget4 = canvas4.get_tk_widget()
canvas_widget4.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

fig5 = Figure(figsize=(5, 4), dpi=100)
canvas5 = FigureCanvasTkAgg(fig5, master=col2)
canvas_widget5 = canvas5.get_tk_widget()
canvas_widget5.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

fig6 = Figure(figsize=(5, 4), dpi=100)
canvas6 = FigureCanvasTkAgg(fig6, master=col2)
canvas_widget6 = canvas6.get_tk_widget()
canvas_widget6.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

col2.grid_rowconfigure(0, weight=1)
col2.grid_rowconfigure(1, weight=1)
col2.grid_rowconfigure(2, weight=1)

col1.grid_columnconfigure(0, weight=1)
col2.grid_columnconfigure(0, weight=1)

frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

root.mainloop()
