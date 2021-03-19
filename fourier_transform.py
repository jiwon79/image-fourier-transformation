from math import cos, sin, pi
from tkinter import *
import time
#from img_to_function import *

def convert(centerx, centery, radius):
    return centerx-radius, centery-radius, centerx+radius, centery+radius


def integrate(g):
    # integrate g(t) from 0 to 1
    h = 0.0001
    N = int(1/h)
    return h*sum(g(h*(i+0.5)) for i in range(N))


def complex_fourier_transform(x, y, N):
    # input x(t), y(t)
    # returns dictionary of complex fourier c c_i, where -N <= i <= N
    c = dict()
    for i in range(-N, N+1):
        real_func = lambda t: cos(2*pi*i*t)*x(t) + sin(2*pi*i*t)*y(t)
        imag_func = lambda t: -sin(2*pi*i*t)*x(t) + cos(2*pi*i*t)*y(t)
        c[i] = integrate(real_func) + integrate(imag_func) * 1j
    return c

# x = lambda t: img_function(t).x
# y = lambda t: img_function(t).y
x = lambda t: 50*cos(2*pi*t)+ 30*cos(6*pi*t) + 200
y = lambda t: 100*sin(2*pi*t)+200

N = 10
c = complex_fourier_transform(x, y, N)

window = Tk()
window.title("image fourier transformation")
window.geometry("600x400+100+100")
window.resizable(True, True)

canvas = Canvas(window, width=400, height=400, bg="white", bd=2)
canvas.pack()
window.update()

centers = dict()
centers[0] = 0
tmp = convert(0, 0, abs(c[0]))
canvas.create_oval(tmp[0], tmp[1], tmp[2], tmp[3], fill="")

for i in range(1, N+1):
    centers[i] = centers[1-i] + c[1-i]
    tmp = convert(centers[i].real, centers[i].imag, abs(c[i]))
    canvas.create_oval(tmp[0], tmp[1], tmp[2], tmp[3], fill="")
    
    centers[-i] = centers[i] + c[i]
    tmp = convert(centers[-i].real, centers[-i].imag, abs(c[-i]))
    canvas.create_oval(tmp[0], tmp[1], tmp[2], tmp[3], fill="")


for k in range(1000):
    t = k / 1000
    position = sum(c[i] * (cos(2*pi*i*t)+sin(2*pi*i*t)*1j) for i in range(-10, 11))
    canvas.create_oval(position.real, position.imag, position.real+1, position.imag+1, fill="blue")
    window.update()

time.sleep(1.5)
    


