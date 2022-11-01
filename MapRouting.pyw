from cgitb import text
from ctypes.wintypes import SIZE
from pickle import READONLY_BUFFER
from re import T, X
from tkinter import Tk, Label, Button, Entry
from tkinter import font
from tkinter.font import Font
from turtle import bgcolor, color, width
from typing import Text
import tkinter.font as tkFont
from colorama import Style
from pyparsing import col
import openstreetmap
from tkhtmlview import *


# def suma():
#     n1=txt.get()
#     n2=txt.get()

#     r=float(n1) + float(n2)
#     txt3.insert(0,r)

Ventana = Tk()
Ventana.title("MapRouting")
Ventana.geometry("800x600")
Ventana.config(bg="#1e1e1e")


# html_label = HTMLLabel(Ventana, html='<h1 style="color: #1e1e1e; text-align: center"> Map routing </H1><p></li><li>A mi hay que mamarmelo</li></ul>')
# html_label.pack(fill="both", expand=True)

# label1=Label(Ventana, foreground="red")
# label1.place(relx=0, rely=0.50,relwidth=1,relheight=0.1)


txt1 = Entry(Ventana, font=("Arial",24))
txt1.pack()
txt2 = Entry(Ventana, font=("Arial",24))
txt2.place(relx=0.01, rely=1,relwidth=0.5,relheight=0.1)
txt2.pack()


def ejecutar():
    try:
        openstreetmap.main(int(txt1.get()),int(txt2.get()))
        link = HTMLLabel(Ventana, html='<div style="text-align: center;"><a href="mapa.html" style="color: dodgerblue; text-align: left; width: 50px; height: 20px;">Abrir en el mapa</a></div>')
        link.config(width="20", height="2", background="#1e1e1e", foreground="white")
        link.pack()
    except Exception as e:
        print(e)
        popupmsg("Solo se puede buscar una ruta a la vez")

def popupmsg(msg):
    popup = Tk()
    popup.wm_title("!")
    label = Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

btn = Button(text="Ejecutar", command= ejecutar,font=("verdana",14), width=50, height=1)
btn.pack()



# openstreetmap.main(10,30)
Ventana.mainloop();