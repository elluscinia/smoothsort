# -*- coding: utf-8 -*-
"""
Алгоритм плавной сортировки за O(lgN)
"""
import random
import unittest
import sys
import time

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
            else: # для остальных случаев необходимо найти левого и правого ребёнка
                childRight = roots[j] - 1 # правый ребёнок всегда стоит рядом со своим родителем
                if indexesHeapsSizes[j] > 1: # в случае, если куча размером больше 3
                    childLeft = roots[j]-heapsSizes[indexesHeapsSizes[j]-2]-1 # мы наверняка знаем размеры детей левого ребёнка (по индексам), ищем с конца
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
            pos -= 1 # образовалась новая куча из двух существующих, общее кол-во куч уменьшилось
            indexesHeapsSizes[pos] += 1 # увеличиваем размер последней кучи (объединение двух последних куч новым элементом)
        else: # добавляется новый элемент - куча размером 1
            indexesHeapsSizes.append(0)
            pos += 1
        # отсортируем получившиеся корни куч
        sortRoots(array, heapsSizes, indexesHeapsSizes, pos)
    return array

def destroySmoothHeap(array, heapsSizes, indexesHeapsSizes, pos):
    """
    Функция разрушает кучу, упорядочивая элементы в исходном массива с конца
    :param array: куча из куч размерами чисел Леонардо
    :param heapsSizes: список размеров куч
    :param indexesHeapsSizes: список индексов размеров используемых куч
    :param pos: последняя куча
    :param return: упорядоченный массив чисел
    """
    for i in xrange(len(array)-2,0,-1): # выбираем элементы, начиная с предпоследнего, последний элемент 100% наибольший
        if indexesHeapsSizes[pos] == 0: # куча размером 1
            indexesHeapsSizes.pop() # просто удаляем её из общего списка вершин, тем самым исключая из дальнейшего рассмотрения
            pos -= 1 
        else:
            indexesHeapsSizes[pos] -= 1 # уменьшаем размер кучи, L(x-1)
            if indexesHeapsSizes[pos] == 0:
                indexesHeapsSizes.append(0)
            else:
                # добавим кучу L(x-2)
                indexesHeapsSizes.append(indexesHeapsSizes[pos]-1)
            pos += 1 # т.к. разбили кучу на подкучи, увеличилось число куч
        sortRoots(array, heapsSizes, indexesHeapsSizes, pos) # отсортируем после "удаления" новые корни
    return array

def siftDown(array, heapsSizes, indexesHeapsSizes, pos, node):
    """
    Функция просеивания (восстановление свойств кучи)
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
    pos = 0 # индекс последнего элемента в списке индексов размеров используемых куч
    heapsSizes = numbersLeonardo(len(array)) # находим размеры куч, которые будут использованны
    indexesHeapsSizes = [0] # для начала
    array = createSmoothHeap(array, heapsSizes, indexesHeapsSizes, pos) # создаем кучу из куч размерами чисел Леонардо
    pos = len(indexesHeapsSizes)-1
    array = destroySmoothHeap(array, heapsSizes, indexesHeapsSizes, pos) # создаем упорядоченный массив
    return array

class SmoothSortTestCase (unittest.TestCase):
    def test_run(self):
        """
        Тестирование правильности сортировки на 2000 случайных целых числах
        """
        data = []
        for i in xrange(0, 2000):
            data.append(random.randint(500,1000))
        self.assertEqual(smoothsort(data), sorted(data))

def argumentHandling(inputFileName, outputFileName):
    """
    Функция обработки аргументов командной строки
    :param inputFileName: полный путь к файлу чтения
    :param outputFileName: полный путь к файлу записи
    :return None:
    """
    try:
        inputFile = open(inputFileName, 'r')
        if outputFileName == None:
            outputFile = open('smoothsort.txt', 'w')
            print 'Файл для записи не был задан'
            print 'Файл был создан в директории запуска программы: smoothsort.txt'
        else:
            outputFile = open(outputFileName, 'w')
    except IOError as e:
        print 'Файл для чтения не существует или не доступен'
    except Exception as e:
        print 'Неизвестная ошибка:'
        print e
    else:
        inputData = inputFile.read()
        inputFile.close()
        data = [int(x) for x in inputData.split('\n') if x != '']
        timeStart = time.time()
        data = smoothsort(data)
        timeEnd = time.time()
        for x in data:
            outputFile.write('%s\n' % x)
        outputFile.close()
        print 'Время работы алгоритма сортировки:', timeEnd - timeStart, 'seconds'
    return None

if __name__ == '__main__':
    if len(sys.argv) == 2:
        argumentHandling(str(sys.argv[1]), None)
    elif len(sys.argv) == 5:
        argumentHandling(str(sys.argv[sys.argv.index('--input') + 1]), str(sys.argv[sys.argv.index('--output') + 1]))
    else:
        print 'Неверно введены параметры для запуска программы'
        print '--input полный_путь_к_файлу_чтения --output полный_путь_к_файлу_записи'
else:
    print 'import smoothsort module'