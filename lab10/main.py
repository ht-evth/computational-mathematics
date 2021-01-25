from spline import interpolation, splineGetValue
import pylab
import random

FILENAME = 'input.txt'

def numberToStr(number):
    tmp = str(round(number, 2))
    while len(tmp) < 9:
        tmp += ' '
    return tmp

def printTable(listX, listY, listT):
    """
    Печать таблицы точек
    """
    print('\tt' + ' ' * 8 + 'X' + ' ' * 8 + 'Y')
    for i in range(len(listX)):
        print('\t{}{}{}'
              .format(numberToStr(listT[i]), numberToStr(listX[i]), numberToStr(listY[i])))
    print('\n')

def loadData(filename: str):
    """ Считать входные данные из файла """
    listT = []
    listX = []
    listY = []
    with open(filename, "r") as file:
        eps = float(file.readline())
        amount = int(file.readline())
        i = 0
        for line in file:
            listT.append(i)
            listX.append(float(line.split()[0]))
            listY.append(float(line.split()[1]))
            i += 1

    return listT, listX, listY, eps, amount

def simpson(splineX, splineY, start, end, eps):
    """
    Вычисление интеграла методом Симпсона
    с автоматическим выбором шага
    """

    result = 0
    cur = start
    h = 1

    # пока не дошли до конца отрезка
    while cur < end:
        if cur + h > end:
            h = end - cur

        # интеграл на отрезке x[i-1], x[i] по локальной формуле симпсона:
        result1 = (calcArea(cur, splineX, splineY) + 4 * calcArea(cur + h / 2, splineX, splineY)
                   + calcArea(cur + h, splineX, splineY)) * h / 6

        # складываем два локальных интеграла половин отрезка:
        result2 = (calcArea(cur, splineX, splineY) + 4 * calcArea(cur + h / 4, splineX, splineY)
                   + 2 * calcArea(cur + h / 2, splineX, splineY) + 4 * calcArea(cur + 3 * h / 4, splineX, splineY) +
                   calcArea(cur + h, splineX, splineY)) * h / 12

        if abs(result1 - result2) > eps:
            h /= 2
        else:
            result += result1
            cur += h
            h *= 2

    return abs(result)

def calcArea(t, splineX, splineY):
    """
    Вычисление площади для области, которая ограничена кривой
    """
    return splineGetValue(splineY, t) * getFirst(splineX, t)

def getFirst(splines, x):
    """
    Вычисление 1 производной
    """
    # Если значение х лежит левее крайнего сплайна слева
    if x <= splines[0][0]:
        choice = splines[0]    # выбираем этот сплайн

    # Если значение x лежит правее крайнего сплайна справа
    elif x >= splines[-1][0]:
        choice = splines[-1]   # выбираем этот сплайн

    # значение х находится внутри
    # выбор сплайна к которому принадлежит точка х
    else:

        min = 0
        max = len(splines) - 1
        while min + 1 < max:
            middle = (min + max) // 2
            if x <= splines[middle][0]:
                max = middle
            else:
                min = middle
        choice = splines[max]

    # вычисление производной в заданной точке
    result = choice[2] + choice[3] * (x - choice[0]) + 0.5 * choice[4] * (x - choice[0]) ** 2

    return result


def monteCarlo(listX, listY, amount):
    """
    Метод Монте-Карло
    """
    count = 0

    # определяем минимальные/макимальные координаты
    xMin, xMax = min(listX), max(listX)
    yMin, yMax = min(listY), max(listY)

    # инициализация массива случайных точек
    createdPoints = []

    for i in range(amount):
        # генерация координат случайной точки
        x, y = random.uniform(xMin, xMax), random.uniform(yMin, yMax)

        # проверка: Внутри точка?
        if isPointInside(x, y, listX, listY):
            count += 1
            createdPoints.append((x, y, True))
        else:
            createdPoints.append((x, y, False))

    j = (abs((xMax - xMin) * (yMax - yMin)))

    # вычислить и вернуть площадь и созданные точки
    return j * count / amount, createdPoints


def isPointInside(x, y, listX, listY):
    """ находится ли точка внутри?"""

    result = False

    j = len(listX) - 1
    for i in range(len(listX)):
        # если координата y находится внутри
        # и не выходит за пределы по х
        if ((listY[i] < y <= listY[j]) or (listY[j] < y <= listY[i])) and (
                listX[i] + (y - listY[i]) / (listY[j] - listY[i]) * (listX[j] - listX[i])) < x:
            result = not result
        j = i
    return result






def main():
    integral_simpson = 0
    integral_monte_karlo = 0

    # Чтение и печать данных из файла
    listT, listX, listY, eps, amount = loadData(FILENAME)
    printTable(listX, listY, listT)

    # создаём список параметра t с бОльшей
    # точностью для более точного построения слпайнов
    t = []
    tmp = 0
    while tmp <= listT[-1]:
        t.append(tmp)
        tmp += 0.001


    # Интерполирование сплайнами для x = x(t) и y = y(t)
    splinesX = interpolation(listT, listX)
    splinesY = interpolation(listT, listY)
    valuesX = [splineGetValue(splinesX, x) for x in t]
    valuesY = [splineGetValue(splinesY, y) for y in t]

    # Симпсон
    print('Симпсон: ', simpson(splinesX, splinesY, listT[0], listT[-1], eps))

    # Монте-Карло
    resultMonteCarlo, points = monteCarlo(valuesX, valuesY, amount)
    print('Монте-Карло ({}): {}'.format(amount, resultMonteCarlo))

    # рисуем точки
    for i, point in enumerate(points):
        # для быстрой отрисовки введём ограничение в 1500 точек
        if i < 1500:
            # Если точка внутри, рисуем её голубым
            if point[2] is True:
                pylab.scatter(point[0], point[1], s=3, c="blue")
            else:
            # иначе, чёрным
                pylab.scatter(point[0], point[1], s=3, c="black")
        else:
            break

    # Рисование графика позже, чтобы его было видно поверх точек
    pylab.plot(valuesX, valuesY, c='orange')
    pylab.grid(True)
    pylab.show()


if __name__ == '__main__':
    main()
