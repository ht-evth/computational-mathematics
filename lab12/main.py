from sympy import sympify, symbols
import newtone

EXAMPLE = 3

def finput(msg):
    while True:
        try:
            num = float(input(msg))
            break
        except ValueError:
            pass
    return num

def getInputData(len):
    print( '\nВведите начальный вектор X (для {} переменных): '.format(len), end='')
    vec = list(map(float, input().split()))[0:len]
    eps = finput('Введите точность: ')
    return vec, eps


def main():

    if EXAMPLE == 1:
        funcs = ['(x1 ** 2) + (x2 ** 2) - 25',
                 '(x1 ** 3) - x2 + 2']
    elif EXAMPLE == 2:
        funcs = ['3 * x1 - sin(x2) - 1.4',
                 'cos(x1 + 0.5) - x2 -0.8']
    elif EXAMPLE == 3:
        funcs = ['x1 + 2 * x2 + x3 - 2',
                 '3 * x1 - x2 + 2 * x3 - 2',
                 '0 * x1 + x2 + x3 + 0']

    elif EXAMPLE == 4:
        funcs = ['(x1 ** 2) - x2 + 0',
                 'x1 + x2 + 1']

    # генерация списка уравнений системы
    # генерация имён переменных в системе
    functions = [sympify(func) for func in funcs]
    varNames = [symbols('x{}'.format(i+1)) for i in range(len(functions))]

    # печать системы на экран
    print('Система уравнений:')
    for func in functions:
        print(func)

    # диалог с запросом ввода входных данных
    startVecX, eps = getInputData(len(functions))


    x, iterations = newtone.method(functions, startVecX, eps, varNames)
    print('\nРешение: ', x)
    print('Итераций: ', iterations)

    check = newtone.calcFunc(varNames, functions, x)
    print('\nПроверка решения: {}'.format(check))


if __name__ == "__main__":
    main()