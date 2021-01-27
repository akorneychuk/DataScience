import matplotlib.pyplot as plt
import numpy as np


def calc_A(Xs, Ys):
    n = len(Xs)
    sum_xy_prod = 0
    sum_x = 0
    sum_y = 0
    sum_x_2 = 0
    for i in range(0, n):
        x_i = Xs[i]
        y_i = Ys[i]
        prod1 = x_i * y_i
        sum_xy_prod = sum_xy_prod + prod1
        sum_x = sum_x + x_i
        sum_y = sum_y + y_i
        sum_x_2 = sum_x_2 + x_i ** 2

    a = (n * sum_xy_prod - sum_x * sum_y) / (n * sum_x_2 - sum_x ** 2)

    return a


def calc_B(Xs, Ys, a):
    n = len(Xs)
    sum_y = 0
    sum_x = 0

    for i in range(0, n):
        x_i = Xs[i]
        y_i = Ys[i]
        sum_y = sum_y + y_i
        sum_x = sum_x + x_i

    b =  (sum_y - a * sum_x) / n

    return b


if __name__ == '__main__':
    Xs = [240, 400, 445, 500, 630, 800, 1000, 1080, 1250, 2000]
    Ys = [3, 7.5, 8.37, 11, 15, 18.5, 22, 22, 30, 55]

    plt.plot(Xs, Ys, 'o')

    a = calc_A(Xs, Ys)
    b = calc_B(Xs, Ys, a)

    y = lambda x : a * x + b

    extrapolatedXs = np.array([100, 2300])
    extrapolatedYs = np.array(list(map(y, extrapolatedXs)))

    plt.plot(extrapolatedXs, extrapolatedYs, '--')

    plt.show()