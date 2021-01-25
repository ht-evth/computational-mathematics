# Построение сплайна дефекта 1
def interpolation(listX, listY):

    # инициализация массива для сплайнов
    res = []
    for i in range(len(listX)):
        res.append([-1, 0, 0, 0, 0])
        res[i][0] = listX[i]  # задаём значение х

    # задаём коэф-т а
    for i in range(len(listX)):
        res[i][1] = listY[i]

    # c[0] = c[n-1] = 0
    res[0][3] = res[-1][3] = 0

    # метод прогонки для поиска ci
    alpha = [0 for i in range(len(listX) - 1)]
    beta = [0 for i in range(len(listX) - 1)]

    for i in range(1, len(listX) - 1):
        h_i = listX[i] - listX[i - 1]
        h_i_next = listX[i + 1] - listX[i]

        # приведение уравнения к виду, пригодному для решения методом прогонки
        A = h_i
        b = -(2 * (h_i + h_i_next))
        c = h_i_next
        d = 6 * ((listY[i + 1] - listY[i]) / h_i_next - (listY[i] - listY[i - 1])
                 / h_i)

        alpha[i] = c / (b - A * alpha[i - 1])
        beta[i] = (A * beta[i - 1] - d) / (b - A * alpha[i - 1])

    # вычисление c[i] обратной прогонкой
    for i in range(len(listX) - 2, 0, -1):
        res[i][3] = alpha[i] * res[i + 1][3] + beta[i]

    # поиск d[i] и b[i]
    for i in range(len(listX) - 1, 0, -1):
        h = listX[i] - listX[i - 1]
        res[i][4] = (res[i][3] - res[i - 1][3]) / h
        res[i][2] = (h / 2 * res[i][3]) - \
                    (h ** 2 / 6 * res[i][4]) + (listY[i] - listY[i - 1]) / h
    return res


# Вычисление приближенного значения в заданной точке
def splineGetValue(splines, x):
    n = len(splines)

    # значение x слева от минимального сплайна
    if x <= splines[0][0]:
        result = splines[0]    # выбираем этот сплайн

    # значение x справа от максимального сплайна
    elif x >= splines[n - 1][0]:
        result = splines[n - 1] # выбираем его

    # значение x внутри:
    else:
        min_c = 0
        max_c = n - 1
        while min_c + 1 < max_c:
            middle = (min_c + max_c) // 2
            if x <= splines[middle][0]:
                max_c = middle
            else:
                min_c = middle
        result = splines[max_c]


    # вычисляем значение сплайна
    return result[1] + (result[2] * (x - result[0])) + (result[3] / 2 * (x - result[0]) ** 2) + (result[4] / 6 * (x - result[0]) ** 3)
