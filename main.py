import cv2
from tkinter import *
from PIL import Image
from PIL import ImageTk

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


def img_function(t): # 0<= t <= 1
    global connectList
    
    idx = int(t*len(connectList)-1)
    para = t*len(connectList)-idx
    return segment_function(connectList[idx], connectList[idx+1], para)


def convert_to_tkimage():
    global src
    global connectList
    
    # color img -> gray sclae -> outline
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    outline = cv2.Canny(gray, 100, 255)
    # cv2.imshow("canny", outline)

    connectList = connect_points(outline)
    draw_by_list(canvas_outline, connectList)

    print(img_function(0.3))

    img = Image.fromarray(outline)
    imgtk = ImageTk.PhotoImage(image=img)

    label.config(image=imgtk)
    label.image = imgtk


def connect_points(outline):
    # detect black point
    pointList = []
    for i in range(img_width):
        for j in range(img_height):
            if outline[i][j] == 255:
                pointList.append(Point(j, i))
    
    # connect near point
    connectList = [0]
    while len(connectList) != len(pointList):
        dis = 800
        point = pointList[connectList[-1]]
        for i in range(len(pointList)):
            if not i in connectList and dis > point.getDistance(pointList[i]):
                dis = point.getDistance(pointList[i])
                near = i
        connectList.append(near)
        
        print(len(connectList)/len(pointList))
    connectList.append(0)

    for i in range(len(connectList)):
        connectList[i] = pointList[connectList[i]]
   
    return connectList


# GUI function
l = [Point(10,10), Point(100,50), Point(40,100), Point(80,90)]
def draw_by_list(canvas, l):
    for i in range(len(l)-1):
        canvas.create_line(l[i].x, l[i].y, l[i+1].x, l[i+1].y, fill="#476042", width=1)


# bilateral filter
############################## load img ###############################
src = cv2.imread("./img/music.jpg")
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
