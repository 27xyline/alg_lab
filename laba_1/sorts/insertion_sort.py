def insertion_sort(array: list[int]) -> int:
    """сортирует массив вставками на месте и возвращает число обменов соседей."""
    swaps = 0
    for index in range(1, len(array)):
        position = index
        while position > 0 and array[position] < array[position - 1]:
            array[position], array[position - 1] = array[position - 1], array[position]
            swaps += 1
            position -= 1
    return swaps
