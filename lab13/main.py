import numpy as np
import math
import pylab
import rk


def main():

    EXAMPLE = 3

    h = 0.001
    eps = 0.001
    p = 1
    a, b, = 0, 1

    dudt = lambda t, u: dfdx(t) + p * (u - f(t))

    if EXAMPLE == 1:

        f = lambda x: 2.2 * (x ** 3) + 3 * (x ** 2) - 4 * x
        solveFunc = [f]
        dfdx = lambda x: 6.6 * (x ** 2) + 6 * x - 4
        funcs = [dudt]

    elif EXAMPLE == 2:
        f = lambda x: math.cos(x) * x
        solveFunc = [f]
        dfdx = lambda x: - x * math.sin(x) + math.cos(x)
        funcs = [dudt]

    else:
        example3()
        return

    # начальные данные
    init = np.array([0])

    # с постоянным шагом
    X, Y = rk.RungeKutta(funcs, init, a, b, h)
    err = rk.calculateError(X, Y, solveFunc)

    print('Норма гл. погрешности с постоянным шагом {}: {}'.format(h, err))
    pylab.plot(X, Y, 'k--', label='Постоянный шаг = {}'.format(h))


    # с автоматическим шагом
    X, Y = rk.autoStep(funcs, init, a, b, eps)
    err = rk.calculateError(X, Y, solveFunc)

    print('Норма гл. погрешности с переменным шагом ({}): {}'.format(eps, err))
    pylab.plot(X, Y, 'c--', label='Переменный шаг, точность = {}'.format(eps))

    listX = np.linspace(a, b, 1000)
    listY = [f(x) for x in listX]
    pylab.plot(listX, listY, 'orange', label='f(x)')


    pylab.legend()
    pylab.show()

def example3():
    dudt = lambda t, u: (-30.0) * u

    funcs = [dudt]
    X, Y = rk.RungeKutta(funcs, np.array([1]), 0, 1, 1/10)
    pylab.plot(X, Y, 'green', label='10 шагов')

    X, Y = rk.RungeKutta(funcs, np.array([1]), 0, 1, 1/11)
    pylab.plot(X, Y, 'orange', label='11 шагов')

    pylab.legend()
    pylab.show()

if __name__ == '__main__':
    main()
