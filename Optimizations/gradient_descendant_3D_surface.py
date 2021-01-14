from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from celluloid import Camera

def z(x, y):
    z = np.sin(np.pi * x) * np.sin(np.pi * y)
    return z


if __name__ == '__main__':
    fig = plt.figure()
    camera = Camera(fig)

    ax = fig.add_subplot(221, projection="3d")
    X, Y = np.mgrid[-1:1:30j, -1:1:30j]
    Z = np.sin(np.pi * X) * np.sin(np.pi * Y)

    x0s_y0s_plot = plt.subplot(222)
    x0s_i0s_plot = plt.subplot(223)
    y0s_i0s_plot = plt.subplot(224)

    for counter_x in range(len(X[0])):
        for counter_y in range(len(Y[0])):
            _x = X[counter_x][0]
            _y = Y[0][counter_y]
            _z = np.sin(np.pi * _x) * np.sin(np.pi * _y)

    x0 = np.array([0.5])
    y0 = np.array([0.45])
    # x0 = np.array([-0.75])
    # y0 = np.array([-0.25])
    # x0 = np.array([-0.5])
    # y0 = np.array([-0.0])

    z0 = z(x0, y0)

    size = [5]
    step = 0.01

    dz_dxs = []
    dz_dys = []
    x0s = []
    y0s = []
    z0s = []
    i_s = []

    ax.plot_surface(X, Y, Z, cmap="autumn_r", rstride=1, alpha=0.1, antialiased=False)
    camera.snap()

    for i in range(100):
        z0 = z(x0, y0)
        dz_dx = (z(x0 + step, y0) - z0) / step
        dz_dy = (z(x0, y0 + step) - z0) / step

        x0_ = x0 - step * dz_dx
        y0_ = y0 - step * dz_dy

        z0_ = z(x0_, y0_)
        delta = abs(z0 - z0_)
        if (delta < step / 10):
            break

        x0 = x0_
        y0 = y0_

        dz_dxs.append(dz_dx)
        x0s.append(x0[0])

        dz_dys.append(dz_dy)
        y0s.append(y0[0])

        i_s.append(i)
        z0s.append(z0_)

        ax.scatter(x0_, y0_, z0_, s=size, marker='o')

        x0s_y0s_plot.plot(x0s, y0s)
        x0s_i0s_plot.plot(x0s, z0s)
        y0s_i0s_plot.plot(y0s, z0s)

        camera.snap()

    x0s_y0s_plot.plot(x0s, y0s)
    x0s_i0s_plot.plot(x0s, z0s)
    y0s_i0s_plot.plot(y0s, z0s)

    ax.scatter(x0s, y0s, z0s, s=size, marker='o')

    ax.plot_surface(X, Y, Z, cmap="autumn_r", rstride=1, alpha=0.1, antialiased=False)
    camera.snap()

    anim = camera.animate()
    anim.save('scatter_3.mp4')

    plt.show()



