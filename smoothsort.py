# -*- coding: utf-8 -*-
"""
Реализация алгоритма плавной сортировки
"""
import heapq
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
    numbers = [1, 1] # начальные элементы для последовательности чисел Леонардо
    nextNumber = numbers[-1] + numbers[-2] + 1
    while len(numbers) >= 2 and size > nextNumber:
        numbers.append(nextNumber)
        nextNumber = numbers[-1] + numbers[-2] + 1
    numbers.reverse()
    return numbers

def doListHeaps(data):
    """
    Функция формирует список куч по числам Леонардо
    :param data: входной массив данных
    :param return: выходной список с кучами
    """
    # формируем список чисел Леонардо для входной последовательности
    leonardoNumbers = numbersLeonardo(len(data))
    # формируем список куч
    listHeaps = [] # финальный список куч
    m = 0 # хвост предыдущей части и начало следующей
    for i in leonardoNumbers:
        if len(data) - m >= i:
            # если оставшаяся нераспределённая часть входного массива данных больше или равна очередному числу Леонардо
            listHeaps.append(data[m : m+i])
            # переходим к оставшейся нераспределённой части
            m += i
    # восстанавливаем свойство кучи для каждой кучи
    for i in listHeaps:
        heapq.heapify(i)
    # так как кучи неубывающие, конечный результат будет заполняться с начала - минимального элемента 
    # до максимального элемента последовательности, то меняем порядок куч на обратный
    listHeaps.reverse()
    return listHeaps

def countIndexes(i, indexes):
    """
    Функция формирует список элементов по заданным индексам
    :param i: индекс, потомки которого ищутся
    :param indexes: список индексов
    :return indexes: список индексов
    """
    indexes.append(2*indexes[i]+1)
    indexes.append(2*indexes[i]+2)

    return indexes

def getList(indexPart, heap):
    """
    Функция формирует подкучу из заданного списка индексов и исходной кучи
    :param indexPart: список индексов 
    :param heap: исходная куча
    :return heapPart: найденная подкуча
    """
    heapPart = []
    for i in indexPart:
        if i < len(heap):
            heapPart.append(heap[i])

    return heapPart

def heapDivision(heap):
    """
    Функция деления кучи на левые и правые подкучи
    :param heap: куча для деления
    :param return: возвращает кортеж из левой и правой подкучи соответсвенно
    """
    heapleft = []
    heapright = []
    index = 0
    indexesLeft = [1] # список индексов для элементов левой подкучи
    indexesRight = [2] # список индексов для элементов правой подкучи
    while indexesLeft[-1] < len(heap): 
        # исходя из логики построения куч, левая подкуча никогда не будет меньше правой

        # считаем индексы для левой подкучи
        indexesLeft = countIndexes(index, indexesLeft)

        # считаем индексы для правой подкучи
        indexesRight = countIndexes(index, indexesRight)

        index += 1

    # составляем списки левой и правой подкуч
    heapleft = getList(indexesLeft, heap)
    heapright = getList(indexesRight, heap)

    return heapleft, heapright

def smoothSort(listHeaps):
    """
    Функция плавной сортировки
    :param listHeaps: кучи
    :param return: отсортированная последовательность данных
    """
    result = []
    while (listHeaps != []):
        # чтобы не писать пустые подкучи
        flag = 0
        # находим минимальный элемент среди корней куч
        min_index = listHeaps.index(min(listHeaps))
        # меняем его местами с корнем первой кучи
        heapq.heapreplace(listHeaps[min_index], heapq.heapreplace(listHeaps[0], listHeaps[listHeaps.index(min(listHeaps))][0]))
        # т.к. корень первой кучи будет в дальнейшем удален, размер кучи
        # уменьшится на 1 -> образуются две кучи из его левого и правого поддерева
        if len(listHeaps[0]) > 1:
            heapLeft, heapRight = heapDivision(listHeaps[0])
            flag = 1
        # удаляем корень первой кучи - это минимальный элемент из всех возможных
        minimum = heapq.heappop(listHeaps[0])
        # ставим его в конечную последовательность чисел
        result.append(minimum)
        # удалим первый элемент списка и вставим его ранее полученные поддеревья
        listHeaps.pop(0)
        # добавим две получившиеся кучи в начало всей последовательности куч
        if flag == 1:
            listHeaps.insert(0, heapLeft)
            listHeaps.insert(0, heapRight)
    return result

class SmoothSortTestCase (unittest.TestCase):
    def test_run(self):
        """
        Тестирование правильности сортировки на 2000 случайных целых числах
        """
        data = []
        for i in xrange(0, 2000):
            data.append(random.randint(500,1000))
        listHeaps = doListHeaps(data)
        self.assertEqual(smoothSort(listHeaps), sorted(data))

def workFile(inputFileName, outputFileName):
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
        data = smoothSort(doListHeaps(data))
        timeEnd = time.time()
        for x in data:
            outputFile.write('%s\n' % x)
        outputFile.close()
        print 'Время работы алгоритма сортировки:', timeEnd - timeStart
    return None

if __name__ == '__main__':
    if len(sys.argv) == 2:
        workFile(str(sys.argv[1]), None)
    elif len(sys.argv) == 5:
        workFile(str(sys.argv[sys.argv.index('--input') + 1]), str(sys.argv[sys.argv.index('--output') + 1]))
    else:
        print 'Неверно введены параметры для запуска программы'
        print '--input полный_путь_к_файлу_чтения --output полный_путь_к_файлу_записи'
else:
    print 'import SmoothSort module'
    print 'by el.luscinia'
