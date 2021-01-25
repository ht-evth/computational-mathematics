from matplotlib import pyplot
from shootingMethod import method

def numberToStr(number):
    """ функция преобразования числа в строку для красивого вывода"""
    tmp = '{:.8f}'.format(number)
    while len(tmp) < 25:
        tmp += ' '

    return tmp

def main():

    # Заданные параметры

    N = 2
    R = 0.815
    n = 2

    a, b = 0, 1             # граничные значения
    eps = 0.000001          # заданная точность
    p0, p1 = 0.1, 0.8       # начальное приближение


    funcs = [
        lambda x, y, u: u,
        lambda x, y, u: N * u + N * R * (y ** n)
    ]

    def getFirst(y_a):
        """ по одному из значений y(a), u(a) возвращает оба """
        return y_a, N * (y_a - 1)

    def secondCondition(y_b, u_b):
        ''' левая часть уравнения fi2( y(b), u(b) ) = 0 '''
        return u_b


    # вычисляем
    X, Y = method(funcs, a, b, eps, p0, p1, getFirst, secondCondition)

    # печать результатов
    print('Начальные приближения для y(0): {} {}'.format(p0, p1))
    print('Заданная точность: ', eps)
    print('\n     z' + ' ' * 25 + 'y(z)' + ' ' * 21 + "y'(z)")

    allData = zip(X, Y.transpose()[0], Y.transpose()[1])
    # печать каждого 4 значения
    i = 0
    for x, y, y_1 in allData:
        if i % 4 == 0:
            print(numberToStr(x), numberToStr(y), numberToStr(y_1))
        i += 1

    # рисуем график
    pyplot.subplot(2, 1, 1)
    pyplot.plot(X, Y[:, 0], label='y(z)')
    pyplot.legend()

    pyplot.subplot(2, 1, 2)
    pyplot.plot(X, Y[:, 1], label="y'(z)", color='red')
    pyplot.legend()
    pyplot.show()


if __name__ == '__main__':
    main()