import cv2
from tkinter import *
from PIL import Image
from PIL import ImageTk

window = Tk()
window.title("image fourier transformation")
window.geometry("600x400+100+100")
window.resizable(True, True)

# canvas = Canvas(root, width=400, height=400, bg="black", bd=2)
# canvas.pack()

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


src = cv2.imread("piano.jpg")
src = cv2.resize(src, (400, 400))

# transform opencv(BGR) to tkinter(RGB)
img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)

# transform numpy array to img
img = Image.fromarray(img)
imgtk = ImageTk.PhotoImage(image=img)

label = Label(window, image=imgtk)
label.pack(side="left")


# GUI
button = Button(window, text="outline detection", command=convert_to_tkimage)
button.pack(side="right", expand=True, fill='both')

window.mainloop()
