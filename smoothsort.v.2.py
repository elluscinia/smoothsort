# -*- coding: utf-8 -*-
"""
Алгоритм плавной сортировки за O(lgN)
"""
import random

def numbersLeonardo(size):
    """
    Функция формирует список чисел Леонардо, являющихся размерами куч
    :param size: размер входного массива для плавной сортировки
    :param return: возвращает список чисел Леонардо
    """
    numbers = [1, 3] # начальные элементы для последовательности чисел Леонардо
    nextNumber = numbers[-1] + numbers[-2] + 1
    while size > nextNumber:
        numbers.append(nextNumber)
        nextNumber = numbers[-1] + numbers[-2] + 1
    return numbers

def sortRoots(array, heapsSizes, indexesHeapsSizes, pos):
    """
    Функция сортирует корни куч в порядке возрастания
    :param array: список элементов
    :param heapsSizes: список размеров куч
    :param indexesHeapsSizes: список индексов размеров используемых куч
    :param pos: вершина последней кучи
    :param return: массив чисел
    """
    roots = [] # массив корней
    for i in xrange(0, len(indexesHeapsSizes)): # перебор по количеству индексов используемых куч
        if i == 0: # для первой кучи (самой большой)
            roots.append(heapsSizes[indexesHeapsSizes[i]] - 1) # просто берём её размер и для вычисления индекса вершины вычитаем 1, т.к. индексация с нуля
        else:
            roots.append(roots[i-1]+heapsSizes[indexesHeapsSizes[i]]) # в остальных случаях к значению предыдущего индекса корня прибавляем размер текущей кучи
    
    lastRoot = len(roots) - 1 # последний корень (его индекс в общем массиве чисел)
    for i in xrange(0, len(roots)): # перебор по количеству корней 
        for j in xrange(len(roots)-1, i, -1): # в обратном порядке, начиная с последнего индекса с шагом 1
            if indexesHeapsSizes[j] == 0: # куча имеет размер 1 (индекс в списке размеров куч равен 0)
                if array[roots[j]] < array[roots[j-1]]: # если корень меньше предыдущего, то они меняются местами
                    array[roots[j]], array[roots[j-1]] = array[roots[j-1]], array[roots[j]]
                    # для того, чтобы не делать просейку для корней, которые не были изменены
                    if j-1 < lastRoot:
                        lastRoot = j-1
            else: # для остальных случаев необхожимо найти левого и правого ребёнка
                childRight = roots[j] - 1 # правый ребёнок всегда стоит рядом со своим родителем
                if indexesHeapsSizes[j] > 1: # в случае, если куча размером больше 3
                    childLeft = roots[j]-heapsSizes[indexesHeapsSizes[j]-2]-1 # мы навершняка знаем размеры детей левого ребёнка (по индексам), ищем с конца
                else:
                    childLeft = roots[j]-2 # для кучи из 3-х элементов
                # если корень соседней (предыдущей) кучи больше правого и левого ребёнка, а также самого корня текущей кучи
                if array[roots[j-1]] > array[childRight] and array[roots[j-1]] > array[childLeft] and array[roots[j-1]] > array[roots[j]]:
                    # меняем местами корни
                    array[roots[j]], array[roots[j-1]] = array[roots[j-1]], array[roots[j]]
                    if j-1 < lastRoot:
                        lastRoot = j-1 

    # восстановим свойства куч, для которых были изменены корни
    while lastRoot <= pos:
        siftDown(array, heapsSizes, indexesHeapsSizes, lastRoot, roots[lastRoot])
        lastRoot += 1
    return array

def createSmoothHeap(array, heapsSizes, indexesHeapsSizes, pos):
    """
    Функция создаёт кучу из куч размеров чисел Леонардо
    :param array: массив чисел
    :param heapsSizes: список размеров куч
    :param indexesHeapsSizes: список индексов размеров используемых куч
    :param pos: указатель на вершину последней кучи
    :param return: массив чисел
    """
    for i in xrange(1,len(array)): # выбираются элементы, начиная со второго
        if pos > 0 and (indexesHeapsSizes[pos-1] == indexesHeapsSizes[pos]+1 or indexesHeapsSizes[pos-1] == 0): # элемент становится новым корнем двух предыдущих куч
            indexesHeapsSizes.pop()
            pos -= 1 # имеет значение индекса последнего элемента списка используемых размеров куч
            indexesHeapsSizes[pos] += 1 # увеличиваем размер последней кучи (объединение двух последних куч новым элементом)
        else: # добавляется новый элемент - куча размером 1
            indexesHeapsSizes.append(0)
            pos += 1
        # отсортируем получившиеся корни куч
        sortRoots(array, heapsSizes, indexesHeapsSizes, pos)
    return array

def siftDown(array, heapsSizes, indexesHeapsSizes, pos, node):
    """
    Функция просейки (восстановление свойств кучи)
    :param array: массив чисел
    :param heapsSizes: список размеров куч
    :param indexesHeapsSizes: список индексов размеров используемых куч
    :param pos: вершина кучи
    :param node: индекс вершины кучи в массиве чисел, для которой выполняется функция
    :param return: массив чисел
    """
    i = 1
    # просмотрим все подкучи кучи, для которой выполняется просейка
    while i <= indexesHeapsSizes[pos]:
        # ищем левого и правого ребёнка
        childRight = node - 1
        if i == indexesHeapsSizes[pos]:
            childLeft = node - 2
        else:
            childLeft = node - heapsSizes[indexesHeapsSizes[pos]-i-1]-1
        # ищем наибольшего ребёнка
        if array[childRight] < array[childLeft]:
            maxChild = childLeft
            i += 1
        else:
            maxChild = childRight
            i += 2
        # вместо корня подставляем значение наибольшего ребёнка
        if array[maxChild] > array[node]:
            array[maxChild], array[node] = array[node], array[maxChild]
            node = maxChild
        else:
            break
    return array

def smoothsort(array):
    """
    Функция плавной сортировки
    :param array: исходный массив чисел
    :param return: упорядоченный массив
    """
    pos = 0 #индекс последнего элемента в списке индексов размеров используемых куч
    heapsSizes = numbersLeonardo(len(array)) # находим размеры куч, которые будут использованны
    indexesHeapsSizes = [0] # для начала
    array = createSmoothHeap(array, heapsSizes, indexesHeapsSizes, pos) # создаем кучу из куч размерами чисел Леонардо
    return array

if __name__ == '__main__':
    array = [85, 54, 107, 49, 46, 15, 37, 27, 48, 31, 101, 103, 13, 71, 78, 8, 106, 34, 35, 66, 41, 89, 18, 23, 29, 70, 72, 86, 39, 99, 20, 62, 17, 6, 25, 90, 12, 67, 82, 75, 94, 43, 9, 7, 3, 42, 50, 105, 98, 40, 65, 91, 26, 47, 102, 38, 11, 88, 64, 16, 87, 2, 55, 76, 57, 97, 74, 59, 60, 22, 104, 80, 73, 32, 5, 28, 51, 63, 19, 93, 92, 21, 68, 33, 58, 56, 53, 10, 79, 83, 61, 95, 24, 14, 84, 69, 44, 96, 36, 77, 45, 81, 52, 30, 1, 108, 100, 4]
    a = smoothsort(array)