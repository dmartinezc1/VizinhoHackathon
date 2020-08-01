# Modulos necesarios
from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
import manejoUsuarios as ussu
import MenuOpciones as mop


class ActividadesSeleccionadas():
    
    def __init__(self, master, lista):
        
        self.master = master
        self.lista = lista
        self.master.title("Preselección de actividades")
        
        self.listaImgs=[]
        self.listaScrolls=[]

        self.img = ImageTk.PhotoImage(Image.open("VIZINHO.png"))
        self.panel = Label(self.master, image=self.img)
        self.panel.pack(side="top", fill="both", expand="no")
                
        Label(self.master, text="De 1 a 10, cuéntanos qué tan \ninteresado estás en estas \nactividades.",font =('Bahnschrift SemiBold SemiConden', 14), padx=5, pady=5).pack()


        self.my_canvas = Canvas(self.master)
        self.my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(self.master, orient=VERTICAL, command=self.my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        self.my_canvas.config(yscrollcommand=my_scrollbar.set)
        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.config(scrollregion=self.my_canvas.bbox('all')))
        secondframe = Frame(self.my_canvas)
        for i in range(len(lista)):
            Label(secondframe, text=lista[i],font =('Bahnschrift SemiBold SemiConden', 14), padx=5, pady=5).pack()
            self.listaScrolls.append(Scale(secondframe, from_=0, to=10, orient=HORIZONTAL, length=200, showvalue=1))
            self.listaScrolls[i].pack(padx = 90)
        self.my_canvas.create_window((0, 0),window=secondframe, anchor='nw')
        self.confirmarbttn = Button(secondframe, text='Confirmar', command=self.Siguiente)
        self.confirmarbttn.pack(padx=5, pady=5)
        

    def Siguiente(self):
        
        listaAux=[]
        for elemento in self.listaScrolls:
            listaAux.append(elemento.get())
        
        print(listaAux)
        
        listaUtil = mop.darNecesario()
        
        usuario = listaUtil[0]
        contra = listaUtil[1]
        
        dicRecuperado =  ussu.registrarCalifActiv({}, usuario, contra)
        
        nombres = list()
        
        for i in dicRecuperado:
            if dicRecuperado[i] is None:
                nombres.append(i)
        
        i = 0      
        
        print(len(nombres), nombres)
        while i < len(listaAux):
            
            palabra = nombres[i]
            dicRecuperado[palabra] = listaAux[i]
            
            i += 1
        
        print(dicRecuperado)
        
        ussu.registrarCalifActiv(dicRecuperado, usuario, contra)
        
        self.master.destroy()
        

        
  