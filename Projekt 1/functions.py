# Funkcja do wczytania obrazu
from tkinter import filedialog

import numpy as np
from PIL import Image  # Do obsługi obrazów


# from app2 import pixel_matrix_grey


#
# def read_image(file):
#     image = Image.open(file)
#     pixel_matrix = np.array(image)
#     n, m = pixel_matrix.shape[0], pixel_matrix.shape[1]
#     return pixel_matrix, n, m


# Funkcja do wyświetlenia obrazu (w Tkinter)
def show_image_tkinter(matrix, fig, canvas):
    print(matrix.shape)
    fig.clear()  # Czyść poprzednie wykresy
    ax = fig.add_subplot(111)  # Dodaj subplot do rysowania obrazu
    ax.imshow(matrix)
    ax.axis('off')  # Wyłącz osie
    canvas.draw()  # Odśwież płótno


def load_image(fig, canvas, lbl):
    # Wybór pliku za pomocą filedialog
    filepath = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if filepath:
        image = Image.open(filepath)
        global pixel_matrix
        pixel_matrix = np.array(image)
        # Wyświetlenie obrazu w Tkinter
        show_image_tkinter(pixel_matrix, fig, canvas)
        # lbl.configure(text="załadowani")
        lbl.grid_remove()


# Funkcja zapisująca obraz do pliku
def save_image(root, lbl_status):
    # Wybór lokalizacji i nazwy pliku do zapisu
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
    )
    if file_path:
        pm = pixel_matrix_2.astype(np.uint8)
        # Konwersja macierzy pikseli z powrotem na obraz
        image = Image.fromarray(pm)
        image.save(file_path)
        # Zapisanie obrazu do pliku .bmp        pixel_matrix_2.save(file_path)
        show_temporary_message(f"Obraz zapisano jako: {file_path}", root, lbl_status)


def show_temporary_message(message, root, lbl_status):
    lbl_status.config(text=message)  # Ustawienie tekstu komunikatu
    lbl_status.grid_remove()
    root.after(5000, lambda: hide_message(lbl_status))  # Ukrycie komunikatu po 5000 ms (5 sekund)

    # Funkcja ukrywająca komunikat


def hide_message(lbl_status):
    # lbl_status.config(text="")
    lbl_status.grid_remove()


# def save_image(pixel_matrix, output_file):
#     pixel_matrix = pixel_matrix.astype(np.uint8)
#     # Konwersja macierzy pikseli z powrotem na obraz
#     image = Image.fromarray(pixel_matrix)
#     # Zapisanie obrazu do pliku .bmp
#     image.save(output_file, format='BMP')


def in_range(x):
    x = max(0, x)
    x = min(x, 255)
    return x


def change_grey(slider, fig, canvas, show=1):
    global pixel_matrix_2
    global pixel_matrix_grey
    global sl_func
    sl_func = -1
    slider.grid_remove()
    pixel_matrix_2 = np.zeros((pixel_matrix.shape[0], pixel_matrix.shape[1], 3), dtype=int)
    for i in range(pixel_matrix.shape[0]):
        for j in range(pixel_matrix.shape[1]):
            # r, g, b = pixel_matrix[i,j]
            s = np.mean(pixel_matrix[i, j])
            pixel_matrix_2[i, j] = [s, s, s]
    pixel_matrix_grey = pixel_matrix_2.copy()
    if show == 1:
        show_image_tkinter(pixel_matrix_2, fig, canvas)

    # return grey_pixel_matrix


# %%
# def add_in_range(x, add):
#     x += add
#     x = max(0,x)
#     x=min(x, 255)
#     return x

def brigthness_change(slider, fig, canvas):
    slider.config(from_=-255, to=255)
    slider.config(label="Regulacja jasności")

    slider.grid()
    level = slider.get()

    global pixel_matrix_2
    n = pixel_matrix.shape[0]
    m = pixel_matrix.shape[1]
    pixel_matrix_2 = np.zeros((n, m, 3), dtype=int)
    global sl_func
    sl_func = 0
    for i in range(n):
        for j in range(m):
            r, g, b = pixel_matrix[i, j]
            r += level
            g += level
            b += level
            r = in_range(r)
            g = in_range(g)
            b = in_range(b)

            pixel_matrix_2[i, j] = [r, g, b]
    show_image_tkinter(pixel_matrix_2, fig, canvas)


def slider_function(value, slider, fig, canvas):
    if sl_func < 0:
        slider.grid_remove()
    elif sl_func == 0:
        slider.config(label="Regulacja jasności")
        brigthness_change(slider, fig, canvas)
    elif sl_func == 1:
        slider.config(label="Regulacja kontrastu")
        contrast_change(slider, fig, canvas)
    elif sl_func == 2:
        slider.config(label="Regulacja progu odcięcia")
        binary(slider, fig, canvas)


def contrast_change(slider, fig, canvas):
    slider.config(from_=-10, to=10)
    slider.config(label="Regulacja kontrastu")

    slider.grid()
    global pixel_matrix_2
    level = slider.get()
    n = pixel_matrix.shape[0]
    m = pixel_matrix.shape[1]
    maxI = np.max(pixel_matrix)
    pixel_matrix_2 = np.zeros((n, m, 3), dtype=int)
    global sl_func
    sl_func = 1
    if level < 0:
        level = 1 / (-level)
    for i in range(n):
        for j in range(m):
            r, g, b = pixel_matrix[i, j]
            r = ((r / maxI) ** level) * 255
            g = ((g / maxI) ** level) * 255
            b = ((b / maxI) ** level) * 255
            r = in_range(r)
            g = in_range(g)
            b = in_range(b)
            pixel_matrix_2[i, j] = [r, g, b]
    show_image_tkinter(pixel_matrix_2, fig, canvas)


def negate_in_range(x):
    x = 255 - x
    # print(x)
    # x = max(0, x)
    # x = min(x, 255)
    in_range(x)
    return x


def negative(fig, canvas, slider):
    global pixel_matrix_2
    n = pixel_matrix.shape[0]
    m = pixel_matrix.shape[1]
    global sl_func
    sl_func = -1
    slider.grid_remove()
    pixel_matrix_2 = np.zeros((n, m, 3), dtype=int)
    # # contrast_pixel_matrix = contrast_pixel_matrix/255
    # minI = np.min(pixel_matrix)
    # maxI = np.max(pixel_matrix)
    # mean = np.mean(contrast_pixel_matrix)
    for i in range(n):
        for j in range(m):
            r, g, b = pixel_matrix[i, j]
            r = negate_in_range(r)
            g = negate_in_range(g)
            b = negate_in_range(b)

            pixel_matrix_2[i, j] = [r, g, b]
    show_image_tkinter(pixel_matrix_2, fig, canvas)


def b_in_range(x):
    x = 255 - x
    # print(x)
    # x = max(0, x)
    # x = min(x, 255)
    in_range(x)
    return x


def binary(slider, fig, canvas, show=1):
    global pixel_matrix_2
    n = pixel_matrix.shape[0]
    m = pixel_matrix.shape[1]
    slider.config(from_=0, to=255)
    slider.config(label="Regulacja progu odcięcia")

    slider.grid()
    global sl_func
    sl_func = 2
    cut_off = slider.get()
    pixel_matrix_2 = np.zeros((n, m, 3), dtype=int)
    change_grey(slider, 0, fig, canvas)
    sl_func = 2
    slider.config(from_=0, to=255)
    slider.grid()
    for i in range(n):
        for j in range(m):
            s = pixel_matrix_grey[i, j, 0]
            if s >= cut_off:
                s = 255
            else:
                s = 0
            pixel_matrix_2[i, j] = [s, s, s]

    global pixel_matrix_bin
    pixel_matrix_bin = pixel_matrix_2.copy()

    if show == 1:
        print("show")
        show_image_tkinter(pixel_matrix_2, fig, canvas)


def cal_weights_2(weights, i, j, mean):
    r_sum = 0
    g_sum = 0
    b_sum = 0
    for k in range(2):
        for l in range(2):
            r_sum += pixel_matrix[i - k, j - l, 0] * weights[k][l]
            g_sum += pixel_matrix[i - k, j - l, 1] * weights[k][l]
            b_sum += pixel_matrix[i - k, j - l, 2] * weights[k][l]

    if mean == 1:
        r_sum, g_sum, b_sum = normalize_weights(weights, r_sum, g_sum, b_sum)
        # w_sum = 0
        # for k in range(len(weights)):
        #     for l in range(len(weights[0])):
        #         w_sum += weights[k][l]
        #
        # r_sum /= w_sum
        # g_sum /= w_sum
        # b_sum /= w_sum

    r_sum = in_range(r_sum)
    g_sum = in_range(g_sum)
    b_sum = in_range(b_sum)
    pixel = [r_sum, g_sum, b_sum]
    return pixel


def normalize_weights(weights, r, g, b):
    w_sum = 0
    for k in range(len(weights)):
        for l in range(len(weights[0])):
            w_sum += weights[k][l]

    r /= w_sum
    g /= w_sum
    b /= w_sum
    return r, g, b


def cal_weights(size, weights, i, j, mean):
    r_sum = 0
    g_sum = 0
    b_sum = 0
    for k in range(-size, size + 1):
        for l in range(-size, size + 1):
            r_sum += pixel_matrix[i - k, j - l, 0] * weights[k + size][l + size]
            g_sum += pixel_matrix[i - k, j - l, 1] * weights[k + size][l + size]
            b_sum += pixel_matrix[i - k, j - l, 2] * weights[k + size][l + size]

    if mean == 1:
        r_sum, g_sum, b_sum = normalize_weights(weights, r_sum, g_sum, b_sum)
        # w_sum = 0
        # for k in range(len(weights)):
        #     for l in range(len(weights[0])):
        #         w_sum += weights[k][l]
        # r_sum /= w_sum
        # g_sum /= w_sum
        # b_sum /= w_sum

    r_sum = in_range(r_sum)
    g_sum = in_range(g_sum)
    b_sum = in_range(b_sum)
    pixel = [r_sum, g_sum, b_sum]
    return pixel


def use_filter(size, weights, fig, canvas, mean=1):
    global pixel_matrix_2
    n = pixel_matrix.shape[0]
    m = pixel_matrix.shape[1]
    pixel_matrix_2 = np.zeros((n, m, 3), dtype=int)
    if size == 2:
        for i in range(n - size):
            for j in range(m - size):
                pixel = cal_weights_2(weights, i, j, mean)
                pixel_matrix_2[i, j] = pixel
    else:
        size = (size - 1) // 2
        for i in range(size, n - size):
            for j in range(size, m - size):
                pixel = cal_weights(size, weights, i, j, mean)
                pixel_matrix_2[i, j] = pixel
    show_image_tkinter(pixel_matrix_2, fig, canvas)


def average_filter(size, fig, canvas, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7, rbtn9):
    # # weights = np.zeros((2*size+1, 2*size+1) , dtype=int)
    # allowed_values = [1, 2, 3, 5, 7, 9]
    # print(len(allowed_values) - 1)
    # slider.config(from_=0, to=(len(allowed_values) - 1))
    # slider.config(label="Wielkość maski")
    # slider.grid()
    rbtn1.grid()
    rbtn2.grid()
    rbtn3.grid()
    rbtn5.grid()
    rbtn7.grid()
    rbtn9.grid()

    global sl_func
    sl_func = -2

    if size == 2 == 0:
        weights = [[1, 1], [1, 1]]
    else:
        weights = []
        for i in range(size):
            weights_row = []
            for j in range(size):
                weights_row.append(1)
            weights.append(weights_row)
    use_filter(size, weights, fig, canvas)
