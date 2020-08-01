from tkinter import *
from tkinter import messagebox
import re
from PIL import ImageTk, Image
import os
import manejoUsuarios as ussu
import MenuOpciones as principal


def strongPassword(contra):
    if len (contra)>=8:
        if (bool(re.match('((?=.*\d)(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,30})',contra))==True):
            return True
        elif (bool(re.match('((\d*)([a-z]*)([A-Z]*)([!@#$%^&*]*).{8,30})',contra))==True):
            return False
        
        
def ingresarAlSistema(nombre,ape,mail,contra):   
    
    ussu.agregarUsuario(mail, nombre, ape, contra)
    root.destroy()
    principal.acceder(mail, contra)
    
    


def continuar():
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(regex, correo.get()):
        messagebox.showwarning('Correo inválido', 'El correo no es válido')
        return()
    elif contrasenha.get() != confcn.get():
        messagebox.showwarning('Contraseña inválida', 'Las contraseñas no coinciden.')
        return ()
    elif not strongPassword(contrasenha.get()):
        messagebox.showwarning('Contraseña inválida', 'La contraseña no es segura. Debe contener al menos 8 caracteres, una minúscula, una mayúscula y un caracter especial')
    else:
        nom= nombre.get()
        ape = l_name.get()
        mail=correo.get()
        contra=contrasenha.get()
        
        ingresarAlSistema(nom,ape,mail,contra)
        

def registrar():
    global correo
    global contrasenha
    global confcn
    global nombre
    global l_name
    global root
    root = Tk()
    # Ventana de registro
    root.title('Vizinho')
    root.configure(bg='white')

    # Frame para registarse
    cuadro = Frame(root)
    cuadro.pack()
    
    img = ImageTk.PhotoImage(Image.open("VIZINHO.png"))
    panel = Label(root, image = img)
    panel.pack(side = "top", expand = "no")
    
    
    
    cuadro = LabelFrame(root, text= 'Creación de Perfil', padx=5, pady=5,background='white')
    cuadro.pack(padx=5, pady=5)

    
    #Cuados de entrada
    nombre = Entry(cuadro, width=15)
    nombre.grid(row=0, column=1, padx=20, pady=(10, 0))
    l_name = Entry(cuadro, width=15)
    l_name.grid(row=1, column=1, padx=20)
    correo = Entry(cuadro, width=15)
    correo.grid(row=2, column=1, padx=20)
    contrasenha = Entry(cuadro, width=15, show='*')
    contrasenha.grid(row=3, column=1, padx=20)
    confcn = Entry(cuadro, width=15, show='*')
    confcn.grid(row=4, column=1, padx=20)

    #Cuadros de texto
    f_name_label = Label(cuadro, text='Nombre:',background='white')
    f_name_label.grid(row=0, column=0)
    l_name_label = Label(cuadro, text='Apellido:',background='white')
    l_name_label.grid(row=1, column=0)
    correo_label = Label(cuadro, text='Correo:',background='white')
    correo_label.grid(row=2, column=0)
    contrasenha_label = Label(cuadro, text='Contraseña: ',background='white')
    contrasenha_label.grid(row=3, column=0)
    confcon_label = Label(cuadro, text='Confirmar contraseña:',background='white')
    confcon_label.grid(row=4, column=0, padx=5)

    #Boton de confirmacion
    confirmarbttn = Button(root, text='Confirmar ', width=30, command=continuar)
    confirmarbttn.pack(padx=10, pady=10 )

    root.mainloop()
