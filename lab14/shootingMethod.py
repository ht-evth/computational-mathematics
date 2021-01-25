import numpy as np

def calculateKq(funcs, x, y, h):
    """ Вычисление коэф-тов к1-к4 """

    k1 = np.array([h * f(x, *y) for f in funcs])

    curX = x+h/2
    curY = y + k1 / 2
    k2 = np.array([h * f(curX, *curY) for f in funcs])

    curY = y + k2 / 2
    k3 = np.array([h * f(curX, *curY) for f in funcs])

    curX = x+h
    curY = y + k3
    k4 = np.array([h * f(curX, *curY) for f in funcs])

    return k1, k2, k3, k4

def RungeKutta(funcs, init, a, b, h):
    """
    Метод Рунге-Кутта 4 порядка
    на заданном отрезке [a; b] с заданным шагом h
    при начальных условиях init для функций системы funcs

    возвращает вектор X и матрицу Y, в которой Y[i] соответствует X[i]
    """

    # сгенерировать массив точек от a до b с шагом h
    stepByStep = np.concatenate([np.arange(a, b, h), [b]])
    y = [init, ]

    # для каждой точки вычисляем список новых приближенных
    # значений для каждой функции из заданной системы
    for x in stepByStep[:-1]:

        # вычислить коэф-ты
        k1, k2, k3, k4 = calculateKq(funcs, x, y[-1], h)
        k = (k1 + k2 * 2 + k3 * 2 + k4) / 6
        # вычислить значение
        y.append(y[-1] + k)

    return stepByStep, np.array(y)

def autoStep(funcs, init, a, b, eps):
    """
    Метод Рунге-Кутта 4 порядка с автоматическим выбором шага
    """

    minH = (b-a)/ 10000

    # так как порядок метода = 4
    # за новую точность примем eps = eps (стар.) / 2^(4 + 1)
    eps1 = eps / 32

    # функция вычисления длины очередного шага
    def calculateStep(funcs, y, a, b, h, eps):
        # если выходим за пределы отрезка
        if h > b - a:
            # шаг = длине отрезка
            h = b - a

        while True:
            # вычисляем коэф-ты и ошибку
            k1, k2, k3, k4 = calculateKq(funcs, a, y, h)
            err = (abs(k1 - k2 - k3 + k4)*(2/3)).max()

            # если достигли заданной точности, шаг найден
            #if h < minH or err < eps:
            if err < eps:
                return h, err

            # уменьшаем шаг и повторяем вычисления
            h /= 2

    # начальный шаг равен длине отрезка
    h = b - a

    # выбираем начальную точку
    currentPoint = a

    y = init

    # инициализация векторов для хранения результатов
    X, resultY = [a], [y, ]

    # пока не дошли до конца отрезка
    while currentPoint < b:
        # вычисляем новый шаг и значение ошибки
        h, err = calculateStep(funcs, y, currentPoint, b, h, eps)

        # вычисляем новые значения функций с начальными данными из прерыдущей итерации
        _, newY = RungeKutta(funcs, resultY[-1], currentPoint, currentPoint + h, h)

        # переходим к следующей точке
        currentPoint += h

        # сохраняем результаты
        X.append(currentPoint)
        resultY.append(newY[-1])

        # если локальная погрешность слишком маленькая, можно попытаться
        # продолжить вычислять с шагом в 2 раза больше
        if err < eps1 or h < minH:
            h *= 2

    return X, np.array(resultY)

def chord(p, q, func):
    return q - func(q) * (p - q) / (func(p)-func(q))


def secantMethod(func, prevX, x, eps):

    # Деление на 0 или превышение числа итераций
    # Подразумевает отсутствие решения
    with np.errstate(all='raise'):
        try:
            for iterations in range(1000):
                curX = chord(prevX, x, func)
                # если достигнули заданную точность - выходим
                if abs(curX - x) < eps:
                    break
                x, prevX = curX, x
            else:
                iterations = np.Inf

            result = x + (curX - x)/2

        # обработка ошибки вычислений
        except FloatingPointError:
            result, iterations = np.NaN, np.Inf

        return result, iterations



def funcForLastValues(funcs, a, b, eps, getFirst):
    """ Возвращает функцию для вычисления приблизительных значений в последней точке функции """
    def func(par):
        values = np.array(getFirst(par))
        _, y_mx = autoStep(funcs, values, a, b, eps)
        return y_mx[-1]

    return func


def checkLastValues(getLastVal, secondCondition):
    """ получить уравнение для правого гр. условия исходя из приближения для левого гр условия """
    def func(a):
        return secondCondition(*getLastVal(a))

    return func


def method(system, a, b, eps, approx0, approx1, getFirst, secondCondition):
    """
    Поиск левых первых значений и решение задачи Коши методом Рунге-Кутта.

    :param system: система диф. уравнений
    :param a: левое граничное условие
    :param b: правое граничное условие
    :param eps: заданная тончность вычислений
    :param approx0: приближение к y(a) или u(a)
    :param approx1: -- // --
    :param getFirst: функция, которая по одному из значений y(a), u(a) возвращает оба
    :param secondCondition: левая часть граничного условия вида fi2(y(b), u(b)) = 0.

    """

    getLastVal = funcForLastValues(system, a, b, eps, getFirst)
    checkLastVal = checkLastValues(getLastVal, secondCondition)


    # Метод секущих для изменения параметра a
    changedParamA, _ = secantMethod(checkLastVal, approx0, approx1, eps)
    y_a, u_a = getFirst(changedParamA)

    # сформируем список начальных параметров a
    initA = np.array([y_a, u_a])

    # решаем методом Рунге-Кутта
    return autoStep(system, initA, a, b, eps)