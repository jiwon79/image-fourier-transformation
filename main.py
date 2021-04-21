import cv2
from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
from math import cos, sin, pi
import random

from near_algorithm import *
from classes import *

############################ tkinter window ############################
window = Tk()
window.title("image fourier transformation")
window.geometry("1400x400+100+100")
window.resizable(False, False)

############################### functions ##############################
connectList = []

def segment_function(p1, p2, t): # 0 <= t <= 1
    return p1 + (p2-p1)*t

def connectlist_to_func(t): # 0 <= t <= 1
    global connectList
    
    idx = int(t*len(connectList)-1)
    para = t*len(connectList)-idx
    return segment_function(connectList[idx], connectList[idx+1], para)

def outline_action():
    global src
    global connectList
    
    # color img -> gray sclae -> outline
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    outline = cv2.Canny(gray, 100, 255)

    # points -> connect list
    connectList, cluster = connect_points(outline)
    draw_by_cluster(canvas_outline, cluster)
    
    # transform img form
    img = Image.fromarray(outline)
    imgtk = ImageTk.PhotoImage(image=img)
    label.config(image=imgtk)
    label.image = imgtk
    print("Outline Detection Finished")

def connect_points(outline):
    # detect black point
    pointList = []
    for i in range(img_width):
        for j in range(img_height):
            if outline[j][i] == 255: # 0 : white, 255 : black
                pointList.append(Point(i, j))
    
    # connect near point
    connectList = [pointList[0]]
    cluster = [[]]
    while len(connectList) != len(pointList):
        point = connectList[-1]
        near, cluster = nearest_point_cluster(outline, point, cluster)
        connectList.append(near)
    connectList.append(connectList[0])
   
    return connectList, cluster

########################### fourier functions ##########################

def integrate(g):
    # integrate g(t) from 0 to 1
    h = 0.001
    N = int(1/h)
    return h*sum(g(h*(i+0.5)) for i in range(N))

def complex_fourier_transform(x, y, N):
    # input x(t), y(t)
    # returns dictionary of complex fourier constants c_i, where -N <= i <= N
    c = dict()
    for i in range(-N, N+1):
        real_func = lambda t: cos(2*pi*i*t) * x(t) + sin(2*pi*i*t) * y(t)
        imag_func = lambda t: -sin(2*pi*i*t) * x(t) + cos(2*pi*i*t) * y(t)
        c[i] = integrate(real_func) + integrate(imag_func) * 1j
    return c

def fourier_action():
    # fourier transformation
    connectList.append(connectList[0])
    x = lambda t: connectlist_to_func(t).x
    y = lambda t: connectlist_to_func(t).y

    N = slider_N.get()
    c = complex_fourier_transform(x, y, N)

    window.update()

    centers = dict()
    circles = dict()
    arrows = dict()
    centers[0] = 0

    canvas_fourier.delete('all')

    for i in range(1, N+1):
        centers[i] = centers[1-i] + c[1-i]
        tmp = convert(centers[i].real, centers[i].imag, abs(c[i]))
        circles[i] = canvas_fourier.create_oval(tmp[0], tmp[1], tmp[2], tmp[3], fill="", outline = "#ff948c")
        arrows[i] = canvas_fourier.create_line(centers[1-i].real, centers[1-i].imag, centers[i].real, centers[i].imag, width=2)
        
        centers[-i] = centers[i] + c[i]
        tmp = convert(centers[-i].real, centers[-i].imag, abs(c[-i]))
        circles[-i] = canvas_fourier.create_oval(tmp[0], tmp[1], tmp[2], tmp[3], fill="", outline = "#ff948c")
        arrows[-i] = canvas_fourier.create_line(centers[i].real, centers[i].imag, centers[-i].real, centers[-i].imag, width=2)

    canvas_fourier.delete(arrows[1])
    position = centers[-N] + c[-N]
    arrows[N+1] = canvas_fourier.create_line(centers[-N].real, centers[-N].imag, position.real, position.imag)

    M = slider_M.get()

    for k in range(M):
        t = k / M
        for i in range(1, N+1):
            centers[i] = centers[1-i] + c[1-i] * (cos(2*pi*(1-i)*t) + 1j * sin(2*pi*(1-i)*t))
            tmp = convert(centers[i].real, centers[i].imag, abs(c[i]))
            canvas_fourier.coords(circles[i], tmp[0], tmp[1], tmp[2], tmp[3])
            canvas_fourier.coords(arrows[i], centers[1-i].real, centers[1-i].imag, centers[i].real, centers[i].imag)
            
            centers[-i] = centers[i] + c[i] * (cos(2*pi*i*t) + 1j * sin(2*pi*i*t))
            tmp = convert(centers[-i].real, centers[-i].imag, abs(c[-i]))
            canvas_fourier.coords(circles[-i], tmp[0], tmp[1], tmp[2], tmp[3])
            canvas_fourier.coords(arrows[-i], centers[i].real, centers[i].imag, centers[-i].real, centers[-i].imag)
        
        position = centers[-N] + c[-N] * (cos(2*pi*(-N)*t) + 1j * sin(2*pi*(-N)*t))
        canvas_fourier.coords(arrows[N+1], centers[-N].real, centers[-N].imag, position.real, position.imag)
        canvas_fourier.create_oval(position.real, position.imag, position.real+1, position.imag+1, fill="blue")
        window.update()
    print("Fourier Transform Finished")

def convert(centerx, centery, radius):
    return centerx-radius, centery-radius, centerx+radius, centery+radius
    


############################## GUI functions #############################
def draw_by_list(canvas, l, color):
    color = "#%02x%02x%02x" % (color[0], color[1], color[2])
    for i in range(len(l)-1):
        canvas.create_line(l[i].x, l[i].y, l[i+1].x, l[i+1].y, fill=color, width=1)

def draw_by_cluster(canvas, cluster):
    canvas.delete("all")
    color = (0, 255, 255)
    print(len(cluster))
    for l in cluster:
        print(len(l))
        color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        draw_by_list(canvas, l, color)

def load():
    global src, img, imgtk
    window.filename =  filedialog.askopenfilename(initialdir = "./", title = "Select file")

    src = cv2.imread(window.filename)
    src = cv2.resize(src, (img_width,  img_height))

    # transform opencv(BGR) to tkinter(RGB)
    img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)

    # transform numpy array to img
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    label.configure(image=imgtk)
    label.image = imgtk


############################## load img ###############################
img_width, img_height = 400, 400

src = cv2.imread("./img/lion.jpg")
img_width, img_height = 400, 400
src = cv2.resize(src, (img_width,  img_height))

# transform opencv(BGR) to tkinter(RGB)
img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)

# transform numpy array to img
img = Image.fromarray(img)
imgtk = ImageTk.PhotoImage(image=img)

label = Label(window, image=imgtk)
label.place(x=800, y=0)
label.pack


############################# Draw Line ################################

pastx, pasty = 0, 0
startbool = False

def drawing(event):
    global pastx, pasty, startbool
    if startbool:
        canvas_outline.create_line(pastx, pasty, event.x, event.y)
    pastx, pasty = event.x, event.y
    connectList.append(Point(event.x,event.y))
    startbool = True


############################## Clearing ################################

def clear():
    global startbool, connectList
    canvas_outline.delete('all')
    connectList = []
    startbool = False


################################ GUI ###################################
canvas_fourier = Canvas(window, width=img_width, height=img_height, bg="white", bd=2)
canvas_fourier.place(x=0, y=0)

canvas_outline = Canvas(window, width=img_width, height=img_height, bg="white", bd=2)
canvas_outline.place(x=400, y=0)
canvas_outline.bind("<B1-Motion>", drawing)

button_outline = Button(window, text="outline detection", command=outline_action)
button_outline.place(x=1200,y=0, width=200, height=75)

button_fourier = Button(window, text="fourier transform", command=fourier_action)
button_fourier.place(x=1200,y=75, width=200, height=75)

button_clear = Button(window, text="Clear Line", command=clear)
button_clear.place(x=1200,y=150, width=200, height=75)

button_load = Button(window, text="load img", command=load)
button_load.place(x=1200, y=225, width=200, height=75)

slider_N = Scale(window, from_=0, to=200, orient=HORIZONTAL, sliderlength=15, length=150)
slider_N.place(x=1225,y=300)
slider_N.set(10)

slider_M = Scale(window, from_=0, to=1500, orient=HORIZONTAL, sliderlength=15, length=150)
slider_M.place(x=1225,y=350)
slider_M.set(300)

window.mainloop()