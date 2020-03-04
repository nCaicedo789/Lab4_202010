"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
Implementación de una tabla de simbolos ordenada, mediante un arbol binario
balanceado Red-Black. 
"""



import config as cf 
from DataStructures import rbtnode as node
from ADT import list as lt


#_____________________________________________________________________________
#      API
#_____________________________________________________________________________


def newMap ( omaptype='RBT' ):
    """
    Crea una tabla de simbolos ordenada vacía.
    """
    return node.newNode (None, None, 0, node.BLACK)

    

def put (rbt, key , value, comparefunction):
    """
    Ingresa una pareja llave,valor a la tabla.  Si la llave ya existe, se reemplaza el valor.
    Es necesario proveer una función de comparación para las llaves.
    """

    if rbt['key'] == None:                                                 # Se trata de la raíz del árbol
        rbt['key'] = key
        rbt['value'] = value
        rbt['color'] = node.RED
        rbt['size'] = 1
        return rbt

    cmp = comparefunction (key, rbt['key'])

    if  (cmp < 0):                                                          # La llave a insertar es menor que la raiz
        if (rbt['left']==None):
            rbt['left'] = node.newNode (key, value, 1, node.RED)
        else:
            rbt['left'] = put(rbt['left'],  key, value, comparefunction)      
    elif (cmp > 0):                                                          # La llave a insertar es mayor que la raíz
        if (rbt['right']==None):
            rbt['right'] = node.newNode (key, value, 1, node.RED)
        else:
            rbt['right'] = put( rbt['right'], key, value, comparefunction)      
    else:                                                                    # La llave ya se encuentra en la tabla
        rbt['value'] = value

    #Se ajusta el balanceo del arbol
    
    if ( isRed(rbt['right']) and not (isRed(rbt['left']) ) ):                # El hijo derecho es rojo
        rbt = rotateLeft(rbt)
    if (isRed(rbt['left'])  and  isRed( rbt['left']['left'] )):              # Dos enlaces consecutivos izquierdos rojos
        rbt = rotateRight(rbt)
    if (isRed(rbt['left'])  and isRed(rbt['right'])):                        # Dos hijos rojos
        flipColors(rbt)
    rbt['size'] = size(rbt['left']) + size(rbt['right']) + 1

    return rbt
    



def get (rbt, key, comparefunction):
    """
    Retorna la pareja llave, valor, cuya llave sea igual a key.
    Es necesario proveer una función de comparación para las llaves.
    """
    element = None
    if ( rbt['key'] != None):
        cmp = comparefunction (key, rbt['key'] )
        if (cmp < 0):
            if (rbt['left'] != None):
                element =  get (rbt['left'], key, comparefunction)
        elif (cmp > 0):
            if (rbt['right'] != None):
                element = get (rbt['right'], key, comparefunction)
        else:
            element = rbt
    return element




def remove (map , key, comparefunction):
    """
    Elimina la pareja llave,valor, donde llave == key.
    Es necesario proveer la función de comparación entre llaves 

    No implementada en esta versión
    """
    pass



def contains (rbt, key, comparefunction):
    """
    Retorna True si la llave key se encuentra en la tabla o False en caso contrario.  
    Es necesario proveer la función de comparación entre llaves. 
    """
    if ( rbt['key'] == None):
        return False
    else:
        return (get(rbt,key,comparefunction)!= None)



def size(rbt):
    """
    Retornar el número de entradas en la tabla
    """
    if (rbt == None):
        return 0
    else:
        return rbt['size']



def isEmpty( rbt ):
    """
    Informa si la tabla  se encuentra vacia
    """
    return (rbt['key'] == None)



def keySet (rbt):
    """
    Retorna una lista con todas las llaves de la tabla 
    """
    klist = lt.newList ()
    klist = KeySetHelper (rbt, klist)

    return klist




def valueSet(rbt):
    """
    Retorna una lista con todos los valores de la tabla 
    """
    vlist = lt.newList ()
    vlist = valueSetHelper (rbt, vlist)
    return vlist



def minKey (rbt):
    """
    Retorna la menor llave de la tabla de simbolos 
    """
    if (rbt['left'] == None): 
        return rbt; 
    else:                
        return minKey(rbt['left'])




def maxKey (rbt):
    """
    Retorna la mayor llave de la tabla de simbolos 
    """
    if (rbt['right'] == None): 
        return rbt; 
    else:                
        return maxKey(rbt['right'])



def deleteMin (rbt):
    """
    Encuentra y remueve la menor  llave de la tabla de simbolos y su valor asociado

    No implementada en esta versión
    """
    pass



def deleteMax (rbt):
    """
    Encuentra y remueve la mayor llave de la tabla de simbolos y su valor asociado

    No implementada en esta versión
    """
    pass
    



def floor (rbt, key, comparefunction):
    """
    Retorna la llave mas grande en la tabla de simbolos, menor o igual a la llave key 
    """ 
    if (rbt == None):
        return None

    cmp = comparefunction (key, rbt['key'])

    if (cmp == 0): 
        return rbt
    if (cmp <  0):
        return floor (rbt['left'], key, comparefunction)
    t = floor(rbt['right'], key, comparefunction); 
    if (t != None):
        return t
    else:
        return rbt




def ceiling (rbt, key, comparefunction):
    """
    Retorna la llave mas pequeña en la tabla de simbolos, mayor o igual a la llave key 
    """ 
    pass



def select (rbt, k):
    """
    Retorna la k-esima llave mas pequeña de la tabla
    """ 
    pass



def rank (rbt, key, comparefunction):
    """
    Retorna el número de llaves en la tabla estrictamente menores que key
    """
    pass


def height (rbt):
    if (rbt == None):
        return -1
    else:
        return 1  +  max (height (rbt['left']),  height (rbt['right']))


#_____________________________________________________________________________
#       Funciones Helper
#_____________________________________________________________________________

def valueSetHelper (rbt, vlist):
    """
    Retorna una lista con las llaves del arbol. La lista se crea siguiendo un recorrido en inorden.
    """
    if (rbt == None):
        return vlist
    valueSetHelper (rbt['left'], vlist)
    lt.addLast (vlist, rbt['value'])
    valueSetHelper (rbt['right'], vlist)
    return vlist



def KeySetHelper (rbt, klist):
    """
    Retorna una lista con las llaves del arbol. La lista se crea siguiendo un recorrido en inorden.
    """
    if (rbt == None):
        return klist
    KeySetHelper (rbt['left'], klist)
    lt.addLast (klist, rbt['key'])
    KeySetHelper (rbt['right'], klist)
    return klist



def rotateLeft(rbt):
    """
    rotación izquierda para compensar dos enlaces rojos consecutivos
    """        
    x = rbt['right']
    rbt['right'] = x['left'] 
    x['left'] = rbt
    x['color'] = x['left']['color']
    x['left']['color'] = node.RED
    x['size'] = rbt['size']
    rbt['size'] = size(rbt['left']) + size(rbt['right']) + 1
    return x


def rotateRight(rbt):
    """
    Rotación a la derecha para compensar un hijo rojo a la derecha
    """
    x = rbt['left']
    rbt['left'] = x['right'] 
    x['right'] = rbt
    x['color'] = x['right']['color']
    x['right']['color'] = node.RED
    x['size'] = rbt['size']
    rbt['size'] = size(rbt['left']) + size(rbt['right']) + 1
    return x
  
        

def flipNodeColor (rbnode):
    """
    Cambi el color de un nodo
    """
    if (rbnode != None):
        if (rbnode['color'] == node.RED):
            rbnode['color'] = node.BLACK
        else:
            rbnode['color'] = node.RED



def flipColors (rbnode):
    """
    Cambia el color de un nodo y de sus dos hijos
    """
    flipNodeColor ( rbnode )
    flipNodeColor ( rbnode['left'] )
    flipNodeColor ( rbnode['right'] )
   



def isRed (rbnode):
    """
    Indica si un nodo del arbol es rojo
    """

    if (rbnode == None):
        return False
    else:
        return (rbnode['color'] == node.RED)



