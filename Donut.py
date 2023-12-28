import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import math

# Rotating animation
A, B = 0, 0

theta_spacing = 0.07
phi_spacing = 0.02

screen_size = 40
illumination = np.fromiter(".,-~:;=!*#$@", dtype="<U1")

R1 = 1
R2 = 2
K2 = 5
K1 = screen_size * K2 * 3 / (8 * (R1 + R2))

# Function to render the spinning donut
def render_donut(A, B):
    output = np.full((screen_size, screen_size), " ")
    zbuffer = np.zeros((screen_size, screen_size))

    cos_phi = np.cos(phi := np.arange(0, 2 * np.pi, phi_spacing))
    sin_phi = np.sin(phi)
    cos_theta = np.cos(theta := np.arange(0, 2 * np.pi, theta_spacing))
    sin_theta = np.sin(theta)
    circle_x = R2 + R1 * cos_theta
    circle_y = R1 * sin_theta

    x = (
        np.outer(cos_B * cos_phi + sin_A * sin_B * sin_phi, circle_x)
        - circle_y * cos_A * sin_B
    ).T
    y = (
        np.outer(sin_B * cos_phi - sin_A * cos_B * sin_phi, circle_x)
        + circle_y * cos_A * cos_B
    ).T
    z = (
        (K2 + cos_A * np.outer(sin_phi, circle_x)) + circle_y * sin_A
    ).T
    ooz = np.reciprocal(z)
    xp = (screen_size / 2 + K1 * ooz * x).astype(int)
    yp = (screen_size / 2 - K1 * ooz * y).astype(int)
    L1 = (
        ((np.outer(cos_phi, cos_theta) * sin_B) - cos_A * np.outer(sin_phi, cos_theta))
        - sin_A * sin_theta
    )
    L2 = cos_B * (cos_A * sin_theta - np.outer(sin_phi, cos_theta * sin_A))
    L = np.around(((L1 + L2) * 8)).astype(int).T
    mask_L = L >= 0
    chars = illumination[L]

    for i in range(90):
        mask = mask_L[i] & (ooz[i] > zbuffer[xp[i], yp[i]])

        zbuffer[xp[i], yp[i]] = np.where(mask, ooz[i], zbuffer[xp[i], yp[i]])
        output[xp[i], yp[i]] = np.where(mask, chars[i], output[xp[i], yp[i]])

    return output


st.title("Spinning Donut")

# Create a Matplotlib figure
fig, ax = plt.subplots()

# Function to update the Matplotlib plot
def update_plot(A, B):
    ax.clear()
    donut_frame = render_donut(A, B)

    # Customize the color map for the ASCII characters
    cmap = mcolors.ListedColormap(["black"] + list(mcolors.TABLEAU_COLORS.values()))
    bounds = [0] + list(range(1, len(illumination) + 1))
    norm = mcolors.BoundaryNorm(bounds, cmap.N, clip=True)

    # Display the donut frame using Matplotlib's imshow
    ax.imshow(
        donut_frame,
        cmap=cmap,
        norm=norm,
        interpolation="nearest",
        aspect="equal",
        extent=(-screen_size / 2, screen_size / 2, -screen_size / 2, screen_size / 2),
    )

# Streamlit slider widgets for controlling the rotation angles
A_slider = st.slider("A", 0.0, 2 * np.pi, 0.0, step=0.01)
B_slider = st.slider("B", 0.0, 2 * np.pi, 0.0, step=0.01)

# Update the plot with the current slider values
update_plot(A_slider, B_slider)

# Display the Matplotlib figure using Streamlit
st.pyplot(fig)
