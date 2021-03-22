import cv2
from tkinter import *
from PIL import Image
from PIL import ImageTk
from math import cos, sin, pi

from classes import *
# from fourier_transform import *

############################ tkinter window ############################
window = Tk()
window.title("image fourier transformation")
window.geometry("1400x400+100+100")
window.resizable(False, False)

############################### functions ##############################
connectList = []

def segment_function(p1, p2, t): # 0 <= t <= 1
    return p1 + (p2-p1)*t


def img_function(t): # 0<= t <= 1
    global connectList
    
    idx = int(t*len(connectList)-1)
    para = t*len(connectList)-idx
    return segment_function(connectList[idx], connectList[idx+1], para)


# fourier functions
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


# action when click button
def convert_to_tkimage():
    global src
    global connectList
    
    # color img -> gray sclae -> outline
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    outline = cv2.Canny(gray, 100, 255)

    # points -> connect list
    connectList = connect_points(outline)
    draw_by_list(canvas_outline, connectList)

    # transform img form
    img = Image.fromarray(outline)
    imgtk = ImageTk.PhotoImage(image=img)

    label.config(image=imgtk)
    label.image = imgtk

    # fourier transformation
    x = lambda t: img_function(t).x
    y = lambda t: img_function(t).y

    constants = complex_fourier_transform(x, y, 10)

    window.update()

    for k in range(1000):
        t = k / 1000
        position = sum(constants[i] * (cos(2*pi*i*t)+sin(2*pi*i*t)*1j) for i in range(-10, 11))
        canvas_fourier.create_oval(position.real, position.imag, position.real+1, position.imag+1, fill="blue")
        window.update()

def nearest_point(outline, p):
    n = 1
    while True:
        for i in range(n):
            direction = [(n-i, i), (-i, n-i), (-n+i, -i), (i, -n+i)]
            for dir in direction:
                x, y = p.x + dir[0], p.y + dir[1]
                if 0 <= x < 400 and 0 <= y < 400:
                    if outline[y][x] == 255:
                        outline[y][x] = 254
                        return Point(x, y)
        n += 1

    

def connect_points(outline):
    # detect black point
    pointList = []
    for i in range(img_width):
        for j in range(img_height):
            if outline[j][i] == 255: # 0 : white, 255 : black
                pointList.append(Point(i, j))
    
    # connect near point
    connectList = [pointList[0]]
    while len(connectList) != len(pointList):
        point = connectList[-1]
        near = nearest_point(outline, point)
        connectList.append(near)
        
        print(len(connectList))
    connectList.append(connectList[0])
   
    return connectList


# GUI function
l = [Point(10,10), Point(100,50), Point(40,100), Point(80,90)]
def draw_by_list(canvas, l):
    for i in range(len(l)-1):
        canvas.create_line(l[i].x, l[i].y, l[i+1].x, l[i+1].y, fill="#476042", width=1)


# bilateral filter
############################## load img ###############################
src = cv2.imread("./img/lion.jpg")
img_width, img_height = 400, 400
src = cv2.resize(src, (img_width,  img_height))

# transform opencv(BGR) to tkinter(RGB)
img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)

# transform numpy array to img
img = Image.fromarray(img)
imgtk = ImageTk.PhotoImage(image=img)


################################ GUI ###################################
canvas_fourier = Canvas(window, width=img_width, height=img_height, bg="white", bd=2)
canvas_fourier.place(x=0, y=0)

canvas_outline = Canvas(window, width=img_width, height=img_height, bg="white", bd=2)
canvas_outline.place(x=400, y=0)


label = Label(window, image=imgtk)
label.place(x=800, y=0)
label.pack

button = Button(window, text="outline detection", command=convert_to_tkimage)
button.place(x=1200,y=0, width=200, height=400)
# button.pack(expand=True, fill='both')

window.mainloop()
