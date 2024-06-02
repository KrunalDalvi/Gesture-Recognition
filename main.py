import tkinter as tk
import os
import tkinter.font as font
from tkinter import *
from PIL import Image, ImageTk # PIL is the Python Imaging Library which provides the python interpreter with image editing capabilities. 
import subprocess

window = tk.Tk()
window.title("OS Project")
window.geometry("1280x750")

# The PhotoImage class is used to display images in labels, buttons, canvases, and text widgets, which is present in tkinter package.
# This function takes a file path as an argument and returns the image object.
# We can place the geometry manager that allows users to put the widget anywhere on the screen by providing x & y coordinates. 
bg = ImageTk.PhotoImage(file="os_project_bg.png")
label1 = Label(window, image=bg)
label1.place(x=0, y=0, relwidth=1, relheight=1)

btn_font = font.Font(size=12)

def open_brightness_control():
    subprocess.Popen(["python", "BrightnessControlHandTracking.py"])

def open_volume_control():
    subprocess.Popen(["python", "Volume_control.py"])

button1 = tk.Button(window, text="Brightness Control", height=2, width=35, bg='white', command=open_brightness_control, fg='#224362')
button1['font'] = btn_font
button1.place(x=60, y=200)

button2 = tk.Button(window, text="Volume Control", height=2, width=35, bg='white', command=open_volume_control, fg='#224362')
button2['font'] = btn_font
button2.place(x=60, y=270)

btn_font = font.Font(size=12)

button3 = tk.Button(window, text="Exit", height=2, width=35, bg='white', fg='#224362', command=window.destroy)
button3['font'] = btn_font
button3.place(x=60, y=340)

window.mainloop()
