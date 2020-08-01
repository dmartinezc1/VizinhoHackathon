from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image


class VentanaConResultados():
    
    def __init__(self, master, lista):
        self.master = master
        self.lista = lista
        self.mostrar=[]

        # Imagen
        self.img = ImageTk.PhotoImage(Image.open("VIZINHO.png"))
        self.panel = Label(self.master, image=self.img)
        self.panel.pack(side="top", fill="both", expand="no")

        # Combobox con las actividades
        for i in range(0,len(lista)):
            self.mostrar.append(lista[i][1])

        self.listaAct = ttk.Combobox(self.master, height=6, values=self.mostrar)
        self.listaAct.pack()

        # Boton de actividad
        self.botton = Button(self.master, text='Ver Actividad', command=self.MostrarActividad)
        self.botton.pack()

        self.cuadro = Frame(self.master)
        self.nombre = Label(self.cuadro, font=('Bahnschrift SemiBold SemiConden', 25), padx=5,pady=5)
        self.fuente = Label(self.cuadro, padx=5, pady=5)
        self.link = Label(self.cuadro, padx=5, pady=5)
        self.foto = Label(self.cuadro, padx=10, pady=10)
        self.nombre.pack()
        self.foto.pack()
        self.fuente.pack()
        self.link.pack()


    def MostrarActividad(self):
        
        if self.listaAct.get() != '':
            self.cuadro.pack()
            self.nombre.config(text=self.lista[self.listaAct.current()][0]+' ( '+self.listaAct.get()+')')
            self.imagen = Image.open(str(self.listaAct.get())+'.png')
            self.imagen = self.imagen.resize((100, 50), Image.ANTIALIAS)
            self.imagen = ImageTk.PhotoImage(self.imagen)
            self.foto.config(image=self.imagen)
            self.fuente.config(text='Fuente: '+str(self.lista[self.listaAct.current()][2]))
            self.link(str(self.lista[self.listaAct.current()][2]))



