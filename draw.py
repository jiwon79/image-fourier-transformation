from tkinter import *

window=Tk()
window.geometry("640x400+100+100")
window.resizable(True, True)
pastx, pasty = 0, 0
startbool = False

def drawing(event):
    global pastx, pasty, startbool
    if startbool:
        canvas.create_line(pastx, pasty, event.x, event.y)
    pastx, pasty = event.x, event.y
    startbool = True

canvas = Canvas(window, width=600, height=400, bg="white", bd=2)
canvas.pack()
window.update()
canvas.bind("<B1-Motion>", drawing)
window.mainloop()