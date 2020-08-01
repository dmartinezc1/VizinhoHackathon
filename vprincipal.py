from tkinter import *
from tkinter import  messagebox
import vregistar as regis
from PIL import ImageTk, Image
import os
import MenuOpciones as principal
import manejoUsuarios as ussu

contador=0

def darUsuario():
    return lcorreo.get()

def darContra():
    return lcontrasenha.get()

def registrar():
    raiz.destroy()
    regis.registrar()
    print("")

def contraCorrecta(user,contra):
    print ("Revisando contraseña")
    return True

def obtenerDatos():
    user = lcorreo.get()
    contra = lcontrasenha.get()
    
    busqueda = ussu.recuperarUsuario(user, contra) 
    
    if busqueda is not False:
        busqueda = True
    
    if not busqueda:
        messagebox.showwarning('Usuario Inexistente o contraseña incorrecta.', 'Por favor inténtelo nuevamente, no hemos encontrado este usuario')
    else:
        raiz.destroy()
        principal.acceder(user, contra)

    
def mostrar():

    global raiz
    global lcorreo
    global lcontrasenha
    
    # Ventana principal
    raiz = Tk()
    raiz.title('Vizinho')
    raiz.configure(bg='white')

    img = ImageTk.PhotoImage(Image.open("VIZINHO.png"))
    panel = Label(raiz, image = img)
    panel.pack(side = "top", fill = "both", expand = "no")
    
    # Cuadros de texto y entradas
    cuadro = LabelFrame(raiz, text= 'Bienvenido', padx=5, pady=5,background='white')
    cuadro.pack(padx=5, pady=5)
    
    correo = Label(cuadro, text='Correo electrónico: ', padx=5, pady=5, background='white')
    correo.grid(row=0, column=0)    
    
    lcorreo = Entry(cuadro)
    lcorreo.grid(row=0, column=1, padx=5, pady=5)
    
    contrasenha = Label(cuadro, text='Contraseña: ', padx=5, pady=5,background='white')
    contrasenha.grid(row=1, column=0)
    
    lcontrasenha = Entry(cuadro, show='*')
    lcontrasenha.grid(row=1, column=1, padx=5, pady=5)
    
    entrar = Button(cuadro, text='Iniciar Sesión', command=obtenerDatos)
    entrar.grid(row=2, column=0, padx=5, pady=5)
    
    registrarBtn = Button(cuadro, text='Registrarse ', command=registrar)
    registrarBtn.grid(row=2, column=1, padx=5, pady=5)
    
    raiz.mainloop()

mostrar()