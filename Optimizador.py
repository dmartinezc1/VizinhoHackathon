### Recuperar información para correr el modelo de optimización.

import Procesamiento as pr

### Definir el modelo de optimización

import gurobipy as gp
from gurobipy import GRB

#############################
### Resolución del modelo ###
#############################

def hacerOptimizacion(listaFinal, tiempolibre, act):
    
    print(type(listaFinal), type(tiempolibre))
    
    numcat, cati = pr.categoriasValidas(listaFinal)
    numact, activ = pr.actividadesValidas(listaFinal)
    activ = act
    fuv = pr.fuentesValidas(listaFinal)
    cateActi = pr.subConjCategorias(cati, listaFinal)
    actiFu = pr.subConjActividades(activ, listaFinal)

    #######################################################  Modelo

    modelo = gp.Model("Mejores actividades para ti.")

    ####################################################### Declarar Variables

    # Creamos las variables de decisión de Categoria.
    categoriasElegidas = {}

    for c in cati:
        categoriasElegidas[c] = modelo.addVar(vtype=GRB.BINARY, name = c)
        
    # Creamos las variables de decisión de Actividad.
    actividadesElegidas = {}

    for a in activ:
        actividadesElegidas[a] = modelo.addVar(vtype=GRB.BINARY, name = a)

    # Creamos las variables de decisión de Fuente.
    fuentesElegidas = {}

    for f in fuv:
        fuentesElegidas[f] = modelo.addVar(vtype=GRB.BINARY, name = f)

    ####################################################### Restricciones

    ### El usuario escoge categorias válidas.
    modelo.addConstr( sum(categoriasElegidas[c] for c in cati) >= numcat)

    ### El usuario escoge actividades válidas.
    modelo.addConstr( sum(actividadesElegidas[a] for a in activ) <= numact)

    ### Las fuentes escogidas no deben sobrepasar el tiempo libre.
    for f in fuv:
        modelo.addConstr( fuentesElegidas[f] * fuv[f] <= tiempolibre)

    ### Se selecciona mínimo una acticidad de cada categoría elegida.
    for c in cati:
        modelo.addConstr( sum( actividadesElegidas[a] for a in cateActi[c]) >= 1 * categoriasElegidas[c])

    ### Se selecciona mínimo una fuente de cada actividad elegida.
    for a in activ:
        modelo.addConstr( sum( fuentesElegidas[f] for f in actiFu[a]) >= 1 * actividadesElegidas[a])


    ####################################################### Función Objetivo

    Fo = 0

    print(activ)
    for a in activ:
        Fo += actividadesElegidas[a] * activ[a]
    

    modelo.setObjective(Fo, GRB.MAXIMIZE)

    ####################################################### Correr el modelo.

    modelo.optimize()

    ####################################################### Imprimir la información.

    ### Fuente selecionadas
    fuentesSele = list()
    activSele = list()
    cateSele = list()

    ### Si encontro solución.
    if modelo.status == GRB.OPTIMAL:

        ### Función Objetivo
        print('Función Objetivo:', modelo.objVal)
        print('-------------------------------------')


        ### Variables de Categoria
        print('Las categorias elegidas fueron:')
        envioFCResultados = modelo.getAttr('x', categoriasElegidas)

        for c in cati:
            if categoriasElegidas[c].x > 0:
                cateSele.append(c)
                print('\t', c)
        print('-------------------------------------')

        ### Variables de Actividad
        print('Las actividad elegidas fueron:')
        envioFCResultados = modelo.getAttr('x', actividadesElegidas)

        for a in activ:
            if actividadesElegidas[a].x > 0:
                activSele.append(a)
                print('\t', a)
        print('-------------------------------------')

        ### Variables de Fuente
        print('Las fuentes elegidas fueron:')
        envioFCResultados = modelo.getAttr('x', fuentesElegidas)

        for f in fuv:
            if fuentesElegidas[f].x > 0:
                fuentesSele.append(f)
                print('\t', f)
        print('-------------------------------------')

    ### Si se petaqueo
    else:
        print('Ay no buu :(')

    ### Devolvemos las fuentes
    return fuentesSele, activSele, cateSele


