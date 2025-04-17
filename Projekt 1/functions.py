from tkinter import filedialog

import numpy as np
from PIL import Image


def menu_func(slider, fig, canvas, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7,
              rbtn9, func_nr, v, entry, error_label, button, label, save_btn):
    global sl_func
    sl_func = -1
    slider.set(0)
    entry.grid_remove()
    button.grid_remove()
    error_label.grid_remove()
    label.grid_remove()
    save_btn.grid()
    if func_nr < 6:
        rbtn1.grid_remove()
        rbtn2.grid_remove()
        rbtn3.grid_remove()
        rbtn5.grid_remove()
        rbtn7.grid_remove()
        rbtn9.grid_remove()
        if func_nr == 1:
            sl_func = -1
            slider.grid_remove()
            change_grey(fig, canvas, 1)
        elif func_nr == 4:
            sl_func = -1
            slider.grid_remove()
            negative(fig, canvas, slider)
        else:
            if func_nr == 2:
                sl_func = 0
            elif func_nr == 3:
                sl_func = 1
            else:
                sl_func = 2
            slider_function(0, slider, fig, canvas)
    elif func_nr == 9:
        rbtn1.grid_remove()
        rbtn2.grid_remove()
        rbtn3.grid_remove()
        rbtn5.grid_remove()
        rbtn7.grid_remove()
        rbtn9.grid_remove()
        slider.grid_remove()
        roberts_cross(fig, canvas)
    elif func_nr == 10:
        rbtn1.grid_remove()
        rbtn2.grid_remove()
        rbtn3.grid_remove()
        rbtn5.grid_remove()
        rbtn7.grid_remove()
        rbtn9.grid_remove()
        slider.grid_remove()
        sobel_operator(fig, canvas)
    elif func_nr == 16:
        rbtn1.grid_remove()
        rbtn2.grid_remove()
        rbtn3.grid_remove()
        rbtn5.grid_remove()
        rbtn7.grid_remove()
        rbtn9.grid_remove()
        slider.grid_remove()
        entry.grid()
        button.grid()
        error_label.grid()
        label.grid()
        apply_filter(fig, canvas, entry, error_label)
    elif func_nr > 10:
        rbtn1.grid_remove()
        rbtn2.grid_remove()
        rbtn3.grid_remove()
        rbtn5.grid_remove()
        rbtn7.grid_remove()
        rbtn9.grid_remove()
        slider.grid_remove()
        save_btn.grid_remove()
        if func_nr == 11:
            histogram(fig, canvas)
        elif func_nr == 12:
            histogram_col(fig, canvas)
        elif func_nr == 13:
            fig.clear()
            ax = fig.add_subplot(111)
            projection_horizontal(fig, canvas, ax)
        elif func_nr == 14:
            fig.clear()
            ax = fig.add_subplot(111)
            projection_vertical(fig, canvas, ax)

        elif func_nr == 15:
            projections(fig, canvas)
    else:
        rbtn1.grid()
        rbtn2.grid()
        rbtn3.grid()
        rbtn5.grid()
        rbtn7.grid()
        rbtn9.grid()
        slider.grid_remove()
        sl_func = -1
        v.set(1)
        if func_nr == 6:
            rbtn1.config(text='maska 1x1')
            rbtn2.config(text='maska 2x2')
            rbtn3.config(text='maska 3x3')
            rbtn5.config(text='maska 5x5')
            rbtn7.config(text='maska 7x7')
            rbtn9.config(text='maska 9x9')
            average_filter(1, fig, canvas, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7, rbtn9)
        elif func_nr == 7:
            rbtn1.config(text='b=1')
            rbtn2.config(text='b=2')
            rbtn3.config(text='b=3')
            rbtn5.config(text='b=4')
            rbtn7.config(text='b=5')
            rbtn9.config(text='b=6')
            gauss_filter(1, fig, canvas, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7, rbtn9)
        elif func_nr == 8:
            rbtn7.grid_remove()
            rbtn9.grid_remove()
            rbtn1.config(text='maska nr 1')
            rbtn2.config(text='maska nr 2')
            rbtn3.config(text='maska nr 3')
            rbtn5.config(text='maska nr 4')
            sharp_filter(1, fig, canvas, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7, rbtn9)


def show_image_tkinter(matrix, fig, canvas):
    fig.clear()
    ax = fig.add_subplot(111)

    ax.imshow(matrix)
    ax.axis('off')
    fig.tight_layout(pad=0)
    # global kept

    canvas.draw()


def load_image(fig, canvas, lbl):
    filepath = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if filepath:
        image = Image.open(filepath)
        global pixel_matrix
        global sl_func
        sl_func = -1
        pixel_matrix = np.array(image)
        show_image_tkinter(pixel_matrix, fig, canvas)

        lbl.grid_remove()


def save_image(root, lbl_status):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
    )
    if file_path:
        pm = pixel_matrix_2.astype(np.uint8)
        image = Image.fromarray(pm)
        image.save(file_path)
        show_temporary_message(f"Obraz zapisano jako: {file_path}", root, lbl_status)


def show_temporary_message(message, root, lbl_status):
    lbl_status.config(text=message)
    lbl_status.grid_remove()
    root.after(5000, lambda: hide_message(lbl_status))


def hide_message(lbl_status):
    lbl_status.grid_remove()


def in_range(x):
    x = max(0, x)
    x = min(x, 255)
    return x


def change_grey(fig, canvas, show=1):
    global pixel_matrix_2
    global pixel_matrix_grey
    global sl_func
    sl_func = -1
    pixel_matrix_2 = np.zeros((pixel_matrix.shape[0], pixel_matrix.shape[1], 3), dtype=int)
    for i in range(pixel_matrix.shape[0]):
        for j in range(pixel_matrix.shape[1]):
            s = np.mean(pixel_matrix[i, j])
            pixel_matrix_2[i, j] = [s, s, s]
    pixel_matrix_grey = pixel_matrix_2.copy()
    if show == 1:
        show_image_tkinter(pixel_matrix_2, fig, canvas)


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


def filter_func(v, fig, canvas, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7, rbtn9):
    if sl_func > -2:
        rbtn1.grid_remove()
        rbtn2.grid_remove()
        rbtn3.grid_remove()
        rbtn5.grid_remove()
        rbtn7.grid_remove()
        rbtn9.grid_remove()
    else:
        rbtn1.grid()
        rbtn2.grid()
        rbtn3.grid()
        rbtn5.grid()

        if sl_func == -2:
            rbtn7.grid()
            rbtn9.grid()
            rbtn1.config(text='maska 1x1')
            rbtn2.config(text='maska 2x2')
            rbtn3.config(text='maska 3x3')
            rbtn5.config(text='maska 5x5')
            rbtn7.config(text='maska 7x7')
            rbtn9.config(text='maska 9x9')
            average_filter(v, fig, canvas, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7, rbtn9)
        elif sl_func == -3:
            rbtn7.grid()
            rbtn9.grid()
            rbtn1.config(text='b=1')
            rbtn2.config(text='b=2')
            rbtn3.config(text='b=3')
            rbtn5.config(text='b=4')
            rbtn7.config(text='b=5')
            rbtn9.config(text='b=6')
            gauss_filter(v, fig, canvas, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7, rbtn9)
        elif sl_func == -4:
            rbtn7.grid_remove()
            rbtn9.grid_remove()
            rbtn1.config(text='maska nr 1')
            rbtn2.config(text='maska nr 2')
            rbtn3.config(text='maska nr 3')
            rbtn5.config(text='maska nr 4')
            sharp_filter(v, fig, canvas, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7, rbtn9)


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
    change_grey(0, fig, canvas)
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

    r_sum = in_range(r_sum)
    g_sum = in_range(g_sum)
    b_sum = in_range(b_sum)
    pixel = [r_sum, g_sum, b_sum]
    return pixel


def apply_filter(fig, canvas, entry, error_label):
    weights_input = entry.get()
    try:
        weights = np.array(eval(weights_input))
        size = len(weights)

        use_filter(size, weights, fig, canvas)

        error_label.config(text="")
    except Exception as e:
        error_label.config(text=f"Błąd: {e}")


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
    global sl_func
    sl_func = -2
    rbtn1.grid()
    rbtn2.grid()
    rbtn3.grid()
    rbtn5.grid()
    rbtn7.grid()
    rbtn9.grid()
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


def gauss_filter(b, fig, canvas, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7, rbtn9):
    global sl_func
    sl_func = -3
    rbtn1.grid()
    rbtn2.grid()
    rbtn3.grid()
    rbtn5.grid()
    rbtn7.grid()
    rbtn9.grid()
    weights = [[1, b, 1], [b, b ^ 2, b], [1, b, 1]]
    use_filter(3, weights, fig, canvas)


def sharp_filter(nr, fig, canvas, rbtn1, rbtn2, rbtn3, rbtn5, rbtn7, rbtn9):
    global sl_func
    sl_func = -4
    rbtn1.grid()
    rbtn2.grid()
    rbtn3.grid()
    rbtn5.grid()
    rbtn7.grid_remove()
    rbtn9.grid_remove()
    if nr == 1:
        weights = [[-1, -1, -1],
                   [-1, 9, -1],
                   [-1, -1, -1]]
    elif nr == 2:
        weights = [[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]]
    elif nr == 3:
        weights = [[1, -2, 1],
                   [-2, 5, -2],
                   [1, -2, 1]]
    else:
        weights = [[0, -1, 0],
                   [-1, 9, -1],
                   [0, -1, 0]]
    use_filter(3, weights, fig, canvas, 1)


def cal_conv(i, j):
    r_temp_1, g_temp_1, b_temp_1 = (
            pixel_matrix[i, j].astype(np.int32) - pixel_matrix[i + 1, j + 1].astype(np.int32)).astype(np.int32)
    r_temp_2, g_temp_2, b_temp_2 = (
            pixel_matrix[i, j + 1].astype(np.int32) - pixel_matrix[i + 1, j].astype(np.int32)).astype(np.int32)
    r = in_range(abs(r_temp_1) + abs(r_temp_2))
    g = in_range(abs(g_temp_1) + abs(g_temp_2))
    b = in_range(abs(b_temp_1) + abs(b_temp_2))
    pixel = [r, g, b]
    return pixel


def roberts_cross(fig, canvas):
    global sl_func
    sl_func = -1
    global pixel_matrix_2

    n = pixel_matrix.shape[0]
    m = pixel_matrix.shape[1]
    pixel_matrix_2 = np.zeros((pixel_matrix.shape[0], pixel_matrix.shape[1], 3), dtype=int)
    for i in range(n - 1):
        for j in range(m - 1):
            pixel = cal_conv(i, j)
            pixel_matrix_2[i, j] = pixel
    show_image_tkinter(pixel_matrix_2, fig, canvas)


def sobel_operator(fig, canvas):
    global sl_func
    sl_func = -1
    global pixel_matrix_2

    n = pixel_matrix.shape[0]
    m = pixel_matrix.shape[1]
    pixel_matrix_2 = np.zeros((n, m, 3), dtype=int)
    weightsx = [[-1, 0, 1],
                [-2, 0, 2],
                [-1, 0, 1]]
    weightsy = [[-1, -2, -1],
                [0, 0, 0],
                [1, 2, 1]]

    for i in range(n - 1):
        for j in range(m - 1):
            rx, gx, bx = cal_weights(1, weightsx, i, j, 0)
            ry, gy, by = cal_weights(1, weightsy, i, j, 0)
            r = int((rx ^ 2 + ry ^ 2) ** 0.5)
            g = int((gx ^ 2 + gy ^ 2) ** 0.5)
            b = int((bx ^ 2 + by ^ 2) ** 0.5)
            r = in_range(r)
            g = in_range(g)
            b = in_range(b)
            pixel_matrix_2[i, j] = [r, g, b]
    pixel_matrix_2 = (pixel_matrix_2 / pixel_matrix_2.max() * 255).astype(np.uint8)
    show_image_tkinter(pixel_matrix_2, fig, canvas)


def col_list(pixel_matrix, col):
    col_matrix = pixel_matrix[:, :, col]
    col_list = col_matrix.flatten()
    return col_list


def histogram(fig, canvas):
    change_grey(fig, canvas, 0)

    list_grey = col_list(pixel_matrix_grey, 0)
    fig.clear()
    ax = fig.add_subplot(111)
    ax.hist(list_grey, color='grey', bins=(max(list_grey) - min(list_grey)))
    ax.set_title('Histogram', fontsize=14)
    ax.set_xlabel('Wartości odcieni szarości', fontsize=12)
    ax.set_ylabel('Liczba pikseli', fontsize=12)
    fig.tight_layout()
    canvas.draw()


def histogram_col(fig, canvas):
    change_grey(fig, canvas, 0)
    list_grey = col_list(pixel_matrix_grey, 0)
    list_red = col_list(pixel_matrix, 0)
    list_green = col_list(pixel_matrix, 1)
    list_blue = col_list(pixel_matrix, 2)
    fig.clear()
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.hist(list_red, color='red', bins=max(list_red) - min(list_red))
    ax1.set_title('Histogram Red', fontsize=10)

    ax2 = fig.add_subplot(2, 2, 2)
    ax2.hist(list_green, color='green', bins=max(list_green) - min(list_green))
    ax2.set_title('Histogram Green', fontsize=10)

    ax3 = fig.add_subplot(2, 2, 3)
    ax3.hist(list_blue, color='blue', bins=max(list_blue) - min(list_blue))
    ax3.set_title('Histogram Blue', fontsize=10)

    ax4 = fig.add_subplot(2, 2, 4)
    ax4.hist(list_grey, color='grey', bins=max(list_grey) - min(list_grey))
    ax4.set_title('Histogram Brightness', fontsize=10)

    fig.subplots_adjust(hspace=0.4, wspace=0.4, left=0.1, right=0.9, top=0.9, bottom=0.1)
    canvas.draw()


def projection_horizontal(fig, canvas, ax):
    global sl_func
    sl_func = -1
    global pixel_matrix_2

    n = pixel_matrix.shape[0]
    m = pixel_matrix.shape[1]
    change_grey(fig, canvas, 0)
    sumsp = np.zeros(n, dtype=int)
    for i in range(n):
        for j in range(m):
            sumsp[i] += pixel_matrix_grey[i, j, 0]

    ax.plot(sumsp, range(len(sumsp)), color='grey')
    ax.fill_betweenx(range(n), 0, sumsp, color='grey')

    ax.set_title('Projekcja pozioma', fontsize=14)
    ax.set_title('Projekcja pozioma', fontsize=14)
    ax.set_xlabel('Suma jasności w wierszu', fontsize=12)
    ax.set_ylabel('Nr wiersza', fontsize=12)

    ax.xaxis.set_ticks_position('top')
    ax.yaxis.set_ticks_position('left')

    ax.set_xlim(0, max(sumsp))
    ax.set_ylim(0, n)
    ax.invert_yaxis()

    canvas.draw()


def projection_vertical(fig, canvas, ax):
    global sl_func
    sl_func = -1
    global pixel_matrix_2

    n = pixel_matrix.shape[0]
    m = pixel_matrix.shape[1]
    change_grey(fig, canvas, 0)
    sumsp = np.zeros(m, dtype=int)
    for i in range(m):
        for j in range(n):
            sumsp[i] += pixel_matrix_grey[j, i, 0]

    ax.plot(range(len(sumsp)), sumsp, color='grey')
    ax.fill_between(range(m), sumsp, color='grey')
    ax.set_title('Projekcja pionowa', fontsize=14)
    ax.set_ylim(0, np.max(sumsp))
    ax.set_xlim(0, len(sumsp))
    ax.set_xlabel('Nr kolumny', fontsize=12)
    ax.set_ylabel('Suma jasności w kolumnie', fontsize=12)
    ax.invert_yaxis()

    canvas.draw()


def show_image_tkinter_ax(matrix, fig, canvas, ax):
    ax.clear()
    ax.imshow(matrix)
    ax.axis('off')
    ax.set_xlim(0, matrix.shape[1])
    ax.set_ylim(matrix.shape[0], 0)

    canvas.draw()


def projections(fig, canvas):
    fig.clear()

    gs = fig.add_gridspec(
        2, 2,
        height_ratios=[3, 1],
        width_ratios=[3, 1]
    )

    ax1 = fig.add_subplot(gs[0, 0])
    show_image_tkinter_ax(pixel_matrix, fig, canvas, ax1)

    ax2 = fig.add_subplot(gs[0, 1])
    projection_horizontal(fig, canvas, ax2)

    ax3 = fig.add_subplot(gs[1, 0])
    projection_vertical(fig, canvas, ax3)

    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    fig.subplots_adjust(hspace=0.4, wspace=0.4, left=0.1, right=0.9, top=0.9, bottom=0.1)

    canvas.draw()

