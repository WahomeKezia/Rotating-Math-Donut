import pygame as pg
import math
import colorsys

pg.init()

white = (255, 255, 255)
black = (0, 0, 0)
hue = 0

WIDTH = 1920
HEIGHT = 1080

x_start, y_start = 0, 0

x_s = 10
y_s = 20

rows = HEIGHT // y_s
columns = WIDTH // x_s
screen_size = rows * columns

x_offset = columns / 2
y_offset = rows / 2

# Rotating animation
A, B = 0, 0

theta_spacing = 10
# We'll change phi_spacing later for faster rotation
phi_spacing = 5

# Brightness index
chars = ".,-~:;=!*#$@"

screen = pg.display.set_mode((WIDTH, HEIGHT))
display_surface = pg.display.set_mode((WIDTH, HEIGHT))

pg.display.set_caption('Spinning Donut')
font = pg.font.SysFont('Arial', 18, bold=True)

# Function to convert HSV to RGB
def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

# Function to display text
def text_display(letter, x_start, y_start):
    text = font.render(str(letter), True, hsv2rgb(hue, 1, 1))
    display_surface.blit(text, (x_start, y_start))

run = True
while run:

    screen.fill((black))

    z = [0] * screen_size
    b = [' '] * screen_size

    for j in range(0, 628, theta_spacing):  # 0 to 2pi
        for i in range(0, 628, phi_spacing):
            c = math.sin(i)
            d = math.cos(j)
            e = math.sin(A)
            f = math.sin(j)
            g = math.cos(A)
            h = d + 2
            D = 1 / (c * h * e + f * g + 5)
            l = math.cos(i)
            m = math.cos(B)
            n = math.sin(B)
            t = c * h * g - f * e
            # This is for 3D coordinate x after rotation
            x = int(x_offset + 40 * D * (l * h * m - t * n))
            # This is for 3D coordinate y after rotation
            y = int(y_offset + 20 * D * (l * h * n + t * m))
            o = int(x + columns * y)
            N = int(8 * ((f * e - c * d * g) * m - c * d * e - f * g - l * d * n))  # Brightness index
            if rows > y and y > 0 and x > 0 and columns > x and D > z[o]:
                z[o] = D
                b[o] = chars[N if N > 0 else 0]

    if y_start == rows * y_s - y_s:
        y_start = 0

    for i in range(len(b)):
        # For faster rotation, change the value to a higher one.
        A += 0.00004
        B += 0.00002
        if i == 0 or i % columns:
            text_display(b[i], x_start, y_start)
            x_start += x_s
        else:
            y_start += y_s
            x_start = 0
            text_display(b[i], x_start, y_start)
            x_start += x_s

    pg.display.update()

    hue += 0.005

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run = False
