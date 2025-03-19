from pybtex.database import parse_file, BibliographyData
import time

class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key


def insert(root, key):
    if root is None:
        return TreeNode(key)

    if key < root.val:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)

    return root


def inorder_traversal(root, res):
    if root:
        inorder_traversal(root.left, res)
        res.append(root.val)
        inorder_traversal(root.right, res)


def tree_sort(arr):
    if not arr:
        return arr

    root = None
    for key in arr:
        root = insert(root, key)

    sorted_arr = []
    inorder_traversal(root, sorted_arr)
    return sorted_arr


# Example usage
#arr = [5, 3, 7, 2, 8, 1, 4, 6]
#sorted_arr = tree_sort(referencias)
#print("Sorted array:", sorted_arr)

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

    print(f"✅ Ordenamiento completado en {tiempo_total:.3f} ms. Revisa el archivo: {archivo_salida}")

# 📌 Uso:
archivo_bib = "../extract_information/conections/archivos_csv/unificado.bib"
salida_bib = "../extract_information/conections/archivos_csv/ordenadoTreeSort.bib"

limpiar_y_ordenar_bibtex(archivo_bib, salida_bib)