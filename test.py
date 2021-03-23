from tkinter import * 
from tkinter import filedialog

root = Tk() 
root.filename = filedialog.askopenfilename(initialdir = "C:/User",title = "choose your file",filetypes = (("jpeg files","*.jpg"),("all files","*.*"))) 
print (root.filename)