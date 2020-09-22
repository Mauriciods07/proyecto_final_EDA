import tkinter as tk
from PIL import ImageTk, Image

#Variables de la ventana
HEIGHT = 600
WIDTH = 800

raiz = tk.Tk()
raiz.title("Paráfrasis baja")
#Crear la ventana
canvas = tk.Canvas(raiz, height=HEIGHT, width=WIDTH)
canvas.pack()

#Crear un marco
frame = tk.Frame(raiz, bg='white', padx=50, pady=50)
frame.place(relx=0.05, rely=0.05, relheight=0.88, relwidth=0.9)



raiz.mainloop()