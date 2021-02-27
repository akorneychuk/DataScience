import random as rand

import matplotlib.pyplot as plt

from Helpers.CameraHelper import RealCamera
from Optimizations.approximation_poly_numbers import approximate

if __name__ == '__main__':
    fig = plt.figure()
    camera = RealCamera(fig)

    iterations_count = [500, 1000, 5000]
    learning_rates = [0.1, 1, 0.01]
    polynom_paddings = [0, 1, 2]
    polynom_coefficients = [
        [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
        [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3],
        [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
    ]

    for i in range(10):
        next_i = rand.randint(0, 2)
        next_l = rand.randint(0, 2)
        next_p_p = rand.randint(0, 2)
        next_p_c = rand.randint(0, 2)

        iteration_count = iterations_count[next_i]
        learning_rate = learning_rates[next_l]
        polynom_padding = polynom_paddings[next_p_p]
        polynom_coefficient = polynom_coefficients[next_p_c]

        file_name = "approx_poly_num_opt__" + str(next_i) + "-" + str(next_l) + "-" + str(next_p_p) + "-" + str(next_p_c)
        approximate(camera, iteration_count, learning_rate, polynom_coefficient, polynom_padding, file_name)
        print("Ready: " + file_name)
