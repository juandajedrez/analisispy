"""
==============================
https://parzibyte.me/blog
==============================
"""


def quicksort(arreglo, izquierda, derecha):
    if izquierda < derecha:
        indiceParticion = particion(arreglo, izquierda, derecha)
        quicksort(arreglo, izquierda, indiceParticion)
        quicksort(arreglo, indiceParticion + 1, derecha)


def particion(arreglo, izquierda, derecha):
    pivote = arreglo[izquierda]
    while True:
        # Mientras cada elemento desde la izquierda esté en orden (sea menor que el
        # pivote) continúa avanzando el índice
        while arreglo[izquierda] < pivote:
            izquierda += 1

        # Mientras cada elemento desde la derecha esté en orden (sea mayor que el
        # pivote) continúa disminuyendo el índice
        while arreglo[derecha] > pivote:
            derecha -= 1

        """
            Si la izquierda es mayor o igual que la derecha significa que no
            necesitamos hacer ningún intercambio
            de variables, pues los elementos ya están en orden (al menos en esta
            iteración)
        """
        if izquierda >= derecha:
            # Indicar "en dónde nos quedamos" para poder dividir el arreglo de nuevo
            # y ordenar los demás elementos
            return derecha
        else:
            # Nota: yo sé que el else no hace falta por el return de arriba, pero así el algoritmo es más claro
            """
            Si las variables quedaron "lejos" (es decir, la izquierda no superó ni
            alcanzó a la derecha)
            significa que se detuvieron porque encontraron un valor que no estaba
            en orden, así que lo intercambiamos
            """
            arreglo[izquierda], arreglo[derecha] = arreglo[derecha], arreglo[izquierda]
            """
                Ya intercambiamos, pero seguimos avanzando los índices
            """
            izquierda += 1
            derecha -= 1


"""
Modo de uso:
"""

arreglo = [
    5,
    1,
    2,
    1,
    1,
    3,
    5,
    1,
    5,
    1,
    99,
    231,
    234,
    12,
    121,
    312,
    123,
    123,
    12,
    312,
    321,
    312,
    31,
    23,
    12,
    3123,
    123,
]
print("Antes de ordenarlo: ")
print(arreglo)
quicksort(arreglo, 0, len(arreglo) - 1)
print("Después de ordenarlo: ")
print(arreglo)
