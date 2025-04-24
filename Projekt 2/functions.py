from tkinter import filedialog
from PIL import Image
import numpy as np
from collections import deque
import matplotlib.patches as patches

def read_image():
    file_path = filedialog.askopenfilename(title="Select Image",
                                           filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        image = Image.open(file_path)
        pixel_matrix = np.array(image)
        return image, pixel_matrix

def show_image_ax(pixel_matrix, ax, canvas):
    ax.clear()
    ax.imshow(pixel_matrix, cmap='gray', aspect='equal')
    ax.axis('off')
    ax.grid(True)

def change_grey(pixel_matrix):
    n, m, _ = pixel_matrix.shape
    grey_pixel_matrix = np.zeros((n, m), dtype=float)
    for i in range(n):
        for j in range(m):
            r, g, b = pixel_matrix[i, j]
            s = (int(r) + int(g) + int(b)) / 3
            grey_pixel_matrix[i, j] = s
    min_val = np.min(grey_pixel_matrix)
    max_val = np.max(grey_pixel_matrix)
    if max_val != min_val:
        grey_pixel_matrix = (grey_pixel_matrix - min_val) / (max_val - min_val) * 255
    else:
        grey_pixel_matrix.fill(0)
    return grey_pixel_matrix.astype(np.uint8)

def countP(iris, pupil_cutoff=5.5, iris_cutoff=1.4):
    P = np.mean(iris)
    p_i = P / iris_cutoff
    p_p = P / pupil_cutoff
    return P, p_i, p_p

def binary(pixel_matrix, cut_off):
    binary_pixel_matrix = np.where(pixel_matrix >= cut_off, 255, 0)
    return binary_pixel_matrix

def convert():
    image, iris = read_image()
    iris = iris[:-1, :]
    image = Image.fromarray(iris)
    iris_grey = change_grey(iris)
    P, p_i, p_p = countP(iris_grey)
    binary_iris = binary(iris_grey, p_i)
    binary_pupil = binary(iris_grey, p_p)
    return image, iris_grey, binary_iris, binary_pupil

def inverse(matrix):
    return np.where(matrix == 0, 1, 0)

def fill_holes(binary_image):
    filled = np.zeros_like(binary_image, dtype=bool)
    visited = np.zeros_like(binary_image, dtype=bool)
    h, w = binary_image.shape
    queue = deque()
    for y in range(h):
        for x in [0, w - 1]:
            if binary_image[y, x] == 0 and not visited[y, x]:
                queue.append((y, x))
                visited[y, x] = True
    for x in range(w):
        for y in [0, h - 1]:
            if binary_image[y, x] == 0 and not visited[y, x]:
                queue.append((y, x))
                visited[y, x] = True
    while queue:
        y, x = queue.popleft()
        filled[y, x] = True
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and binary_image[ny, nx] == 0 and not visited[ny, nx]:
                queue.append((ny, nx))
                visited[ny, nx] = True
    holes = ~filled & (binary_image == 0)
    output = binary_image.copy()
    output[holes] = 1
    return output

def erode_2d(image, kernel_size=3):
    padded = np.pad(image, kernel_size // 2, mode='constant', constant_values=0)
    output = np.zeros_like(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            window = padded[i:i + kernel_size, j:j + kernel_size]
            output[i, j] = 1 if np.all(window == 1) else 0
    return output

def projection_horizontal(pixel_matrix):
    return np.sum(pixel_matrix, axis=0)

def projection_vertical(pixel_matrix):
    return np.sum(pixel_matrix, axis=1)

def smooth_proj(sums, cut_off=100):
    return np.where(sums < cut_off, 0, sums)

def find_center(binary_pupil):
    clos_in = inverse(binary_pupil)
    filled = fill_holes(clos_in).astype(np.int8)
    erosion_100 = erode_2d(filled, int(0.07 * len(binary_pupil)))
    row_sum = projection_vertical(erosion_100)
    col_sum = projection_horizontal(erosion_100)
    row_sum_smooth = smooth_proj(row_sum, 0.3 * max(row_sum))
    col_sum_smooth = smooth_proj(col_sum, 0.3 * max(col_sum))
    if np.sum(col_sum_smooth) != 0:
        x_center = np.sum(col_sum_smooth * np.arange(erosion_100.shape[1])) / np.sum(col_sum_smooth)
        y_center = np.sum(row_sum_smooth * np.arange(erosion_100.shape[0])) / np.sum(row_sum_smooth)
    else:
        x_center, y_center = 0, 0
    return x_center, y_center

def find_changes(sums, center):
    pix_min = next((i for i in range(int(center), -1, -1) if sums[i] == 0), 0)
    pix_max = next((i for i in range(int(center), len(sums)) if sums[i] == 0), len(sums))
    r_min = center - pix_min
    r_max = pix_max - center
    return int(r_min), int(r_max)

def find_rad(binary, x_center, y_center):
    clos_in = inverse(binary)
    filled = fill_holes(clos_in).astype(np.int8)
    erosion_10 = erode_2d(filled, max(5, int(0.007 * len(binary))))
    row_sum = projection_vertical(erosion_10)
    col_sum = projection_horizontal(erosion_10)
    row_sum_smooth = smooth_proj(row_sum, 0.15 * max(row_sum))
    col_sum_smooth = smooth_proj(col_sum, 0.15 * max(col_sum))
    r_1, r_2 = find_changes(col_sum_smooth, x_center)
    r_3, r_4 = find_changes(row_sum_smooth, y_center)
    rad = np.median([r_1, r_2, r_3, r_4])
    return rad

def crop_convert(image, rad_iris, x_center, y_center):
    iris = np.array(image)
    n, m = iris.shape[:2]
    add = 0.06 * n
    xmin = max(x_center - rad_iris - add, 0)
    xmax = min(x_center + rad_iris + add, m)
    ymin = max(y_center - rad_iris - add, 0)
    ymax = min(y_center + rad_iris + add, n)
    cropped = image.crop((xmin, ymin, xmax, ymax))
    iris = np.array(cropped)
    iris_grey = change_grey(iris)
    P, p_i, p_p = countP(iris_grey, 4.9, 1)
    binary_iris = binary(iris_grey, p_i)
    binary_pupil = binary(iris_grey, p_p)
    return cropped, iris_grey, binary_iris, binary_pupil, xmin, ymin

def normalize_iris(image, x_center, y_center, r_pupil, r_iris, height=None, width=None):
    if height is None:
        height = int(np.round(r_iris - r_pupil))
    if width is None:
        width = int(round(2 * np.pi * r_iris))
    theta = np.linspace(0, 2 * np.pi, width)
    r = np.linspace(0, 1, height)
    r_grid, theta_grid = np.meshgrid(r, theta)
    x = x_center + (r_pupil + r_grid.T * (r_iris - r_pupil)) * np.cos(theta_grid.T)
    y = y_center + (r_pupil + r_grid.T * (r_iris - r_pupil)) * np.sin(theta_grid.T)
    x = np.clip(x, 0, image.shape[1] - 1)
    y = np.clip(y, 0, image.shape[0] - 1)
    x0 = np.floor(x).astype(int)
    x1 = np.ceil(x).astype(int)
    y0 = np.floor(y).astype(int)
    y1 = np.ceil(y).astype(int)
    ia = image[y0, x0]
    ib = image[y1, x0]
    ic = image[y0, x1]
    id = image[y1, x1]
    wa = (x1 - x) * (y1 - y)
    wb = (x1 - x) * (y - y0)
    wc = (x - x0) * (y1 - y)
    wd = (x - x0) * (y - y0)
    result = wa * ia + wb * ib + wc * ic + wd * id
    return result


def koduj_iris(iris_rect, liczba_pasm=8, liczba_punktow=128, margines=0.2, f=None):
    wysokosc, szerokosc = iris_rect.shape
    r_start = int(margines * wysokosc)
    r_end = int((1 - margines) * wysokosc)
    pas_wysokosc = (r_end - r_start) // liczba_pasm
    if f is None:
        f = (0.07 * pas_wysokosc)
    theta_idx = np.linspace(0, szerokosc - 1, liczba_punktow).astype(int)
    sigma = 0.5 * np.pi * f
    iris_code = []
    for i in range(liczba_pasm):
        start = r_start + i * pas_wysokosc
        end = start + pas_wysokosc
        pas = iris_rect[start:end, :]
        cechy_1d = []
        for t in theta_idx:
            kolumna = pas[:, t]
            r = np.arange(len(kolumna))
            gauss = np.exp(-0.5 * ((r - len(kolumna) // 2) / sigma) ** 2)
            gauss /= np.sum(gauss)
            wartosc = np.sum(gauss * kolumna)
            cechy_1d.append(wartosc)
        cechy_1d = np.array(cechy_1d)
        f = (0.1 * len(cechy_1d))
        sigma = 0.5 * np.pi * f
        x = np.arange(-len(cechy_1d) // 2, len(cechy_1d) // 2)
        gabor_real = np.exp(-x ** 2 / (2 * sigma ** 2)) * np.cos(2 * np.pi * f * x)
        gabor_real = gabor_real / np.max(np.abs(gabor_real))
        gabor_odpowiedz = np.convolve(cechy_1d, gabor_real, mode='same')
        kod_binarny = (gabor_odpowiedz > 0).astype(int)
        iris_code.append(kod_binarny)
    iris_code = np.array(iris_code)
    return iris_code


def full_process(canvas1, fig1, canvas2, fig2, canvas3, fig3, label):
    label.grid_remove()
    image, iris_grey, binary_iris, binary_pupil = convert()
    x_center, y_center = find_center(binary_pupil)
    cut_off = 5.5
    while x_center == 0 and y_center == 0:
        cut_off -= 0.1
        P, p_i, p_p = countP(iris_grey, cut_off)
        binary_pupil = binary(iris_grey, p_p)
        x_center, y_center = find_center(binary_pupil)
    rad = find_rad(binary_pupil, x_center, y_center)
    rad_iris = find_rad(binary_iris, x_center, y_center)
    cropped, iris_grey, binary_iris, binary_pupil, xmin, ymin = crop_convert(image, rad_iris, x_center, y_center)
    x_center_cropped, y_center_cropped = find_center(binary_pupil)
    cut_off = 5.5
    while x_center_cropped == 0 and y_center_cropped == 0:
        cut_off -= 0.1
        P, p_i, p_p = countP(iris_grey, cut_off)
        binary_pupil = binary(iris_grey, p_p)
        x_center_cropped, y_center_cropped = find_center(binary_pupil)
    rad_cropped = find_rad(binary_pupil, x_center_cropped, y_center_cropped)
    rad_iris_cropped = find_rad(binary_iris, x_center_cropped, y_center_cropped)
    fig1.clear()
    ax = fig1.add_subplot(111)
    ax.imshow(iris_grey, cmap='gray', aspect='equal')
    ax.axis('off')
    ax.grid(True)
    ax.plot(x_center_cropped, y_center_cropped, 'ro', markersize=5)
    circle = patches.Circle((x_center_cropped, y_center_cropped), rad_cropped, edgecolor='yellow', facecolor='none', linewidth=2)
    ax.add_patch(circle)
    circle2 = patches.Circle((x_center_cropped, y_center_cropped), rad_iris_cropped, edgecolor='pink', facecolor='none', linewidth=2)
    ax.add_patch(circle2)
    fig1.tight_layout()
    canvas1.draw()
    normalized_cropped = normalize_iris(iris_grey, x_center_cropped, y_center_cropped, rad_cropped, rad_iris_cropped)
    fig2.clear()
    ax = fig2.add_subplot(111)
    ax.imshow(normalized_cropped, cmap='gray', aspect='equal')
    ax.axis('off')
    ax.grid(True)
    fig2.tight_layout()
    canvas2.draw()
    kod = koduj_iris(normalized_cropped)
    fig3.clear()
    ax = fig3.add_subplot(111)
    ax.imshow(kod, cmap='gray', aspect='equal')
    ax.set_title("Iris code (8 pasów × 128 bitów)")
    ax.axis('off')
    ax.grid(True)
    fig3.tight_layout()
    canvas3.draw()
    return kod


def hamming_distance(code1, code2):
    assert code1.shape == code2.shape, "Kody muszą mieć ten sam kształt"
    return np.sum(code1 != code2) / code1.size


def compare(label):
    distance = hamming_distance(kod1, kod2)
    label.config(text=f"Hamming distance between irises: {distance:.2f}")
    label.grid()


def left(canvas1, fig1, canvas2, fig2, canvas3, fig3, label):
    global kod1
    kod1 = full_process(canvas1, fig1, canvas2, fig2, canvas3, fig3, label)


def right(canvas1, fig1, canvas2, fig2, canvas3, fig3, label):
    global kod2
    kod2 = full_process(canvas1, fig1, canvas2, fig2, canvas3, fig3, label)


