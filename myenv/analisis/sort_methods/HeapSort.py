import time


def heapify(arr, n, i):
    largest = i  # Initialize largest as root
    l = 2 * i + 1  # left = 2*i + 1
    r = 2 * i + 2  # right = 2*i + 2

    # See if left child of root exists and is
    # greater than root

    if l < n and arr[i] < arr[l]:
        largest = l

    # See if right child of root exists and is
    # greater than root

    if r < n and arr[largest] < arr[r]:
        largest = r

    # Change root, if needed

    if largest != i:
        (arr[i], arr[largest]) = (arr[largest], arr[i])  # swap

        # Heapify the root.

        heapify(arr, n, largest)


# The main function to sort an array of given size


def heapSort(arr):
    n = len(arr)

    # Build a maxheap.
    # Since last parent will be at (n//2) we can start at that location.

    for i in range(n // 2, -1, -1):
        heapify(arr, n, i)

    # One by one extract elements

    for i in range(n - 1, 0, -1):
        (arr[i], arr[0]) = (arr[0], arr[i])  # swap
        heapify(arr, i, 0)


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
    entradas_ordenadas = heapSort(bib_entries)

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
salida_bib = "../extract_information/conections/archivos_csv/ordenadoHeapSort.bib"

limpiar_y_ordenar_bibtex(archivo_bib, salida_bib)
