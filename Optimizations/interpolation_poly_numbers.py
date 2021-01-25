import matplotlib.pyplot as plt
import numpy as np
import functools
from scipy.interpolate import interp1d


def approximation(poly_x, X_k, X_i):
    approx_res = (poly_x - X_k) / (X_i - X_k)

    return approx_res


def production(Xs, counter_1, poly_x):
    prod_res = 1
    for counter_2 in range(len(Xs)):
        if counter_1 == counter_2:
            continue

        X_k = Xs[counter_2]
        X_i = Xs[counter_1]
        oper_res = approximation(poly_x, X_k, X_i)
        prod_res = prod_res * oper_res

    return prod_res


def summation(Xs, Ys, poly_x):
    summ_res = 0
    for counter_1 in range(len(Ys)):
        prod_res = Ys[counter_1] * production(Xs, counter_1, poly_x)
        summ_res = summ_res + prod_res

    return summ_res


def polinom_n(Xs, Ys, poly_x):
    polinom_res = summation(Xs, Ys, poly_x)

    return polinom_res


if __name__ == '__main__':
    step = 10
    x_start = 0
    x_end = 1/2
    Xs = np.array([x_start, 1/5, x_end])
    # Xs = np.linspace(0, 1/2, num=100, endpoint=True)

    Ys = np.sin(np.pi * Xs)

    plt.plot(Xs, Ys, '-')

    for x_i in np.linspace(x_start, x_end, step):
        Y_calc = polinom_n(Xs, Ys, x_i)
        plt.plot(x_i, Y_calc, 'o')

    plt.show()

