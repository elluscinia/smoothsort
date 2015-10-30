# -*- coding: utf-8 -*-
import heapq
import random
import unittest

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
        a = 2*indexesLeft[index] + 1
        b = 2*indexesLeft[index] + 2

        indexesLeft.append(a)
        indexesLeft.append(b)

        # считаем индексы для правой подкучи
        c = 2*indexesRight[index] + 1
        d = 2*indexesRight[index] + 2

        indexesRight.append(c)
        indexesRight.append(d)

        index += 1

    # составляем списки левой и правой подкуч
    for i in indexesLeft:
        try: 
            heapleft.append(heap[i])
        except:
            # если обратились к элементу кучи, которого нет
            # вообще так плохо делать. но я искренне раскиваюсь
            pass
    for i in indexesRight:
        try: 
            heapright.append(heap[i])
        except:
            # если обратились к элементу кучи, которого нет
            # правда раскаиваюсь
            pass

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
    """
    Тест
    """
    def runTest(self):
        """
        Тестирование правильности сортировки на 2000 случайных целых числах
        """
        data = []
        for i in xrange(0, 2000):
            data.append(random.randint(0,1000))
        listHeaps = doListHeaps(data)
        self.assertEqual(smoothSort(listHeaps), sorted(data))

if __name__ == '__main__':
    unittest.main()
else:
    print 'import SmoothSort module'