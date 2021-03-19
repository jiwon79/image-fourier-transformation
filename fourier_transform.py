from math import cos, sin, pi
from tkinter import *
import time
from img_to_function import *

def integrate(g):
    # integrate g(t) from 0 to 1
    h = 0.0001
    N = int(1/h)
    return h*sum(g(h*(i+0.5)) for i in range(N))


def complex_fourier_transform(x, y, N):
    # input x(t), y(t)
    # returns dictionary of complex fourier constants c_i, where -N <= i <= N
    c = dict()
    for i in range(-N, N+1):
        real_func = lambda t: cos(2*pi*i*t)*x(t) + sin(2*pi*i*t)*y(t)
        imag_func = lambda t: -sin(2*pi*i*t)*x(t) + cos(2*pi*i*t)*y(t)
        c[i] = integrate(real_func) + integrate(imag_func) * 1j
    return c

# x = lambda t: img_function(t).x
# y = lambda t: img_function(t).y
x = lambda t: 50*cos(2*pi*t)+200 + 30*t
y = lambda t: 100*sin(2*pi*t)+200

constants = complex_fourier_transform(x, y, 1)

window = Tk()
window.title("image fourier transformation")
window.geometry("600x400+100+100")
window.resizable(True, True)

canvas = Canvas(window, width=400, height=400, bg="white", bd=2)
canvas.pack()
window.update()

for k in range(1000):
    t = k / 1000
    position = sum(constants[i] * (cos(2*pi*i*t)+sin(2*pi*i*t)*1j) for i in range(-10, 11))
    canvas.create_oval(position.real, position.imag, position.real+1, position.imag+1, fill="blue")
    window.update()

time.sleep(3)
    


