from tkinter import *
import vregistar as regis
from PIL import ImageTk, Image
import os
from tkinter.ttk import *
import tkinter.font as font
import VTest as hacerTest
import vResultados as res
import VerResultados as verResu
import manejoUsuarios as ussu
import Optimizador as opti
import posTest as tesp

#Opciones que debe tener el menú
#Hacer quiz
#Cambiar respestas
#Mostrar respuestas
#Cerrar sesión
#Explorar categorías

listaDatos = list()


def limpiarUser(usuario):
    
    respuesta=""
    
    for i in range (len(usuario)):
        if usuario[i]=="@":
            return respuesta
        else:
            respuesta= respuesta + usuario[i]
            
    return usuario
        

def doTest():
    segunda = Toplevel()
    hacerTest.PrimeraVentan(segunda)

    
def respuestasTest():
    
    usuario = listaDatos[0]
    contra = listaDatos[1]
    
    listaResuestas = ussu.recuperarRespuestas(usuario, contra)
    tiempoLibre = ussu.recuperarTiempoLibre(usuario, contra)
    
    numText = re.findall('[0-9]+', listaResuestas)
    recuperada = list()
            
    for cadaUno in numText:
        recuperada.append(int(cadaUno))
        
    listaCaliche = ussu.recuperarCalifActiv(usuario, contra)
    print(listaCaliche, type(listaCaliche))
    
    fuentesSele, activSele, cateSele = opti.hacerOptimizacion(recuperada, int(tiempoLibre), listaCaliche)
    
    listaFormatoQueNoTieneLink = tesp.respuestasFormatoCorrecto(fuentesSele)
    print(listaFormatoQueNoTieneLink)
    tesp.actualizarNumAccesos(fuentesSele)
    ussu.registrarActividades(fuentesSele, usuario, contra)
    
    raiz2 = Toplevel()
    laListaQueDaBob = listaFormatoQueNoTieneLink
    verResu.VentanaConResultados(raiz2,laListaQueDaBob)

    
def explorar():
    
    raiz3 = Toplevel()
    laListaQueDaBob= tesp.ultimaConsulta()
    verResu.VentanaConResultados(raiz3,laListaQueDaBob)

def cerrarSesion():
    root.destroy()
    

def acceder(usuario, contra): 
    
    listaDatos.append(usuario)
    listaDatos.append(contra)

    global root
    
    root = Tk()
    root.title('Vizinho')
    root.configure(bg='white')
    
    img = ImageTk.PhotoImage(Image.open("VIZINHO.png"))
    panel = Label(root, image = img)
    panel.pack()
    
    Label(root, text = 'Bienvenido de nuevo, \n' + limpiarUser(usuario)+'!', font =('Bahnschrift SemiBold SemiConden', 14),background="white").pack() 

    photo = ImageTk.PhotoImage(Image.open("hacerTest.png"))

    hacerTestBtn=Button(root, text = 'Hacer Test', image = photo, compound = LEFT, command=doTest,width=12)
    hacerTestBtn.pack()   

    
    photo3 = ImageTk.PhotoImage(Image.open("mostrarResultados.png"))

    mostrarResultadosBtn=Button(root, text = 'Mostrar\nResultados', image = photo3, compound = LEFT,command=respuestasTest,width=12)
    mostrarResultadosBtn.pack()
    
    photo4 = ImageTk.PhotoImage(Image.open("explorar.png"))

    explorarBtn=Button(root, text = 'Explorar\nCategorías', image = photo4, compound = LEFT,command=explorar,width=12)
    explorarBtn.pack()

    photo5 = ImageTk.PhotoImage(Image.open("cerrar.png"))

    cerrarBtn=Button(root, text = 'Cerrar\nSesión', image = photo5, compound = LEFT,command=cerrarSesion,width=12)
    cerrarBtn.pack()
        
    root.mainloop()
    
def darNecesario():
    return listaDatos