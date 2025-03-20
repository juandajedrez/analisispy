import time


def comb_sort(arr):
    def get_next_gap(gap):
        gap = (gap * 10) // 13  # Reduce el gap según un factor
        return max(1, gap)  # El gap nunca debe ser menor a 1

    n = len(arr)
    gap = n
    swapped = True

    while gap != 1 or swapped:
        gap = get_next_gap(gap)
        swapped = False

        for i in range(0, n - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swapped = True


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
    entradas_ordenadas = comb_sort(bib_entries)

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
salida_bib = "../extract_information/conections/archivos_csv/ordenadoCombSort.bib"

limpiar_y_ordenar_bibtex(archivo_bib, salida_bib)
