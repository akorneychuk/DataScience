import matplotlib.pyplot as plt
import numpy as np
import torch as torch
from celluloid import Camera
from torch.autograd import Variable


def calc_A_B(Xs, Ys, camera, iteration_count):
    a = Variable(torch.FloatTensor([0.1]), requires_grad=True)
    b = Variable(torch.FloatTensor([0.1]), requires_grad=True)
    ys = Variable(torch.from_numpy(np.array(Ys)), requires_grad=False)
    xs = Variable(torch.from_numpy(np.array(Xs)), requires_grad=False)

    Y = lambda x: torch.add(torch.mul(a, x), b)

    extrapolatedXs = np.array([100, 2300])

    optimizer = torch.optim.Adadelta([a, b], lr=1)
    for i in range(0, iteration_count):
        optimizer.zero_grad()
        ys_ = Y(xs)
        loss = (ys - ys_).pow(2).sum() / len(ys)
        loss.backward()
        optimizer.step()

        a_i = a.detach().numpy()[0]
        b_i = b.detach().numpy()[0]

        y = lambda x: a_i * x + b_i
        extrapolatedYs = np.array(list(map(y, extrapolatedXs)))
        plt.plot(extrapolatedXs, extrapolatedYs, '--', c="#FFA557")
        plt.plot(Xs, Ys, 'o', c="#1F78B4")
        camera.snap()

    a = a.detach().numpy()[0]
    b = b.detach().numpy()[0]

    return a, b


if __name__ == '__main__':
    fig = plt.figure()
    camera = Camera(fig)

    Xs = [240, 400, 445, 500, 630, 800, 1000, 1080, 1250, 2000]
    Ys = [3, 7.5, 8.37, 11, 15, 18.5, 22, 22, 30, 55]

    plt.xlim(Xs[0] - 50, Xs[len(Xs)-1] + 50)
    plt.ylim(Ys[0] - 3, Ys[len(Ys)-1] + 3)

    plt.plot(Xs, Ys, 'o', c="#1F78B4")
    camera.snap()

    a, b = calc_A_B(Xs, Ys, camera, 75)

    anim = camera.animate()
    anim.save('../render_outputs/linear_approximation_regression.mp4')
    plt.show()