import tridiagAlg
import numpy as np
import math
import pylab

def numberToStr(number):
    """ функция преобразования числа в строку для красивого вывода"""
    tmp = str(number)
    while len(tmp) < 25:
        tmp += ' '

    return tmp

def main():

    # входные данные:

    # начало конец отрезка интегрирования
    start, end = 0, 1

    # точное решение
    func_u = lambda x: (math.exp(2 * x) / math.e) - 2 * math.exp(x) + math.e - 1

    # функции A(x), B(x), C(x)
    funcA = lambda x: -2
    funcB = lambda x: 0
    funcC = lambda x: 2 * math.exp(x)

    # коэф-ты
    F1, D1, E1 = 2, -1, 2 * math.e - 4
    F2, D2, E2 = 0, 1, 0

    # кол-во разбиений
    partition = [25, 50, 100, 200, 3200]


    # инициализация массива для хранения
    # норм погрешностей для разных разбиений
    norms = []

    # получим истинные значения
    realX = np.linspace(start, end, 500)
    realY = [func_u(x) for x in realX]

    # Запакуем входные данные в списки
    # для удобной передачи их в функции
    funcs = [funcA, funcB, funcC]
    coefs = (F1, D1, E1, F2, D2, E2)

    # рассмотрим каждое разбиение
    for n in partition:
        # вычислим шаг
        h = (end - start) / n
        # разобьём на n частей с шагом h
        listX = [start + i * h for i in range(n + 1)]

        # аппроксимация первого и второго порядка
        listY_first = tridiagAlg.first(n, h, listX, coefs, funcs)
        listY_second = tridiagAlg.second(n, h, listX, (start, end), coefs, funcs)

        # вычислим и сохраним нормы погрешностей
        norm1 = norm2 = 0
        for i in range(n + 1):
            norm1 = max(norm1, abs(listY_first[i] - func_u(listX[i])))
            norm2 = max(norm2, abs(listY_second[i] - func_u(listX[i])))
        norms.append((norm1, norm2))

        # Отрисовка графика
        pylab.plot(listX, listY_first, 'green', label='Результат для первого порядка')
        pylab.plot(listX, listY_second, 'red', label='Результат для второго порядка')
        pylab.plot(realX, realY, 'b--', label='Точное решение')
        pylab.legend()
        pylab.show()

    # печать норм погрешностей
    print('\nНормы погрешности')
    print('Разбиений' + ' ' * 17 + 'Первый порядок' + ' ' * 12 + 'Второй порядок')
    for i, part in enumerate(partition):
        norm1, norm2 = norms[i]
        print(numberToStr(part), numberToStr(norm1), numberToStr(norm2))


if __name__ == '__main__':
    main()
