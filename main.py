import cv2
from tkinter import *
from PIL import Image
from PIL import ImageTk

from classes import *
from img_to_function import *

############################ tkinter window ############################
window = Tk()
window.title("image fourier transformation")
window.geometry("1000x400+100+100")
window.resizable(False, False)

############################### functions ##############################
connectList = []
def convert_to_tkimage():
    global src
    global connectList
    
    # color img -> gray sclae -> outline
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    outline = cv2.Canny(gray, 100, 255)
    # cv2.imshow("canny", outline)

    connectList = connect_points(outline)
    # print(connectList)
    draw_by_list(canvas, connectList)

    img = Image.fromarray(outline)
    imgtk = ImageTk.PhotoImage(image=img)

    label.config(image=imgtk)
    label.image = imgtk

def connect_points(outline):
    pointList = []
    for i in range(img_width):
        for j in range(img_height):
            if outline[i][j] == 255:
                pointList.append(Point(j, i))
    
    connectList = [0]
    # print(len(pointList))
    while len(connectList) != len(pointList):
        dis = 800
        point = pointList[connectList[-1]]
        for i in range(len(pointList)):
            if not i in connectList and dis > point.getDistance(pointList[i]):
                dis = point.getDistance(pointList[i])
                near = i
        connectList.append(near)
        
        per = len(connectList)/len(pointList)
        print(per)

    for i in range(len(connectList)):
        connectList[i] = pointList[connectList[i]]
    # print(connectList)
   
    return connectList

# bilateral filter
############################## load img ###############################
src = cv2.imread("./img/lion.jpg")
img_width, img_height = 200, 200
src = cv2.resize(src, (img_width,  img_height))

# transform opencv(BGR) to tkinter(RGB)
img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)

# transform numpy array to img
img = Image.fromarray(img)
imgtk = ImageTk.PhotoImage(image=img)


################################ GUI ###################################
canvas = Canvas(window, width=img_width, height=img_height, bg="white", bd=2)
canvas.place(x=0, y=0)

label = Label(window, image=imgtk)
label.place(x=400, y=0)
label.pack

button = Button(window, text="outline detection", command=convert_to_tkimage)
button.place(x=800,y=0, width=200, height=400)
# button.pack(expand=True, fill='both')

window.mainloop()
