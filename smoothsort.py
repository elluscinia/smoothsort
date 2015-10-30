# -*- coding: utf-8 -*-
import random
import heapq
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

size = 200
# mass - входной массив данных
mass = [530, 15, 140, 801, 881, 166, 37, 174, 516, 87, 324, 484, 275, 939, 218, 107, 340, 105, 656, 992, 5, 960, 235, 686, 803, 215, 579, 554, 876, 779, 49, 28, 648, 437, 784, 774, 654, 552, 601, 64, 499, 624, 270, 301, 721, 853, 378, 121, 580, 288, 907, 527, 939, 285, 37, 474, 276, 507, 73, 8, 917, 677, 818, 724, 159, 827, 626, 229, 812, 549, 15, 895, 142, 798, 785, 22, 574, 127, 429, 212, 920, 925, 357, 272, 598, 569, 984, 191, 467, 664, 995, 131, 103, 856, 811, 895, 895, 333, 509, 157, 419, 387, 3, 507, 231, 381, 656, 114, 442, 11, 301, 878, 418, 286, 930, 547, 726, 489, 493, 13, 986, 883, 713, 50, 944, 762, 211, 375, 591, 883, 995, 592, 977, 185, 390, 985, 221, 700, 941, 727, 336, 202, 868, 116, 746, 165, 795, 442, 588, 910, 729, 457, 403, 774, 697, 86, 637, 521, 883, 462, 673, 934, 767, 932, 499, 856, 408, 285, 706, 942, 825, 799, 269, 731, 266, 194, 728, 924, 69, 61, 287, 76, 936, 91, 732, 766, 150, 837, 586, 654, 510, 630, 444, 300, 790, 177, 685, 26, 187, 235]
# формируем список чисел Леонардо, по которым будут сформированы размеры куч
leonardo = massLeonardo(size)
leonardo.reverse()

# формируем список куч
massHeaps = [] # финальный список куч
m = 0 # хвост предыдущей части и начало следующей
for i in leonardo:
    if len(mass) - m >= i:
        # если оставшаяся нераспределённая часть входного массива данных
        # больше или равна очередному числу Леонардо
        massHeaps.append(mass[m : m+i])
        # переходим к оставшейся нераспределённой части
        m += i
# восстанавливаем свойство кучи для каждой кучи
for i in massHeaps:
    heapq.heapify(i)
# так как кучи неубывающие, конечный результат будет заполняться с начала - минимального элемента 
# до максимального элемента последовательности, то меняем порядок куч на обратный
massHeaps.reverse()

# ищем индексы элементов куч для левогой и правой подкуч
def make_index(i, indexes):

    a = 2*i + 1
    b = 2*i + 2

    indexes.append(a)
    indexes.append(b)

    return indexes
# делим кучи на подкучи
def heapdivision(heap):
    heapleft = []
    heapright = []
    index = 0
    indexes = [1]
    indexes2 = [2]
    while indexes[-1] < len(heap):
        make_index(indexes[index], indexes)
        make_index(indexes2[index], indexes2)
        index += 1
    for i in indexes:
        try: 
            heapleft.append(heap[i])
        except:
            # если обратились к элементу кучи, которого нет
            # то и пофиг на него
            pass
    for i in indexes2:
        try: 
            heapright.append(heap[i])
        except:
            # если обратились к элементу кучи, которого нет
            # то и пофиг на него
            pass
    return heapleft, heapright

print massHeaps

# основной алгоритм
result = []
while (massHeaps != []):
    flag = 0
    # находим минимальный элемент среди корней куч
    min_index = massHeaps.index(min(massHeaps))
    # меняем его местами с корнем первой кучи
    heapq.heapreplace(massHeaps[min_index], heapq.heapreplace(massHeaps[0], massHeaps[massHeaps.index(min(massHeaps))][0]))
    # т.к. корень первой кучи будет в дальнейшем удален, размер кучи
    # уменьшится на 1 -> образуются две кучи из его левого и правого поддерева\
    if len(massHeaps[0]) > 1:
        heapLeft, heapRight = heapdivision(massHeaps[0])
        flag = 1
    else:
        pass
    # удаляем корень первой кучи - это минимальный элемент из всех возможных
    minimum = heapq.heappop(massHeaps[0])
    # ставим его в конечную последовательность чисел
    result.append(minimum)
    # удалим первый элемент списка и вставим его ранее полученные поддеревья
    massHeaps.pop(0)
    # добавим две получившиеся кучи в начало всей последовательности куч
    if flag == 1:
        massHeaps.insert(0, heapLeft)
        massHeaps.insert(0, heapRight)

print result