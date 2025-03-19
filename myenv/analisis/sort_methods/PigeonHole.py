def pigeonhole_sort(arr):
    # Encontrar el valor mínimo y máximo del arreglo
    min_val = min(arr)
    max_val = max(arr)
    size = max_val - min_val + 1

    # Crear un array vacío de "pigeonholes"
    holes = [0] * size

    # Colocar cada elemento del arreglo en su correspondiente "pigeonhole"
    for num in arr:
        holes[num - min_val] += 1

    # Reconstruir el arreglo a partir de los "pigeonholes"
    sorted_arr = []
    for i in range(size):
        while holes[i] > 0:
            sorted_arr.append(i + min_val)
            holes[i] -= 1

    return sorted_arr


# Ejemplo de uso:
arr = [8, 3, 2, 7, 4, 6, 8]
print("Array original:", arr)

sorted_arr = pigeonhole_sort(arr)
print("Array ordenado:", sorted_arr)
