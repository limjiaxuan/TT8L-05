import tkinter as tk
from tkinter import *
from tkinter import messagebox


app = tk.Tk()
app.title('To-do List') 
app.geometry('1000x800')
app.config(bg='#FDEDEC')
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width/2) - (1000/2)
y = (screen_height/2) - (800/2)
app.geometry(f'+{int(x)}+{int(y)}')





app.mainloop()


   
