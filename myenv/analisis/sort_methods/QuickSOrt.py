"""
==============================
https://parzibyte.me/blog
==============================
"""

import time


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


def tree_sort(bib_entries):
    claves = list(bib_entries.keys())
    quicksort(claves, 0, len(claves) - 1)
    return [bib_entries[clave] for clave in claves]


def limpiar_y_ordenar_bibtex(archivo_entrada, archivo_salida):
    with open(archivo_entrada, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    bib_entries = {}
    entrada_actual = []
    clave_actual = None

    for linea in lineas:
        linea_limpia = linea.strip()

        if linea_limpia.lower().startswith("doi:"):
            continue  # Elimina la línea DOI

        if linea_limpia.startswith("@"):
            if clave_actual and entrada_actual:
                bib_entries[clave_actual] = "\n".join(entrada_actual)

            clave_actual = linea_limpia.split("{", 1)[1].split(",", 1)[0].strip()
            entrada_actual = [linea_limpia]

        else:
            entrada_actual.append(linea_limpia)

    if clave_actual and entrada_actual:
        bib_entries[clave_actual] = "\n".join(entrada_actual)

    # Medir tiempo antes de ordenar
    inicio = time.time()

    # Ordenar con TreeSort
    entradas_ordenadas = tree_sort(bib_entries)

    # Medir tiempo después de ordenar
    fin = time.time()
    tiempo_total = (fin - inicio) * 1000  # Convertir a milisegundos

    with open(archivo_salida, "w", encoding="utf-8") as f:
        for entrada in entradas_ordenadas:
            f.write(entrada + "\n\n")

    print(
        f"✅ Ordenamiento completado en {tiempo_total:.3f} ms. Revisa el archivo: {archivo_salida}"
    )


# 📌 Uso:
archivo_bib = "../extract_information/conections/archivos_csv/unificado.bib"
salida_bib = "../extract_information/conections/archivos_csv/ordenamientoQuickSort.bib"

limpiar_y_ordenar_bibtex(archivo_bib, salida_bib)
