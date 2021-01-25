import sympy
import integral

FILENAME_FUNC = 'func1.txt'
FILENAME_START_END_STEP = 'ses1.txt'

def loadFuncFromFile(filename):
    """ считать функцию в виде строки из файла """
    try:
        file = open(filename)
        res = file.readline()
        file.close
        return res
    except FileNotFoundError:
        print('FileNotFoundError: ' + filename)
        return None

def loadStartEndStep(filename):
    """ загрузить отрезок и шаг из файла """
    try:
        f = open(filename)
        line = f.readline()
        f.close()
        res = line.split(' ')
        return float(res[0]), float(res[1]), float(res[2])
    except:
        print('Error')
        return None, None, None

def finput(msg):
    while True:
        try:
            num = float(input(msg))
            break
        except ValueError:
            pass
    return num

def main():
    # считываем функцию из файла
    # и старт, стоп, шаг из файла
    func = loadFuncFromFile(FILENAME_FUNC)
    start, end, step = loadStartEndStep(FILENAME_START_END_STEP)

    # выводим функцию и отрезок
    print('Заданная функция: f(x) = {} на отрезке [ {} ; {} ]'.format(func, start, end))
    print('Точное значение = ', sympy.integrate(func, ('x', start, end)))

    # считываем кол-во шагов
   #print('\n*Постоянный шаг интегрирования.')
   #step = finput('Введите кол-во шагов: ')
   ## вычисляем интегралы с постоянным шагом
   #rect, trap, simpson = integral.constStep(start, end, step, func)

   ## выводим результаты
   #print('\nМетод средних прямоугольников: \t',rect)
   #print('Метод трапеции: \t\t\t\t', trap)
   #print('Метод Симпсона: \t\t\t\t', simpson)

    print('\n*Автоматический шаг интегрирования.')
    # запрос ввода точности
    e = finput('Точность: ')
    # вычисление интегралов с заданной точностью
    rectAutoStep, trapAutoStep, simpsonAutoStep, stepsRect, stepsTrap, stepsSimpson = integral.autoStep(start, end, e, func)
    print('\nМетод средних прямоугольников: {}\nКол-во шагов: {}'.format(rectAutoStep, stepsRect))
    print('\nМетод трапеции: {}\nКол-во шагов = {}'.format(trapAutoStep, stepsTrap))
    print('\nМетод Симпсона: {}\nКол-во шагов = {}'.format(simpsonAutoStep, stepsSimpson))

if __name__ == "__main__":
    main()