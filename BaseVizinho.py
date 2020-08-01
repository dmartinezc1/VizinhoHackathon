### Vamos a usar 'Sqlite' para la base de datos.
import sqlite3

conexion = sqlite3.connect('BaseVizinho.sqlite')
cursor = conexion.cursor()

################################################################################# VAMOS A CREAR LAS TABLAS DESDE CERO.

cursor.executescript ('''

    CREATE TABLE IF NOT EXISTS Categoria (
        id_categoria  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        Nombre_Categoria    TEXT UNIQUE
    );

    CREATE TABLE IF NOT EXISTS Actividad (

        id_actividad  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        Nombre_Actividad TEXT UNIQUE,
        Categoria_Id INTEGER,

        Pregunta_1 INTEGER,
        Pregunta_2 INTEGER,
        Pregunta_3 INTEGER,
        Pregunta_4 INTEGER,
        Pregunta_5 INTEGER,
        Pregunta_6 INTEGER,
        Pregunta_7 INTEGER,
        Pregunta_8 INTEGER,
        Pregunta_9 INTEGER,
        Pregunta_10 INTEGER

    );

    CREATE TABLE IF NOT EXISTS FuenteInfo (

        id_FuenteInfo  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        Nombre_FuenteInfo TEXT UNIQUE,
        Actividad_id  INTEGER,

        Duracion INTEGER,
        Calificacion TEXT,
        NumAccesos INTEGER,
        Link_Acceso TEXT

    );

''')

################################################################################# VAMOS A CARGAR EL ARCHIVO DE LAS CATEGORIAS

fCategoria = open('Categorias.txt')

for cate in fCategoria:
    cate = cate.strip()
    cursor.execute('''INSERT OR IGNORE INTO Categoria (Nombre_Categoria) VALUES ( ? )''', ( cate, ))

conexion.commit()

################################################################################# VAMOS A CARGAR EL ARCHIVO DE LAS ACTIVIDADES

fActividades = open('Actividades.txt')

for acti in fActividades:
    elementosActi = acti.split(',')

    cursor.execute('SELECT id_categoria FROM Categoria WHERE Nombre_Categoria = ?', (elementosActi[1].strip(), ))
    cate_id = cursor.fetchone()[0]

    if cate_id is None:
        exit

    cursor.execute('''INSERT OR IGNORE INTO Actividad (Nombre_Actividad, Categoria_Id, Pregunta_1,
                Pregunta_2, Pregunta_3, Pregunta_4, Pregunta_5, Pregunta_6, Pregunta_7, Pregunta_8, Pregunta_9, Pregunta_10)
                VALUES ( ?,?,?,?,?,?,?,?,?,?,?,? )''', (elementosActi[0].strip(), cate_id, elementosActi[2].strip(),
                elementosActi[3].strip(), elementosActi[4].strip(), elementosActi[5].strip(), elementosActi[6].strip(),
                elementosActi[7].strip(),elementosActi[8].strip(),elementosActi[9].strip(),elementosActi[10].strip(),elementosActi[11].strip() ))

conexion.commit()

################################################################################# VAMOS A CARGAR EL ARCHIVO DE LAS FUENTES DE INFORMACIÓnote

fFuentesInfo = open('FuentesInfo.txt')

for fuente in fFuentesInfo:
    elementosFuente = fuente.split(',')

    cursor.execute('SELECT id_actividad FROM Actividad WHERE Nombre_Actividad = ?', (elementosFuente[1].strip(), ))
    acti_id = cursor.fetchone()[0]

    cursor.execute('''INSERT OR IGNORE INTO FuenteInfo (Nombre_FuenteInfo, Actividad_id, Duracion, Link_Acceso, Calificacion, NumAccesos)
                        VALUES ( ?,?,?,?,Null,Null)''', (elementosFuente[0].strip(), acti_id, elementosFuente[2].strip(), elementosFuente[3].strip() ))

conexion.commit()

################################################################################# BASE DE DATOS CREADA

print(' Base de datos creada exitosamente :)')
