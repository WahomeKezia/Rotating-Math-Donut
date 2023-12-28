import tkinter as tk
import math

A = 1
B = 1
R1 = 1
R2 = 2
K1 = 150
K2 = 5

def asciiframe():
    global A, B
    b = [" "] * 1760
    z = [0] * 1760

    A += 0.07
    B += 0.03

    cA, sA = math.cos(A), math.sin(A)
    cB, sB = math.cos(B), math.sin(B)

    for k in range(1760):
        b[k] = "\n" if k % 80 == 79 else " "
        z[k] = 0

    for j in range(0, int(6.28), int(0.07 * 100)):
        ct, st = math.cos(j / 100), math.sin(j / 100)
        for i in range(0, int(6.28 * 100), int(0.02 * 100)):
            sp, cp = math.sin(i / 100), math.cos(i / 100)
            h = ct + 2
            D = 1 / (sp * h * sA + st * cA + 5)
            t = sp * h * cA - st * sA

            x = int(40 + 30 * D * (cp * h * cB - t * sB))
            y = int(12 + 15 * D * (cp * h * sB + t * cB))
            o = x + 80 * y
            N = int(8 * ((st * sA - sp * ct * cA) * cB - sp * ct * sA - st * cA - cp * ct * sB))

            if 0 <= y < 22 and 0 <= x < 79 and D > z[o]:
                z[o] = D
                b[o] = ".,-~:;=!*#$@"[N if N > 0 else 0]

    pretag.config(text="".join(b))
    root.after(50, asciiframe)

def canvasframe():
    global A, B
    if tmr1 is None:
        A += 0.07
        B += 0.03

    cA, sA = math.cos(A), math.sin(A)
    cB, sB = math.cos(B), math.sin(B)

    canvas.delete("all")
    canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill='#000')

    for j in range(0, int(6.28 * 100), int(0.3 * 100)):
        ct, st = math.cos(j / 100), math.sin(j / 100)
        for i in range(0, int(6.28 * 100), int(0.1 * 100)):
            sp, cp = math.sin(i / 100), math.cos(i / 100)
            ox = R2 + R1 * ct
            oy = R1 * st

            x = int(ox * (cB * cp + sA * sB * sp) - oy * cA * sB)
            y = int(ox * (sB * cp - sA * cB * sp) + oy * cA * cB)
            ooz = 1 / (K2 + cA * ox * sp + sA * oy)
            xp = int(150 + K1 * ooz * x)
            yp = int(120 - K1 * ooz * y)

            L = 0.7 * (cp * ct * sB - cA * ct * sp - sA * st + cB * (cA * st - ct * sA * sp))
            if L > 0:
                canvas.create_rectangle(xp, yp, xp + 1.5, yp + 1.5, fill=f'rgba(255,255,255,{L})')

    root.after(50, canvasframe)

def anim1():
    global tmr1
    if tmr1 is None:
        tmr1 = True
        asciiframe()

def anim2():
    global tmr2
    if tmr2 is None:
        tmr2 = True
        canvasframe()

root = tk.Tk()
root.title("ASCII and Canvas Animation")

pretag = tk.Label(root, font=("Courier", 8), justify=tk.LEFT)
pretag.pack()

canvas = tk.Canvas(root, width=320, height=240)
canvas.pack()

tmr1 = None
tmr2 = None

ascii_button = tk.Button(root, text="Toggle ASCII Animation", command=anim1)
ascii_button.pack()

canvas_button = tk.Button(root, text="Toggle Canvas Animation", command=anim2)
canvas_button.pack()

root.protocol("WM_DELETE_WINDOW", root.destroy)
root.mainloop()
