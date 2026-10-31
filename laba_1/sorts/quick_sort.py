def quick_sort(array: list[int], left: int = 0, right: int | None = None) -> int:
    """сортирует участок массива на месте и возвращает число обменов."""
    if right is None:
        right = len(array) - 1
    if left >= right:
        return 0

    i, j = left, right
    pivot = array[(left + right) // 2 + 1]
    swaps = 0

    while i <= j:
        while array[i] < pivot:
            i += 1
        while array[j] > pivot:
            j -= 1

        if i <= j:
            if i != j and array[i] != array[j]:
                array[i], array[j] = array[j], array[i]
                swaps += 1
            i += 1
            j -= 1

    if left < j:
        swaps += quick_sort(array, left, j)
    if i < right:
        swaps += quick_sort(array, i, right)

    return swaps
