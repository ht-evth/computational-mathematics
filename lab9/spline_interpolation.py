class Spline:
    """
    Структура, описывающая сплайн на сегменте, где

    a, b, c, d - коэфы многочлена

    x - точка
    """
    def __init__(self, a, b, c, d, x):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.x = x

    def print(self):
        print('a = {}, b = {}, c = {}, d = {}, x = {}'.format(self.a, self.b, self.c, self.d, self.x))

def build_spline(x, y, n):
    """
    Построение сплайна

    Args:
        x - узлы сетки, должны быть упорядочены по возрастанию, кратные узлы запрещены
        y - значения функции в узлах сетки
        n - количество узлов сетки

    Return:
        список сплайнов
    """

    # инициализируем список сплайнов
    splines = [Spline(0, 0, 0, 0, 0) for unused_i in range(0, n)]
    for i in range(0, n):
        splines[i].x = x[i]
        splines[i].a = y[i]
    
    # первый и последний коэф C = 0
    splines[0].c = splines[n - 1].c = 0.0
    
    # решение СЛАУ относительно коэффициентов сплайнов c[i] методом прогонки для трехдиагональных матриц
    # прямой ход метода прогонки
    alpha = [0.0 for unused_i in range(0, n - 1)]
    beta  = [0.0 for unused_i in range(0, n - 1)]
 
    for i in range(1, n - 1):
        hi  = x[i] - x[i - 1]
        hi1 = x[i + 1] - x[i]
        A = hi
        C = 2.0 * (hi + hi1)
        B = hi1
        F = 6.0 * ((y[i + 1] - y[i]) / hi1 - (y[i] - y[i - 1]) / hi)
        z = (A * alpha[i - 1] + C)
        alpha[i] = -B / z
        beta[i] = (F - A * beta[i - 1]) / z
    
    # обратный ход метода прогонки
    for i in range(n - 2, 0, -1):
        splines[i].c = alpha[i] * splines[i + 1].c + beta[i]
    
    # находим значения b[i] и d[i]
    for i in range(n - 1, 0, -1):
        hi = x[i] - x[i - 1]
        splines[i].d = (splines[i].c - splines[i - 1].c) / hi
        splines[i].b = hi * (2.0 * splines[i].c + splines[i - 1].c) / 6.0 + (y[i] - y[i - 1]) / hi

    # возвращаем список сплайнов
    return splines
 
def spline_interpolation(splines, x):
    """
    Интерполяция сплайнами в заданной точке x

    Args:
        splines - список сплайнов
        x - заданная точка x

    Return:
        None - если сплайны не заданы, иначе
        f(x) - значение в заданной точке x
    """

    # если сплайны не заданы - возвращаем None
    if not splines:
        return None 
    
    n = len(splines)
    s = Spline(0, 0, 0, 0, 0)

    # если x меньше точки сетки x[0] - пользуемся первым сплайном
    # если x больше точки сетки x[n - 1] - пользуемся последним сплайном
    # иначе x лежит между граничными точками сетки - ищем нужный сплайн
    if x <= splines[0].x: 
        s = splines[0]
    elif x >= splines[n - 1].x: 
        s = splines[n - 1]
    else: 
        i = 0
        j = n - 1
        while i + 1 < j:
            k = i + (j - i) // 2
            if x <= splines[k].x:
                j = k
            else:
                i = k
        s = splines[j]
    
    
    # вычисляем значение сплайна в заданной точке и возвращаем его
    dx = x - s.x
    return s.a + (s.b + (s.c / 2.0 + s.d * dx / 6.0) * dx) * dx

def spline_interpolation_1st_der(splines, x):
    """
    Интерполяция сплайном в заданной точке x
    первой производной

    Args:
        splines - список отрезков сплайна
        x - заданная точка x

    Return:
        None - если отрезки сплайна не заданы, иначе
        f'(x) - значение первой производной в заданной точке x
    """

    # если отрезки сплайна не заданы - возвращаем None
    if not splines:
        return None 
    
    n = len(splines)
    s = Spline(0, 0, 0, 0, 0)

    # если x меньше точки сетки x[0] - пользуемся первым отрезком сплайна
    # если x больше точки сетки x[n - 1] - пользуемся последним отрезком сплайна
    # иначе x лежит между граничными точками сетки - ищем нужный отрезок
    if x <= splines[0].x: 
        s = splines[0]
    elif x >= splines[n - 1].x: 
        s = splines[n - 1]
    else: 
        i = 0
        j = n - 1
        while i + 1 < j:
            k = i + (j - i) // 2
            if x <= splines[k].x:
                j = k
            else:
                i = k
        s = splines[j]
        
    # вычисляем значение сплайна в заданной точке и возвращаем его
    dx = x - s.x
    return s.b + (s.c + s.d * dx / 2.0) * dx