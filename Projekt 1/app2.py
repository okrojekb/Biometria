# Import required modules
from tkinter import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from functions import *

# Create main window
root = Tk()
root.title("Biometria - Projekt 1 - przetwarzanie obrazów")
root.geometry('1000x700')

pixel_matrix = None
pixel_matrix_2 = None
pixel_matrix_grey = None
pixel_matrix_bin = None
global sl_func
sl_func = -1

# Create a menu bar
menu = Menu(root)
root.config(menu=menu)

# Submenus
upload_menu = Menu(menu, tearoff=0)
upload_menu.add_command(label='Załaduj plik', command=lambda: load_image(fig1, canvas1, lbl))
menu.add_cascade(label='Plik', menu=upload_menu)

pixels_menu = Menu(menu, tearoff=0)

pixels_menu.add_command(label="Konwersja do odcieni szarości",
                        command=lambda: menu_func(sl, fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7,
                                                  rbtn9, 1, v, entry, error_label,button, label))
pixels_menu.add_command(label="Korekta jasności",
                        command=lambda: menu_func(sl, fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7,
                                                  rbtn9, 2, v, entry, error_label,button, label))
pixels_menu.add_command(label="Korekta kontrastu",
                        command=lambda: menu_func(sl, fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7,
                                                  rbtn9, 3, v, entry, error_label,button, label))
pixels_menu.add_command(label="Negatyw",
                        command=lambda: menu_func(sl, fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7,
                                                  rbtn9, 4, v, entry, error_label,button, label))
pixels_menu.add_command(label="Binaryzacja",
                        command=lambda: menu_func(sl, fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7,
                                                  rbtn9, 5, v, entry, error_label,button, label))

menu.add_cascade(label="Operacje na pikselach", menu=pixels_menu)

filters_menu = Menu(menu, tearoff=0)

filters_menu.add_command(label="Filtr uśredniający",
                         command=lambda: menu_func(sl, fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7,
                                                   rbtn9, 6, v, entry, error_label,button, label))

filters_menu.add_command(label="Filtr Gaussa",
                         command=lambda: menu_func(sl, fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7,
                                                   rbtn9, 7, v, entry, error_label,button, label))
filters_menu.add_command(label="Filtr wyostrzający",
                         command=lambda: menu_func(sl, fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7,
                                                   rbtn9, 8, v, entry, error_label,button, label))
filters_menu.add_command(label="Wykrywanie krawędzi - krzyż Robertsa",
                         command=lambda: menu_func(sl, fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7,
                                                   rbtn9, 9, v, entry, error_label,button, label))

filters_menu.add_command(label="Wykrywanie krawędzi - operator Sobela",
                         command=lambda: menu_func(sl, fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7,
                                                   rbtn9, 10, v, entry, error_label,button, label))

filters_menu.add_command(label="Ustawienie dowolnych wag filtrów",
                         command=lambda: menu_func(sl, fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7,
                                                   rbtn9, 16, v, entry, error_label,button, label))

menu.add_cascade(label="Filtry", menu=filters_menu)

wykresy_menu = Menu(menu, tearoff=0)

wykresy_menu.add_command(label="Histogram",
                         command=lambda: menu_func(sl, fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7,
                                                   rbtn9, 11, v, entry, error_label,button, label))

wykresy_menu.add_command(label="Histogram kolorów",
                         command=lambda: menu_func(sl, fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7,
                                                   rbtn9, 12, v, entry, error_label,button, label))
wykresy_menu.add_command(label="Projekcja pozioma",
                         command=lambda: menu_func(sl, fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7,
                                                   rbtn9, 13, v, entry, error_label,button, label))
wykresy_menu.add_command(label="Projekcja pionowa",
                         command=lambda: menu_func(sl, fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7,
                                                   rbtn9, 14, v, entry, error_label,button, label))

wykresy_menu.add_command(label="Projekcja pozioma i pionowa",
                         command=lambda: menu_func(sl, fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7,
                                                   rbtn9, 15, v, entry, error_label,button, label))

menu.add_cascade(label="Wykresy", menu=wykresy_menu)

##################################################33
# Tworzenie figury matplotlib
fig1 = Figure(figsize=(6, 6), dpi=100)

canvas1 = FigureCanvasTkAgg(fig1, master=root)
canvas_widget1 = canvas1.get_tk_widget()
canvas_widget1.grid(column=0, row=2, columnspan=5, rowspan=6, padx=10, pady=10)

# Tworzenie figury matplotlib
fig2 = Figure(figsize=(6, 6), dpi=100)
canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas_widget2 = canvas2.get_tk_widget()
canvas_widget2.grid(column=5, row=2, columnspan=5, rowspan=6, padx=10, pady=10)

# Add label and slider for adjustments
lbl = Label(root, text="Wybierz obraz do przetworzenia", font=("Arial", 14))
lbl.grid(column=0, row=0, padx=10, pady=10)

sl = Scale(root, from_=-255, to=255, orient=VERTICAL, label="Regulacja jasności", length=300,
           command=lambda value: slider_function(value, sl, fig2, canvas2))
sl.set(0)
sl.grid(column=10, row=2, rowspan=5, padx=10, pady=10)
sl.grid_remove()

btn = Button(root, text="Załaduj zdjęcie", fg="red", command=lambda: load_image(fig1, canvas1, lbl))
btn.grid(column=0, row=1, padx=10, pady=10)

save_btn = Button(root, text="Zapisz obraz", command=lambda: save_image(root, lbl_status))
save_btn.grid(column=5, row=8, padx=10, pady=10)

# Etykieta statusu
lbl_status = Label(root, text="", font=("Arial", 12))  # Początkowo pusta
lbl_status.grid(column=6, row=8, padx=10, pady=10)
lbl_status.grid_remove()

v = IntVar()
v.set(1)  # Ustawiamy domyślną wartość na 1
rbtn1 = Radiobutton(root, text='maska 1x1', variable=v, value=1,
                    command=lambda: filter_func(v.get(), fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7, rbtn9))
rbtn2 = Radiobutton(root, text='maska 2x2', variable=v, value=2,
                    command=lambda: filter_func(v.get(), fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7, rbtn9))
rbtn3 = Radiobutton(root, text='maska 3x3', variable=v, value=3,
                    command=lambda: filter_func(v.get(), fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7, rbtn9))
rbtn5 = Radiobutton(root, text='maska 5x5', variable=v, value=5,
                    command=lambda: filter_func(v.get(), fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7, rbtn9))
rbtn7 = Radiobutton(root, text='maska 7x7', variable=v, value=7,
                    command=lambda: filter_func(v.get(), fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7, rbtn9))
rbtn9 = Radiobutton(root, text='maska 9x9', variable=v, value=9,
                    command=lambda: filter_func(v.get(), fig2, canvas2, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7, rbtn9))

rbtn1.grid(row=2, column=10, padx=10, pady=5, sticky=W)
rbtn2.grid(row=3, column=10, padx=10, pady=5, sticky=W)
rbtn3.grid(row=4, column=10, padx=10, pady=5, sticky=W)
rbtn5.grid(row=5, column=10, padx=10, pady=5, sticky=W)
rbtn7.grid(row=6, column=10, padx=10, pady=5, sticky=W)
rbtn9.grid(row=7, column=10, padx=10, pady=5, sticky=W)
rbtn1.grid_remove()
rbtn2.grid_remove()
rbtn3.grid_remove()
rbtn5.grid_remove()
rbtn7.grid_remove()
rbtn9.grid_remove()


label = Label(root, text="Wprowadź macierz wag (np. [[-1,0,1],[0,1,0],[-1,0,1]])")
label.grid_remove()


# Pole Entry do wpisywania wag
entry = Entry(root, width=50)
entry.grid_remove()


# Przycisk do uruchomienia funkcji
button = Button(root, text="Zastosuj filtr", command=lambda: apply_filter(fig2, canvas2, entry, error_label))  # Podaj odpowiednie fig, canvas
button.grid_remove()


error_label = Label(root, text="", fg="red")  # Komunikaty błędu wyświetlane na czerwono
error_label.grid_remove()

root.mainloop()
