# -*- coding: utf-8 -*-
def numLeonardo(n):
    """
    Функция считает число Леонардо от n
    :param n: число n
    :param return: возвращает число Леонардо
    """
    if (n == 0 or n == 1):
        return 1
    else:
        return numLeonardo(n-1) + numLeonardo(n-2) + 1

def massLeonardo(size):
    """
    Функция формирует список чисел Леонардо, являющихся размерами куч
    :param size: размер входного массива для плавной сортировки
    :param return: возвращает список чисел Леонардо
    """
    numbers = [1, 1]
    i = 2
    while size > numbers[-1] and len(numbers) >= 2 and size > (numbers[-1] + numbers[-2] + 1):
        numbers.append(numLeonardo(i))
        i = i + 1
    return numbers

print massLeonardo(200)
