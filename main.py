import random
from time import perf_counter

from sorts.insertion_sort import insertion_sort
from sorts.quick_sort import quick_sort
from sorts.selection_sort import selection_sort


def generate_array(n: int) -> list[int]:
    array = []
    for _ in range(n):
        array.append(random.randint(0, 100))
    array[-1] = array[0]
    random.shuffle(array)
    return array


def read_array(filename: str) -> list[int]:
    array = []
    with open(filename, encoding='utf-8-sig') as file:
        for number in file.read().split():
            array.append(int(number))
    return array


def remove_duplicates(array: list[int]) -> list[int]:
    unique = []
    for number in array:
        if not unique or number != unique[-1]:
            unique.append(number)
    return unique


def show_results(original: list[int], unique: bool = False) -> None:
    algorithms = [
        ('сортировка выбором', selection_sort),
        ('быстрая сортировка', quick_sort),
        ('сортировка вставками', insertion_sort),
    ]

    for name, sort in algorithms:
        array = original.copy()
        start = perf_counter()
        swaps = sort(array)
        elapsed = perf_counter() - start

        print('\n' + name)
        print(f'время: {elapsed:.6f} с')
        print('количество перестановок:', swaps)
        if unique:
            print('отсортированные возраста без повторов:', remove_duplicates(array))
        else:
            print('отсортированный массив:', array)


def main() -> None:
    while True:
        try:
            n = int(input('введите размер массива: '))
        except ValueError:
            print('нужно ввести целое число.')
            continue
        if n >= 2:
            break
        print('для повторяющихся чисел нужно минимум 2 элемента.')

    # часть а: случайный массив.
    original = generate_array(n)
    print('\nчасть а. исходный массив:', original)
    show_results(original)

    # часть б: возраста из файла.
    ages = read_array('data.txt')
    print('\nчасть б. количество возрастов:', len(ages))
    show_results(ages, unique=True)


if __name__ == '__main__':
    main()
