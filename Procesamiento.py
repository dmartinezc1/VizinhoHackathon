### Vamos a usar 'Sqlite' para la base de datos.
import sqlite3

conexion = sqlite3.connect('BaseVizinho.sqlite')
cursor = conexion.cursor()

##########################################################
### Vamos a generar la consulta con base a las preguntas.#
##########################################################

lista = [1,20,3,4,5,6,7,8,9,10]

################################################################################# Recuperar categorias diferentes para restricción con base a las preguntas.
### Que categorias hay y cuantas son.

def categoriasValidas (listaResultadoPreguntas):

    numCateg = 0
    Categorias = list()

    cursor.execute('''SELECT Categoria.Nombre_Categoria FROM Actividad JOIN Categoria ON Categoria.id_categoria = Actividad.Categoria_Id
                    WHERE Pregunta_1 >= ? AND Pregunta_2 >= ? AND Pregunta_3 >= ? AND Pregunta_4 >= ? AND Pregunta_5 >= ? AND Pregunta_6 >= ?
                    AND Pregunta_7 >= ? AND Pregunta_8 >= ? AND Pregunta_9 >= ? AND Pregunta_10 >= ?''' ,
                    (listaResultadoPreguntas[0], listaResultadoPreguntas[1], listaResultadoPreguntas[2], listaResultadoPreguntas[3],
                    listaResultadoPreguntas[4], listaResultadoPreguntas[5], listaResultadoPreguntas[6], listaResultadoPreguntas[7],
                    listaResultadoPreguntas[8], listaResultadoPreguntas[9]) )

    filtrado = cursor.fetchone()

    while filtrado is not None:

        if filtrado[0] not in Categorias:
            Categorias.append(filtrado[0])
            numCateg += 1

        filtrado = cursor.fetchone()

    return (numCateg, Categorias)

################################################################################# Recuperar actividades diferentes para restricción y clasificación.
### Que actividades hay y cuantas son.
def actividadesValidas (listaResultadoPreguntas):

    numActiv = 0
    activa = dict()

    cursor.execute('''SELECT Nombre_Actividad FROM Actividad WHERE Pregunta_1 >= ? AND Pregunta_2 >= ? AND Pregunta_3 >= ? AND Pregunta_4 >= ?
                    AND Pregunta_5 >= ? AND Pregunta_6 >= ? AND Pregunta_7 >= ? AND Pregunta_8 >= ? AND Pregunta_9 >= ? AND Pregunta_10 >= ?''' ,
                    (listaResultadoPreguntas[0], listaResultadoPreguntas[1], listaResultadoPreguntas[2], listaResultadoPreguntas[3],
                    listaResultadoPreguntas[4], listaResultadoPreguntas[5], listaResultadoPreguntas[6], listaResultadoPreguntas[7],
                    listaResultadoPreguntas[8], listaResultadoPreguntas[9]))

    filtrado = cursor.fetchone()

    while filtrado is not None:

        if filtrado[0] not in activa:
            activa[filtrado[0]] = None
            numActiv += 1

        filtrado = cursor.fetchone()

    return (numActiv, activa)

################################################################################# Vamos a recuperar las fuentes con su respesctiva duración con base en las preguntas.

def fuentesValidas(listaResultadoPreguntas):

    fuentes = dict()

    cursor.execute('''SELECT FuenteInfo.Nombre_FuenteInfo, FuenteInfo.Duracion FROM Actividad JOIN FuenteInfo
                    ON FuenteInfo.Actividad_id = Actividad.id_actividad
                    WHERE Pregunta_1 >= ? AND Pregunta_2 >= ? AND Pregunta_3 >= ? AND Pregunta_4 >= ? AND Pregunta_5 >= ? AND Pregunta_6 >= ?
                    AND Pregunta_7 >= ? AND Pregunta_8 >= ? AND Pregunta_9 >= ? AND Pregunta_10 >= ?''' ,
                    (listaResultadoPreguntas[0], listaResultadoPreguntas[1], listaResultadoPreguntas[2], listaResultadoPreguntas[3],
                    listaResultadoPreguntas[4], listaResultadoPreguntas[5], listaResultadoPreguntas[6], listaResultadoPreguntas[7],
                    listaResultadoPreguntas[8], listaResultadoPreguntas[9]))

    filtrado = cursor.fetchone()

    while filtrado is not None:

        if filtrado[0] not in fuentes:
            fuentes[filtrado[0]] = filtrado[1]

        filtrado = cursor.fetchone()

    return fuentes

################################################################################# Vamos a generar los subconjuntos de las categorias (que actividades contienen).

def subConjCategorias(listaDeCategoriasValidas, listaResultadoPreguntas):

    cateActi = dict()

    for categoria in listaDeCategoriasValidas:
        cateActi[categoria] = list()

    cursor.execute('''SELECT Categoria.Nombre_Categoria, Actividad.Nombre_Actividad FROM Actividad JOIN Categoria
                    ON Categoria.id_categoria = Actividad.Categoria_Id
                    WHERE Pregunta_1 >= ? AND Pregunta_2 >= ? AND Pregunta_3 >= ? AND Pregunta_4 >= ? AND Pregunta_5 >= ? AND Pregunta_6 >= ?
                    AND Pregunta_7 >= ? AND Pregunta_8 >= ? AND Pregunta_9 >= ? AND Pregunta_10 >= ?''' ,
                    (listaResultadoPreguntas[0], listaResultadoPreguntas[1], listaResultadoPreguntas[2], listaResultadoPreguntas[3],
                    listaResultadoPreguntas[4], listaResultadoPreguntas[5], listaResultadoPreguntas[6], listaResultadoPreguntas[7],
                    listaResultadoPreguntas[8], listaResultadoPreguntas[9]))

    filtrado = cursor.fetchone()

    while filtrado is not None:

        cateActi[filtrado[0]].append(filtrado[1])
        filtrado = cursor.fetchone()

    return cateActi


################################################################################# Vamos a generar los subconjuntos de las actividades (que fuentes contienen).

def subConjActividades(listaDeActividadesValidas, listaResultadoPreguntas):

    actiFu = dict()

    for actividad in listaDeActividadesValidas:
        actiFu[actividad] = list()

    cursor.execute('''SELECT Actividad.Nombre_Actividad, FuenteInfo.Nombre_FuenteInfo FROM Actividad JOIN FuenteInfo
                    ON FuenteInfo.Actividad_id = Actividad.id_actividad
                    WHERE Pregunta_1 >= ? AND Pregunta_2 >= ? AND Pregunta_3 >= ? AND Pregunta_4 >= ? AND Pregunta_5 >= ? AND Pregunta_6 >= ?
                    AND Pregunta_7 >= ? AND Pregunta_8 >= ? AND Pregunta_9 >= ? AND Pregunta_10 >= ?''' ,
                    (listaResultadoPreguntas[0], listaResultadoPreguntas[1], listaResultadoPreguntas[2], listaResultadoPreguntas[3],
                    listaResultadoPreguntas[4], listaResultadoPreguntas[5], listaResultadoPreguntas[6], listaResultadoPreguntas[7],
                    listaResultadoPreguntas[8], listaResultadoPreguntas[9]))

    filtrado = cursor.fetchone()

    while filtrado is not None:

        actiFu[filtrado[0]].append(filtrado[1])
        filtrado = cursor.fetchone()

    return actiFu
