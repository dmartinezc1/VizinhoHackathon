import sqlite3
import re

conexion1 = sqlite3.connect('BaseVizinho.sqlite')
cursor1 = conexion1.cursor()

##Se actualiza el numero de accesos de las fuentes
def actualizarNumAccesos(nombreFuentes):

    for elemento in nombreFuentes:
        
        cursor1.execute('''
            SELECT NumAccesos FROM FuenteInfo
            WHERE Nombre_FuenteInfo= ? ''', (elemento,)
            )

        var = cursor1.fetchone()

        if var is None:
            True
            
        elif var[0] is None:
            
            cursor1.execute('''
                UPDATE FuenteInfo SET NumAccesos = 1
                WHERE Nombre_FuenteInfo= ? ''', (elemento,)
                )
            
        else:
            
            cursor1.execute('''
                UPDATE FuenteInfo SET NumAccesos = ?
                WHERE Nombre_FuenteInfo= ? ''', (var[0]+1, elemento)
                )

        conexion1.commit()

##Se acutaliza la lista de calificacion de la fuente y retorna la calificacion promedio
def actualizarCalif(nombreFuente, calificacion):
    
    cursor1.execute('''
        SELECT Calificacion FROM FuenteInfo
        WHERE Nombre_FuenteInfo= ? ''', (nombreFuente,)
        )
    
    cal = cursor1.fetchone()
    
    if cal is not None:
        
        if cal[0] is not None:
            
            numText = re.findall('[0-9]+', cal[0])
            recuperada = list()
            
            for cadaUno in numText:
                recuperada.append(int(cadaUno))
                
            recuperada.append(calificacion)
            
            cursor1.execute('''
                UPDATE FuenteInfo SET Calificacion = ?
                WHERE Nombre_FuenteInfo= ? ''', (str(recuperada),nombreFuente)
                )

            conexion1.commit()
            return sum(recuperada)/len(recuperada)
        
        else:
            
            lista=list()
            lista.append(calificacion)
            
            cursor1.execute('''
                UPDATE FuenteInfo SET Calificacion = ?
                WHERE Nombre_FuenteInfo= ? ''', (str(lista),nombreFuente)
                )

            conexion1.commit()
            return calificacion
        
    else:
        True    
    
### Devolver respuestas modelo como asociación fuente actividad
def respuestasFormatoCorrecto(listaFuentes):
    
    respu = list()
    
    for cadaFuente in listaFuentes:
        
        cursor1.execute('''SELECT FuenteInfo.Nombre_FuenteInfo, Actividad.Nombre_Actividad, 
                        FuenteInfo.Link_Acceso FROM Actividad JOIN FuenteInfo ON FuenteInfo.Actividad_id 
                       = Actividad.id_actividad WHERE FuenteInfo.Nombre_FuenteInfo = ? 
                       ORDER BY FuenteInfo.Calificacion''', (cadaFuente,))
                    
        parejaFeliz = cursor1.fetchone()
        
        respu.append(parejaFeliz)
                    
    return respu
               
                    
### Ultima consulta exporatoria
    
def ultimaConsulta():
    
    cursor1.execute('''SELECT FuenteInfo.Nombre_FuenteInfo, Actividad.Nombre_Actividad, 
                        FuenteInfo.Link_Acceso FROM Actividad JOIN FuenteInfo ON FuenteInfo.Actividad_id 
                       = Actividad.id_actividad''')
                       
    todo = cursor1.fetchall()
    
    return todo
    
    
