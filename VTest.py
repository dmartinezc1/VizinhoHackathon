# Modulos necesarios
from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
import vResultados as res
import Procesamiento as pro
import manejoUsuarios as ussu
import MenuOpciones as mop

# Prguntas
preguntas = [
    '1. No me siento bien conmigo mismo y tengo una mala autoestima. ',
    '2. Me cuesta manejar mis emociones en momentos difíciles.',
    '3. Me cuesta mucho relajarme, me encuentro en una situación de tensión y me sobresalto con facilidad.', 
    '4. El transporte público (trenes, autobuses) me generan mucho miedo y ansiedad.',
    '5. Me cuesta mucho dormirme y me suelo despertar cansado/a.',
    '6. No me gusta relacionarme con los demás y no tengo una vida social activa.', 
    '7. He perdido el interés por las cosas.', 
    '8. He perdido peso porque no tengo apetito.', 
    '9. Cuando alguien me ofende o me siento atacado/a, mi respuesta suele ser desproporcionada.', 
    '10. Las multitudes me generan miedo o necesidad de escapar.'
    ]

lista = [0,0,0,0,0,0,0,0,0,0]
listaFinal = list()
tiempo = None

class PrimeraVentan():
    
    def __init__(self, master, contestado=lista, tiempolib=0):
        
        self.master = master
        self.master.title('Vizinho ')
        self.secondary_win = None
        self.contestado = contestado
        self.tiempolib = tiempolib
        self.respuesta = []

        # Imagen
        self.img = ImageTk.PhotoImage(Image.open("VIZINHO.png"))
        self.panel = Label(self.master, image = self.img)
        self.panel.pack(side = "top", fill = "both", expand = "no")

        # Frame
        self.cuadro = LabelFrame(self.master, text='Acerca de ti')
        self.cuadro.pack(padx=5, pady=5)

        # Label con informacion
        self.texto = Label(self.cuadro, text='Contesta las siguientes preguntas siendo 0 si \nno te identificas y 10 si concuerda contigo.', width=50)
        self.texto.pack(pady=10)

        # Tiempo libre
        self.pregTiempo = Label(self.cuadro, text='Minutos libres que tengo en un día: ')
        self.pregTiempo.pack()

        self.tiempos = [
            '30',
            '45',
            '60',
            '75',
            '90',
            '105',
            '120'
        ]

        self.listaTiempo = ttk.Combobox(self.cuadro, height=6, values=self.tiempos)
        self.listaTiempo.pack()

        # Agrega las peguntas y Sliders
        for i in range(0, 5):
            Label(self.cuadro, text=preguntas[i], padx=5, pady=5).pack()
            self.respuesta.append(Scale(self.cuadro, from_=0, to=10, orient=HORIZONTAL, length=200, showvalue=1))
            self.respuesta[i].set(self.contestado[i])
            self.respuesta[i].pack()

        # Boton para siguiente
        self.siguientebttn = Button(self.master, text='Siguiente', command=self.Siguiente)
        self.siguientebttn.pack(padx=5, pady=5)



    def Siguiente(self):
        
        tiempo = self.listaTiempo.get()
        print(tiempo)
        
        ## Recuperar correo y contra y subirle sus respuetas
        listaUtil = mop.darNecesario()
        
        usuario = listaUtil[0]
        contra = listaUtil[1]
        
        ### VAMOS PIBE
        
        ussu.guardarTiempoLibre(tiempo, usuario, contra)
        
        if not self.secondary_win:
            
            self.master.withdraw()

            self.secondary_win = Toplevel()
            self.secondary_win.title('Vizinho')
            panel = Label(self.secondary_win, image=self.img)
            panel.pack(side="top", fill="both", expand="no")
            # Frame
            cuadro = LabelFrame(self.secondary_win, text='Acerca de ti')
            cuadro.pack(padx=5, pady=5)

            # Label con informacion
            texto = Label(cuadro,
                          text='Contesta las siguientes preguntas siendo 0 si \nno te identificas y 10 si concuerda contigo.',
                          width=50)
            texto.pack(pady=10)
            for i in range(5, 10):
                Label(cuadro, text=preguntas[i], padx=5, pady=5).pack()
                self.respuesta.append(Scale(cuadro, from_=0, to=10, orient=HORIZONTAL, length=200, showvalue=1))
                self.respuesta[i].set(self.contestado[i])
                self.respuesta[i].pack()

            cuadrito = Frame(self.secondary_win)
            cuadrito.pack()
            antbttn = Button(cuadrito, text='Anterior', command=self.Backward)
            antbttn.grid(column=0, row=0, padx=5, pady=5)
            terminarbtn = Button(cuadrito, text='Terminar', command=self.Terminar)
            terminarbtn.grid(column=1, row=0, padx=5, pady=5)

        else:
            self.secondary_win.deiconify()
            self.master.withdraw()

    def Backward(self):
        self.secondary_win.withdraw()
        self.master.deiconify()

    def Terminar(self):
        
        nuevalista = list()
        listaFinal = None
        listaFinal = nuevalista
        
        for i in self.respuesta:
                listaFinal.append(int(i.get()))
        
        print(listaFinal)
        
        
        ## Recuperar correo y contra y subirle sus respuetas
        listaUtil = mop.darNecesario()
        
        usuario = listaUtil[0]
        contra = listaUtil[1]
        
        ussu.registrarRespuestas(listaFinal, usuario, contra)
        
        
        ## Filtrar la base de datos y recuperar las actividades
        num, acti = pro.actividadesValidas(listaFinal)
        
        ## Escribir el diccionario con base al usuario
        dicUno = ussu.registrarCalifActiv(acti, usuario, contra)
        
        listaCalif = list()
        
        for i in dicUno:
            if dicUno[i] is None:
                listaCalif.append(i)
        
        self.secondary_win.destroy()
        abrir = Toplevel()
        
        res.ActividadesSeleccionadas(abrir, listaCalif)
        