import numpy as np
import sympy

NUMBER = 1  # для печати таблиц. При значении 1 - печатается каждое 1 значение.

FUNC_FILENAME = 'func.txt'
OTHER_FILENAME = 'other.txt'

def loadData():
    """
    Прочитать входные данные из файла
    """
    with open(FUNC_FILENAME, 'r') as file:
        func = file.readline().replace('\n', '')            # прочесть функцию из файла
        startStopStep = file.readline().replace('\n', '').split()
        start = float(startStopStep[0])
        stop = float(startStopStep[1])
        step = float(startStopStep[2])

    with open(OTHER_FILENAME, 'r') as file:
        noiseDelta = float(file.read())
    return func, start, stop, step, noiseDelta



def calculateValue(function: str, x):
    """
    Вычислить значение функции в заданной точке.

    Функция задана в виде строки с аргументом "х"
    """
    return eval(function.replace('x', str(x)))

def calculateFirst(u_plus_1, u_minus_1, h):
    """
    Вычислить 1 производную в точке с номером i
    """
    result = (u_plus_1 - u_minus_1) / (2 * h)

    return result


def calculateSecond(u_minus_1, u_i, u_plus_1, h):
    """
    Вычислить 2 производную в точке с номером i
    """
    result = (u_minus_1 - (2 * u_i) + u_plus_1) / (h * h)

    return result


def calculateThird(u_plus_2, u_plus_1, u_minus_1, u_minus_2,  h):
    """
    Вычислить 3 производную в точке с номером i
    """
    result = (u_plus_2 - (2 * u_plus_1) + (2 * u_minus_1) - u_minus_2) / (2 * h * h * h)

    return result

def calculateDerivatives(indexes, listY, step):
    """ Вычисление производных"""

    # первая производная
    first = []
    for i in indexes:
        first.append(calculateFirst(listY[i+1], listY[i-1], step))

    # вторая производная
    second = []
    for i in indexes:
        second.append(calculateSecond(listY[i-1], listY[i], listY[i+1], step))

    # третья производная
    third = []
    for i in indexes:
        third.append(calculateThird(listY[i+2], listY[i+1], listY[i-1], listY[i-2], step))

    return first, second, third

def ExactCalculate(someFunc: str, listX):
    """ Точное вычисление f(x) и её производных """
    arg = sympy.symbols('x')                    # задать аргумент - х

    # подготовка функции для вычислений
    originalFunc = sympy.sympify(someFunc)      # задать исходную функцию

    # с помощью метода diff вычисляется многочлен - производная функции в виде строки
    first = originalFunc.diff()     # взять 1 производную
    second = first.diff()           # взять 2 производную
    third = second.diff()           # взять 3 производную

    # сформировать лямбда выражения для каждого многочлена
    originalFunc = sympy.lambdify(arg, originalFunc, 'numpy')
    first = sympy.lambdify(arg, first, 'numpy')
    second = sympy.lambdify(arg, second, 'numpy')
    third = sympy.lambdify(arg, third, 'numpy')

    listX = np.array(listX)

    # вычислить и вернуть значения для: исх функ, 1 произв, 2 произв, 3 произв
    return  originalFunc(listX), first(listX), second(listX), third(listX)


def createAndCalculateWithNoises(indexes, noiseDelta, listY, step):
    """ Создать шумы и вычислить производные """

    # добавить шумы
    noisesY = [ curY + np.random.uniform(-noiseDelta, noiseDelta) for curY in listY]

    # вычислить производные
    first, second, third = calculateDerivatives(indexes, noisesY, step)

    return noisesY, first, second, third


def floatToStr(x):
    """ Перевести число в строку и добавить отступ """
    newStr = '{:.8f}'.format(x).rstrip('0.')
    if newStr == '' or newStr == '-':
        newStr = '0'

    if len(newStr) >= 13:
        newStr = newStr[:12]

    while (len(newStr) < 12):
        newStr += ' '

    return newStr

def printResults(listX, listY, first, second, third):
    """ Печать аргументов, значений функции и её производных"""



    allData = zip([i for i in range(len(listX))], listX, listY, first, second, third)

    print("x" + ' ' * 15 + "f(x)" + ' ' * 12 + "f'(x)" + ' ' * 11 + "f''(x)" + ' ' * 10 + "f'''(x)", end = '\n')

    for i, x, y, first, second, third in allData:
        if i % NUMBER == 0:
            x = floatToStr(x)
            y = floatToStr(y)
            first = floatToStr(first)
            second = floatToStr(second)
            third = floatToStr(third)

            print('{}\t{}\t{}\t{}\t{}'.format(x, y, first, second, third))


def printNevyazka(listX, first, second, third, first2, second2, third2):
    """ пеечать невязки для производных """
    temp1 = abs(first - first2)
    temp2 = abs(second - second2)
    temp3 = abs(third - third2)
    deltaList = zip([i for i in range(len(listX))], listX, temp1, temp2, temp3)

    print('\n\nНевязка')
    for i, x, f, s, t in deltaList:
        if i % NUMBER == 0:
            x = floatToStr(x)
            f = floatToStr(f)
            s = floatToStr(s)
            t = floatToStr(t)
            print('{}\t\t\t\t\t{}\t{}\t{}'.format(x, f, s, t))

def main():
    # загрущить входные данные
    function, start, stop, step, noiseDelta = loadData()

    # равномерно распределить список аргументов от start до stop
    exactX = np.linspace(start, stop, round(((stop - start) / step) + 1))

    # вычислить точные значения функции и её производных
    exactY, exactFirst, exactSecond, exactThird = ExactCalculate(function, exactX)

    #печать результатов
    print('\nТочные значения:')
    printResults(exactX, exactY, exactFirst, exactSecond, exactThird)

    # Создать список индексов, чтобы вывести на экран только входные данные
    # +1 - чтобы вошло крайнее значение, +2 - чтобы расширить список на 2
    # начать от 2 чтобы расширить список аргумента для поиска производных
    indexes = [i for i in range(2, round((stop-start)/step) + 1 + 2)]
    # равномерно распределить список аргументов
    listX = np.linspace(start - 2 * step, stop + 2 * step, round(((stop - start) / step) + 5))
    listXForPrint = [listX[i] for i in indexes]


    listY = []
    # вычислить значения функции
    for x in listX:
        listY.append(calculateValue(function, x))
    listYForPrint = [listY[i] for i in indexes]

    # вычислить производные
    first, second, third = calculateDerivatives(indexes, listY, step)

    # печать результатов на экран
    print('\n\nВычисленные значения:')
    printResults(listXForPrint, listYForPrint, first, second, third)

    printNevyazka(listXForPrint, first, second, third, exactFirst, exactSecond, exactThird)

    # добавить шумы и вычислить производные
    noiseY, noiseFirst, noiseSecond, noiseThird = createAndCalculateWithNoises(indexes, noiseDelta, listY, step)
    noiseYForPrint = [noiseY[i] for i in indexes]


    # печать на экран результатов
    print('\n\nШумы: ')
    printResults(listXForPrint, noiseYForPrint, noiseFirst, noiseSecond, noiseThird)

    printNevyazka(listXForPrint, noiseFirst, noiseSecond, noiseThird, exactFirst, exactSecond, exactThird)



if __name__ == '__main__':
    main()