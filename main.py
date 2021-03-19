import cv2
from tkinter import *
from PIL import Image
from PIL import ImageTk

from img_to_function import *

############################ tkinter window ############################
window = Tk()
window.title("image fourier transformation")
window.geometry("1000x400+100+100")
window.resizable(False, False)

############################### functions ##############################
def convert_to_tkimage():
    global src
    
    # color img -> gray sclae -> outline
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    outline = cv2.Canny(gray, 100, 255)
    # cv2.imshow("canny", outline)

    img = Image.fromarray(outline)
    imgtk = ImageTk.PhotoImage(image=img)

    label.config(image=imgtk)
    label.image = imgtk


############################## load img ###############################
src = cv2.imread("./img/lion.jpg")
src = cv2.resize(src, (400, 400))

# transform opencv(BGR) to tkinter(RGB)
img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)

# transform numpy array to img
img = Image.fromarray(img)
imgtk = ImageTk.PhotoImage(image=img)


################################ GUI ###################################
canvas = Canvas(window, width=400, height=400, bg="white", bd=2)
canvas.place(x=0, y=0)

l = [Point(10,10), Point(100,50), Point(40,100), Point(80,90)]
draw_by_list(canvas, l)

label = Label(window, image=imgtk)
label.place(x=400, y=0)
label.pack

button = Button(window, text="outline detection", command=convert_to_tkimage)
button.place(x=800,y=0, width=200, height=400)
# button.pack(expand=True, fill='both')

window.mainloop()
