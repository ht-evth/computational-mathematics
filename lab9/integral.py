import numpy as np
import numexpr as ne

def constStep(start, end, n, func):
    """
    Вычисляем интеграл методами прямоугольников, трапеции и Симпсона
    с фиксированным числом шагов
    """

    # Определяем длину шага путём деления отрезка на число шагов
    h = (abs(start) + abs(end)) / n
    print('Шаг = ', h)

    # Генерируем точки с заданным шагом
    args_x = [start + i * h for i in np.arange(n+1)]


    # вычисляем значения функции в заданных точках
    x = np.copy(args_x)
    args_y = ne.evaluate(func)
    y = np.copy(args_y)
    
    # метод прямоугольников
    x = 0
    rect = 0
    for i in range(1, len(y)):
        # средние прямоугольники
        # выбираем середину отрезка
        # вычисляем значение функции в середине этого отрезка
        x = args_x[i] - h/2
        value = ne.evaluate(func)
        # прибавляем к результату это значение, умноженное на h
        rect += value * h
    
    # метод трапеции

    # складываем крайние значения делённые на 2
    # добавляем остальные значения y[1], ... y[n - 1]
    # умножаем сумму на h
    trap = (y[0] + y[-1]) / 2
    for i in range(1, len(y) - 1):
        trap += y[i]
    trap *= h

    # метод симпсона

    # складываем крайние слагаемые в скобках
    simpson = y[0] + y[-1]
    multiplier = 4

    # прибавляем остальные значения y[1]...y[n-1]

    # умноженные на изменяющийся множитель multiplier = 4, 2, 4, ...
    # Реализованно через отнятие от числа 6 текущего множителя
    # (6 - 2) = 4, (6 - 4) = 2, (6 - 2) = 4, ...

    # умножаем сумму на h/3
    for i in range(1, len(y) - 1):
        simpson += multiplier * y[i]
        multiplier = 6 - multiplier

    simpson *= h/3
    
    return rect, trap, simpson


def autoRect(start, end, e, func):
    """
    Вычисление интеграла методом средних прямоугольников
    с автоматическим выбором числа шагов
    """
    cur = start
    result = 0
    h = 1
    stepsRect = 0

    # пока не дошли до конца отрезка
    while cur < end:
        stepsRect += 1
        x_i = cur + h
        if x_i > end:  # если вышли за пределы
            x_i = end  # устанавливаем граничное значение
            h = end - cur  # пересчитываем шаг

        result1 = result2 = 0

        # локальная формула средних прямоугольников для отрезка x[i-1], x[i]
        x = x_i - h / 2
        result1 = ne.evaluate(func) * h

        # т.к. мы считаем интеграл на x[i-1], x[i]
        # при использовании h/2 - получаем только половину отрезка
        # посчитаем более мелкие разбиения отрезка для точности
        # и просуммируем интегралы этих отрезков
        x = x_i - h / 4
        result2 += ne.evaluate(func) * h / 2
        x = x_i - 3 * h / 4
        result2 += ne.evaluate(func) * h / 2

        # проверка точности вычислений
        if abs(result2 - result1) > e:
            h /= 2  # уменьшаем шаг
            stepsRect -= 1  # отнимаем счетчик шагов
        else:
            result += result1  # суммируем результат
            cur += h  # двигаемся к следующему отрезку
            h *= 2

    return result, stepsRect

def autoTrap(start, end, e, func):
    """
    Вычисление интеграла методом трапеции
    с автоматическим выбором числа шагов
    """

    result = 0
    cur = start
    h = 1
    stepsTrap = 0

    # пока не дошли до конца отрезка
    while cur < end:
        stepsTrap += 1      # увеличить счетчик шагов
        if cur + h > end:
            h = end - cur

        result1 = result2 = 0

        # вычисляем значения функций в точках отрезка
        x = cur
        point1 = ne.evaluate(func)
        x = cur + h
        point2 = ne.evaluate(func)
        x = cur + h / 2
        point3 = ne.evaluate(func)

        # получаем интеграл на отрезке x[i-1], x[i]
        result1 = (point1 + point2) * h / 2

        # снова вычислим также интеграл на отрезке x[i-1], x[i] но возьмем h = h/2.
        # Вычислим два локальных интеграла обеих половин отрезка и сложим их
        result2 = (point1 + 2 * point3 + point2) * h / 4

        # проверка точности вычислений
        if abs(result2 - result1) > e:
            h /= 2
            stepsTrap -= 1
        else:
            result += result1
            cur += h
            h *= 2

    return result, stepsTrap

def autoSimpson(start, end, e, func):
    """
    Вычисление интеграла методом Симпсона
    с автоматическим выбором числа шагов
    """
    result = 0
    cur = start
    h = 1
    stepsSimpson = 0

    # пока не дошли до конца отрезка
    while cur < end:
        stepsSimpson += 1
        if cur + h > end:
            h = end - cur

        result1 = result2 = 0

        # вычисляем значения функции в точках отрезка
        x = cur
        point1 = ne.evaluate(func)
        x = cur + h / 2
        point2 = ne.evaluate(func)
        x = cur + h
        point3 = ne.evaluate(func)
        x = cur + h / 4
        point4 = ne.evaluate(func)
        x = cur + h * 3 / 4
        point5 = ne.evaluate(func)

        # интеграл на отрезке x[i-1], x[i] по локальной формуле симпсона:
        result1 = (point1 + 4 * point2 + point3) * h / 6

        # складываем два локальных интеграла половин отрезка:
        result2 = (point1 + 4 * point4 + 2 * point2 + 4 * point5 + point3) * h / 12

        # проверяем точность вычислений
        if abs(result2 - result1) > e:
            h /= 2
            stepsSimpson -= 1
        else:
            result += result1
            cur += h
            h *= 2

    return result, stepsSimpson

def autoStep(start, end, e, func):
    """
    Вычисляем интеграл методами прямоугольников, трапеции и Симпсона
    с автоматически выбранным числом шагов
    """
    
    # метод средних прямоугольников
    rect, stepsRect = autoRect(start, end, e, func)
    # метод трапеции
    trap, stepsTrap = autoTrap(start, end, e, func)
    # метод симпсона
    simpson, stepsSimpson = autoSimpson(start, end, e, func)
    
    return rect, trap, simpson, stepsRect, stepsTrap, stepsSimpson
