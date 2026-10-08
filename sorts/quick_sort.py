def quick_sort(array: list[int]) -> int:
    """сортирует массив по возрастанию на месте и возвращает число обменов."""
    swaps = 0

    def sort_part(first: int, last: int) -> None:
        """сортирует участок от first до last включительно и считает обмены."""
        nonlocal swaps
        while first < last:
            index = first
            contr_index = last
            step = -1
            condition = True

            while index != contr_index:
                if (array[index] > array[contr_index]) == condition:
                    array[index], array[contr_index] = array[contr_index], array[index]
                    swaps += 1
                    index, contr_index = contr_index, index
                    step = -step
                    condition = not condition
                contr_index += step

            if index - first < last - index:
                sort_part(first, index - 1)
                first = index + 1
            else:
                sort_part(index + 1, last)
                last = index - 1

    sort_part(0, len(array) - 1)
    return swaps
