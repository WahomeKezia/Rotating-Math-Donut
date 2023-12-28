import streamlit as st
import pygame as pg
import numpy as np
import math
import colorsys

white = (255, 255, 255)
black = (0, 0, 0)
hue = 0

WIDTH = 800
HEIGHT = 600

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
phi_spacing = 5

chars = ".,-~:;=!*#$@"

pg.init()
screen = pg.Surface((WIDTH, HEIGHT))

@st.cache(hash_funcs={pg.Surface: lambda _: None})
def render_donut():
    global A, B, hue, x_start, y_start  # Add global for y_start

    y_start = 0  # Initialize y_start

    z = [0] * screen_size
    b = [' '] * screen_size

    for j in range(0, 628, theta_spacing):
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
            x = int(x_offset + 40 * D * (l * h * m - t * n))
            y = int(y_offset + 20 * D * (l * h * n + t * m))
            o = int(x + columns * y)
            N = int(8 * ((f * e - c * d * g) * m - c * d * e - f * g - l * d * n))
            if rows > y and y > 0 and x > 0 and columns > x and D > z[o]:
                z[o] = D
                b[o] = chars[N if N > 0 else 0]

    if y_start == rows * y_s - y_s:
        y_start = 0

    for i in range(len(b)):
        A += 0.00004
        B += 0.00002
        if i == 0 or i % columns:
            x_start += x_s
        else:
            y_start += y_s
            x_start = 0

    hue += 0.005

    imgdata = pg.surfarray.array3d(screen)
    imgdata = imgdata.swapaxes(0, 1)

    return imgdata

st.title("Spinning Donut")
st.image(render_donut(), caption='Spinning Donut', use_column_width=True)
