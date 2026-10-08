def selection_sort(array: list[int]) -> int:
    """сортирует массив выбором на месте и возвращает число обменов."""
    swaps = 0
    for index in range(len(array) - 1):
        min_index = index
        for other in range(index + 1, len(array)):
            if array[other] < array[min_index]:
                min_index = other
        if min_index != index:
            array[index], array[min_index] = array[min_index], array[index]
            swaps += 1
    return swaps
