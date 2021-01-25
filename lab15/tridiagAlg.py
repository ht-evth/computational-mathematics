def tridiagMatrix(a, b, c, d):
    """
    Метод прогонки для трехдиагональной матрицы
    """

    n = len(a)

    alpha = [0 for i in range(n + 1)]
    beta = [0 for i in range(n + 1)]
    x = [0 for i in range(n)]

    # прямой ход
    alpha[1] = c[0] / b[0]
    beta[1] = -d[0] / b[0]

    for i in range(2, n + 1):
        alpha[i] = c[i-1] / (b[i-1] - a[i-1] * alpha[i-1])
        beta[i] = (a[i-1] * beta[i-1] - d[i-1]) / (b[i-1] - a[i-1] * alpha[i-1])

    # обратный ход
    x[n-1] = beta[n]

    for i in range(n-2, -1, -1):
        x[i] = alpha[i+1] * x[i+1] + beta[i+1]

    return x


def first(n, h, x, coefs, funcs):
    """
    Функция для вычисления коэффициентов для системы линейных
    уравнений по формулам аппроксимирующим первым порядком

    Args:
        n - число разбиений
        h - шаг
        x - узлы сетки
        coefs - коэффициенты F1, D1, E1, F2, D2, E2
        funcs - функции A(x), B(x), C(x)

    """

    A, B, C = funcs
    F1, D1, E1, F2, D2, E2 = coefs

    a = [0 for i in range(n+1)]
    b = [0 for i in range(n+1)]
    c = [0 for i in range(n+1)]
    d = [0 for i in range(n+1)]


    b[0] = -(F1 - D1 / h)
    c[0] = D1 / h
    d[0] = E1

    for i in range(1, n):
        a[i] = (1 / (h * h)) - (A(x[i]) / (2 * h))
        b[i] = -((-2/(h*h)) + B(x[i]))
        c[i] = (1 / (h * h)) + (A(x[i]) / (2 * h))
        d[i] = C(x[i])

    a[n] = -D2 / h
    b[n] = -(F2 + D2 / h)
    d[n] = E2

    return tridiagMatrix(a, b, c, d)


def second(n, h, x, segment, coefs, funcs):
    """
    Функция для вычисления коэффициентов для системы линейных
    уравнений по формулам аппроксимирующим вторым порядком

    Args:
        n - число разбиений
        h - шаг
        x - узлы сетки
        segment - отрезок [a, b]
        coefs - коэффициенты F1, D1, E1, F2, D2, E2
        funcs - функции A(x), B(x), C(x)

    """

    A, B, C = funcs
    F1, D1, E1, F2, D2, E2 = coefs
    start, end = segment

    a = [0 for i in range(n+1)]
    b = [0 for i in range(n+1)]
    c = [0 for i in range(n+1)]
    d = [0 for i in range(n+1)]

    b[0] = -F1 * h + D1 + D1 * (A(start) - B(start) * h) * (h/2)
    c[0] = A(start) * D1 * (h/2) + D1
    d[0] = E1 * h + C(start) * D1 * (h ** 2) / 2

    for i in range(1, n):
        a[i] = 1 - A(x[i]) * (h / 2)
        b[i] = 2 - B(x[i]) * (h ** 2)
        c[i] = 1 + A(x[i]) * (h / 2)
        d[i] = C(x[i]) * (h ** 2)

    a[n] = A(end) * D2 * (h/2) - D2
    b[n] = -F2 * h - D2 + D2 * (A(end) + B(end) * h) * (h/2)
    d[n] = E2 * h - C(end) * D2 * (h ** 2)/2

    return tridiagMatrix(a, b, c, d)

