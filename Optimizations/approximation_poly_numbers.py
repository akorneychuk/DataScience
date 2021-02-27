import torch
import matplotlib.pyplot as plt
import numpy as np
from functools import reduce

from celluloid import Camera
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure

from Helpers.CameraHelper import RealCamera, ICamera, FakeCamera
from Optimizations.interpolation_poly_numbers import polinom_n
from torch.autograd import Variable


def produce_n_poly_func(n_poly_num, arr):
    variables = [Variable(torch.FloatTensor([arr[iter]]), requires_grad=True) for iter in range(n_poly_num)]
    y = lambda x: reduce(torch.add, [torch.mul(torch.pow(x, n_poly_num - iter), variables[iter]) for iter in range(n_poly_num)])

    return variables, y


def approximate(camera: ICamera, iterations_count, learning_rate, initial_coefficients, polinom_padding, filename):

    plt.style.use('seaborn-pastel')
    fig = plt.figure()
    ax = plt.axes(xlim=(0, 8), ylim=(-8, 8))
    line1, = ax.plot([], [], '*', c="green")
    # line2, = ax.plot([], [], 'o', c="cyan")
    # line3, = plt.plot([], [], '+', c="#FFA557")

    Xs = np.array([1, 2, 4, 7])
    Ys = np.array([2, 3, 1, 4])

    x_s = np.linspace(Xs[0], Xs[len(Xs) - 1], 50)
    y_s = np.array(list(map(lambda x: polinom_n(Xs, Ys, x), x_s)))

    plt.plot(x_s, y_s, '*', c="gray")
    plt.plot(Xs, Ys, 'o', c="cyan")
    # camera.snap()

    def init():
        # line1.set_data(x_s, y_s)
        line1.set_data([], [])
        return line1,
        # line2.set_data(x_s, y_s)
        # return line1, line2

    xs = Variable(torch.from_numpy(np.array(Xs)), requires_grad=False)
    ys = Variable(torch.from_numpy(np.array(Ys)), requires_grad=False)
    extrapolatedXs = Variable(torch.from_numpy(np.linspace(Xs[0] - 0.2, Xs[len(Xs) - 1] + 0.2, 50)), requires_grad=False)

    n_poly_number_order = len(Xs) + polinom_padding
    # global vars
    vars, Y = produce_n_poly_func(n_poly_number_order, initial_coefficients)
    optimizer = torch.optim.Adamax(vars, lr=learning_rate)

    losses_varses = []
    def animate(i):
        nonlocal vars

        if (i == iterations_count-1):
            sorted_loss_coefficients = sorted(losses_varses, key=lambda x: x[0])
            best_loss_coefficients = sorted_loss_coefficients[0]
            best_coefficients = best_loss_coefficients[1]
            vars, y = produce_n_poly_func(n_poly_number_order, best_coefficients)

            x__s = extrapolatedXs.detach().numpy()
            y__s = y(extrapolatedXs).detach().numpy()

            plt.plot(x_s, y_s, 'o', c="gray")
            plt.plot(Xs, Ys, 'o', c="cyan")
            # plt.plot(Xs, Ys, 'o', c="green")
            plt.savefig("../render_outputs/" + filename + ".png")
        else:
            optimizer.zero_grad()
            ys_ = Y(xs)
            loss = (ys - ys_).pow(2).sum() / len(ys)
            coefficients = [vars[iter].detach().item() for iter in range(len(vars))]
            losses_varses.append((loss, coefficients))
            loss.backward()
            optimizer.step()

            x__s = extrapolatedXs.detach().numpy()
            y__s = Y(extrapolatedXs).detach().numpy()

        line1.set_data(x__s, y__s)

        return line1,

    # for i in range(0, iterations_count):
    #     optimizer.zero_grad()
    #     ys_ = Y(xs)
    #     loss = (ys - ys_).pow(2).sum() / len(ys)
    #     loss.backward()
    #     optimizer.step()
    #
    #     x__s = extrapolatedXs.detach().numpy()
    #     y__s = Y(extrapolatedXs).detach().numpy()
    #
    #     plt.plot(x_s, y_s, '*', c="gray")
    #     plt.plot(Xs, Ys, 'o', c="cyan")
    #     plt.plot(x__s, y__s, '+', c="#FFA557")
    #     camera.snap()

    # plt.plot(x__s, y__s, '+', c="#FFA557")
    # camera.snap()
    # camera.save(filename)
    # plt.show()

    anim = FuncAnimation(fig, animate, init_func=init, frames=iterations_count, interval=1, blit=True)
    anim.save("../render_outputs/" + filename + ".gif", writer='imagemagick')


if __name__ == '__main__':
    fig = plt.figure()
    axes = plt.gca()
    axes.set_xlim([0, 8])
    axes.set_ylim([-10, 10])
    camera = RealCamera(fig)

    approximate(camera, 200, 1, [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], 1, "approx_poly_num")

