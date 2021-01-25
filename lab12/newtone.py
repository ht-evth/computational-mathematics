import numpy as np
from sympy import diff


def jacobian(varNames, diffFuncs, x):
    """
    Функция для вычисления матрицы Якоби
    """

    # создаем список: (имя переменной, значение переменной)
    listX = []
    for i in range(len(varNames)):
        listX.append((varNames[i], x[i]))

    # заменяем переменные и вычисляем
    result = []
    for row in diffFuncs:
        temp = []
        for dFunc in row:
            temp.append(dFunc.subs(listX))
        result.append(temp)

    return np.array(result, dtype=float)

def calcFunc(varNames, funcs, x):
    """
    Функция для вычисления значений функций системы
    """

    # создаем список: (имя переменной, значение переменной)
    listX = [(varNames[i], x[i]) for i in range(len(varNames))]

    # производим замену переменной и вычисляем результат
    result = []
    for func in funcs:
        result.append(func.subs(listX))

    return np.array(result, dtype=float)


def method(funcs, startVecX, eps, varNames):
    """
    Реализация метода Ньютона

    """
    # вычисление частных производных для матрицы Якоби
    diffFuncs = []
    for func in funcs:
        temp = []
        for name in varNames:
            temp.append(diff(func, name))
        diffFuncs.append(temp)


    maxIter = 2500  # ограничение на число итераций
    count = 0       # счётчик итераций

    # задаём начальный вектор X
    x = startVecX

    while True:
        # инкриментируем кол-во итераций
        count += 1

        Jacob = jacobian(varNames, diffFuncs, x)    # вычисление матрицы якоби
        F = calcFunc(varNames, funcs, x)            # вычисление значений функций F
        dx = np.linalg.solve(Jacob, -F)             # решение системы уравнений Jacob * dx = -F
        x += dx                                     # получаем новое значение х
        

        # проверка на выход из цикла (точность или кол-во итераций)
        if calculateNorm(dx) < eps or count > maxIter:
            break

    if count > maxIter:
        print('Количество итераций было превышено ({})...'.format(maxIter))

    return x, count

def calculateNorm(x):
    """ Вычислить норму: модуль корня из суммы квадратов """
    return abs(sum(var ** 2 for var in x) ** 0.5)


