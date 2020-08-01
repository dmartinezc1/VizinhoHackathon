import cryptography, base64, hashlib, os, sqlite3
from cryptography.fernet import Fernet

conex=sqlite3.connect("Usuarios.sqlite")
cur=conex.cursor()

#################################################################################Crear tabla de Usuarios

cur.executescript('''
                  CREATE TABLE IF NOT EXISTS Usuarios(
                      idUsuario INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                      correoUsuario TEXT UNIQUE,
                      nombreUsuario TEXT,
                      apellidoUsuario TEXT,
                      hashContrasena TEXT,
                      parteKeyAlea TEXT,
                      respuestasUsuario TEXT,
                      ultimasFuentes TEXT,
                      calificacionActividades TEXT,
                      tiempoLibre INTEGER
                      );
                  ''')

################################################################################# Agrega usuario
## Parametros ->(correo,nombre,apellido,contrasena)

def agregarUsuario(correo, nombre, apellido, contrasena):

    hash=hashlib.new("sha224",(correo+contrasena).encode())
    contrasenaHash=hash.hexdigest()

    cur.execute('''
    INSERT OR IGNORE INTO Usuarios(correoUsuario,nombreUsuario,apellidoUsuario,
    hashContrasena) VALUES (?,?,?,?)''',(correo,nombre,apellido,contrasenaHash)
                )

    conex.commit()

################################################################################# Recupera usuario
## Parametros ->(correo,contrasena)
## Retorna-> tupla(nombre, apellido) || Mensaje de error si no existe

def recuperarUsuario(correo, contrasena):

    hash=hashlib.new("sha224",(correo+contrasena).encode())
    contrasenaHash=hash.hexdigest()

    cur.execute('''SELECT nombreUsuario,apellidoUsuario,respuestasUsuario FROM Usuarios
    WHERE correoUsuario = ? AND hashContrasena = ?''',(correo,contrasenaHash))
    respuesta = cur.fetchone()

    if respuesta is None:
        return False

    return respuesta

################################################################################# Registra las respuestas dadas por el usuario

def registrarRespuestas(respuestas, correo, contrasena):

    cur.execute('''SELECT idUsuario FROM Usuarios
                WHERE correoUsuario = ? ''',(correo,))

    idUsuarioRecuperado=cur.fetchone()[0]

    partekeyUsuario=str(idUsuarioRecuperado)+correo+contrasena
    partekey=os.urandom(32-len(partekeyUsuario.encode()))

    cur.execute('''
                UPDATE Usuarios SET parteKeyAlea=? WHERE idUsuario=?''',(partekey, idUsuarioRecuperado)
                )

    conex.commit()

    key=base64.urlsafe_b64encode(partekey+partekeyUsuario.encode("utf-8"))
    f=Fernet(key)
    token=f.encrypt(str(respuestas).encode())

    cur.execute('''
                UPDATE Usuarios SET respuestasUsuario=? WHERE idUsuario=?''',(token, idUsuarioRecuperado)
                )

    conex.commit()

################################################################################# Registrar las actividades que le salieron al usuario

def registrarActividades(actividades, correo, contrasena):

    hash=hashlib.new("sha224",(correo+contrasena).encode()).hexdigest()

    cur.execute('''
                UPDATE Usuarios SET ultimasFuentes=? WHERE correoUsuario=? AND hashContrasena=?'''
                ,(str(actividades), correo,hash))

    conex.commit()

################################################################################# Recuperar las respuestas a las preguntas de ususario

def recuperarRespuestas(correo,contrasena):

    cur.execute('''SELECT idUsuario, parteKeyAlea, respuestasUsuario FROM Usuarios
                WHERE correoUsuario = ? ''',(correo,))

    fetch=cur.fetchone()

    idUsuarioRecuperado=fetch[0]
    partekey=fetch[1]
    respuestasEncriptadas=fetch[2]

    parteUser=str(idUsuarioRecuperado)+correo+contrasena
    key=base64.urlsafe_b64encode(partekey+parteUser.encode("utf-8"))
    f=Fernet(key)

    return f.decrypt(respuestasEncriptadas).decode()

################################################################################# Registrar las calificaciones de las actividades
    
def registrarCalifActiv(listaActividades, correo, contrasena):
    
    hash=hashlib.new("sha224",(correo+contrasena).encode()).hexdigest()
    
    cur.execute('''SELECT calificacionActividades FROM Usuarios
                WHERE correoUsuario = ? AND hashContrasena = ?'''
                ,(correo,hash))
    
    calif = cur.fetchone()

    if calif is not None:
        
        if calif[0] is None:
            
            cur.execute('''UPDATE Usuarios SET calificacionActividades = ? 
                        WHERE correoUsuario = ? AND hashContrasena = ?''',
                        (str(listaActividades), correo, hash))
        
            conex.commit()
            
            return listaActividades
            
        else:
           
            dicRecur = eval(calif[0]) 
           
            for palabra in listaActividades:
                dicRecur[palabra] = listaActividades.get(palabra, None)
            
            cur.execute('''UPDATE Usuarios SET calificacionActividades = ? 
                        WHERE correoUsuario = ? AND hashContrasena = ?''',
                        (str(dicRecur), correo, hash))
        
            conex.commit()
            
            return dicRecur
                      
################################################################################ Vamos a guardar el tiempo libre del ususario

def guardarTiempoLibre (tiempo, correo, contrasena):
    
    hash=hashlib.new("sha224",(correo+contrasena).encode()).hexdigest()

    cur.execute('''UPDATE Usuarios SET tiempoLibre = ? 
                WHERE correoUsuario = ? AND hashContrasena = ?''',
                (tiempo, correo, hash))
        
    conex.commit()               

    
################################################################################ Recuperar el tiempo libre

def recuperarTiempoLibre(correo, contrasena):
    
    hash=hashlib.new("sha224",(correo+contrasena).encode()).hexdigest()
    
    cur.execute(''' SELECT tiempoLibre FROM Usuarios WHERE
                correoUsuario = ? AND hashContrasena = ?''',
                (correo, hash))
    
    tiempito = cur.fetchone()[0]
    
    return tiempito
    
    
################################################################################ Recuperar la lista de actividades

def recuperarCalifActiv (correo, contrasena):
    
    hash=hashlib.new("sha224",(correo+contrasena).encode()).hexdigest()
    
    cur.execute(''' SELECT calificacionActividades FROM Usuarios WHERE
                correoUsuario = ? AND hashContrasena = ?''',
                (correo, hash))
    
    tiempito = cur.fetchone()
    dicRecur = eval(tiempito[0]) 
    
    return dicRecur


