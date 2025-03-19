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


# Ejemplo de uso:
arr = [64, 34, 25, 12, 22, 11, 90]
print("Array original:", arr)

comb_sort(arr)

print("Array ordenado:", arr)
