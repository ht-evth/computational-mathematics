import numpy as np

def safe_input_int(string_):
    while True:
        try:
            num = int(input(string_))
            break
        except ValueError:
            pass
    return num

def safe_input_float(string_):
    while True:
        try:
            num = float(input(string_))
            break
        except ValueError:
            pass
    return num

def display_menu(options):
    for i in range(len(options)):
        print("{:d}. {:s}".format(i + 1, options[i]))

    choice = 0
    while not(np.any(choice == np.arange(len(options)) + 1)):
        choice = safe_input_int("Choose a menu item: ")

    return choice

def get_float_num(filename):
    f = open(filename)
    res = float(f.read())
    f.close()
    return res

def read_func_from_file(filename):
    try:
        f = open(filename)
        res = f.readline()
        f.close
        return res
    except FileNotFoundError:
        print('FileNotFoundError: ' + filename)
        return None
    
def read_ses_from_file(filename):
    try:
        f = open(filename)
        line = f.readline()
        f.close()
        res = line.split(' ')
        return float(res[0]), float(res[1]), float(res[2])
    except:
        print('Error')
        return None, None, None

def print_table_ders(x, y, der1, der2, der3):
    n = len(x)

    print('x\t\t|\tf(x)\t\t|\tf\'(x)\t\t|\tf\'\'(x)\t\t|\tf\'\'\'(x)')
    for i in range(n):
        print('{:.6f}\t|\t{:.6f}\t|\t{:.6f}\t|\t{:.6f}\t|\t{:.6f}'.format(x[i], y[i], der1[i], der2[i], der3[i]))

    print('')


def print_table_ders_(x, y, der1, der2, der3, t_d1, t_d2, t_d3):
    n = len(x)

    print('x\t\t|\tf(x)\t\t|\tf\'(x)\t\t\t|\tf\'\'(x)\t\t\t|\tf\'\'\'(x)')
    for i in range(n):
        print('{:.6f}\t|\t{:.6f}\t|\t{:.6f} ({:.6f})\t|\t{:.6f} ({:.6f})\t|\t{:.6f} ({:.6f})'.format(x[i], y[i], der1[i], der1[i] - t_d1[i], der2[i], der2[i] - t_d2[i], der3[i], der3[i] - t_d3[i]))

    print('')

def read_func_with_derivates_from_file(filename):
    try:
        res = []
        f = open(filename)
        lines = f.readlines()
        for line in lines:
            res.append(line.replace('\n', ''))
        f.close
        return res[0], res[1], res[2], res[3]
    except:
        print('Error: ' + filename)
        return None, None, None, None

def print_t_x_y(t, x, y):

    n = len(t)

    print('t\t\t|\tx\t\t|\ty')
    for i in range(n):
        print('{:.10f}\t|\t{:.10f}\t|\t{:.10f}'.format(t[i], x[i], y[i]))
    
