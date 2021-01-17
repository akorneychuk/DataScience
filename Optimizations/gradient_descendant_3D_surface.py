import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as clr
from celluloid import Camera
from mpl_toolkits.mplot3d import Axes3D # <--- This is important for 3d plotting
from colorsys import hls_to_rgb


def z(x, y):
    z = np.sin(np.pi * x) * np.sin(np.pi * y)
    return z


def colorFader(c1,c2,mix=0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)


def rgb2hex(triplet):
    r = int(triplet[0] * 255)
    g = int(triplet[1] * 255)
    b = int(triplet[2] * 255)
    return '#%02x%02x%02x' % (r, g, b)


def rainbow_color_stops(n=10, end=1 / 3):
    return [hls_to_rgb(end * i / (n - 1), 0.5, 1) for i in range(n)]


if __name__ == '__main__':
    c1 = '#c800ff'  # violette
    c2 = '#00fffb'  # blue
    n = 100 #approximate iteration count untill reaches minimum

    fig = plt.figure()
    camera = Camera(fig)

    ax = fig.add_subplot(221, projection="3d")
    X, Y = np.mgrid[-1:1:30j, -1:1:30j]
    Z = np.sin(np.pi * X) * np.sin(np.pi * Y)

    x0s_y0s_plot = plt.subplot(222)
    x0s_i0s_plot = plt.subplot(223)
    y0s_i0s_plot = plt.subplot(224)

    x0s_y0s_plot.set(xlabel='X', ylabel='Y')
    x0s_y0s_plot.set_title('X/Y Dependency')
    x0s_i0s_plot.set(xlabel='X', ylabel='Z')
    x0s_i0s_plot.set_title('X/Z Dependency')
    y0s_i0s_plot.set(xlabel='Y', ylabel='Z')
    y0s_i0s_plot.set_title('Y/Z Dependency')

    plt.tight_layout()

    for counter_x in range(len(X[0])):
        for counter_y in range(len(Y[0])):
            _x = X[counter_x][0]
            _y = Y[0][counter_y]
            _z = np.sin(np.pi * _x) * np.sin(np.pi * _y)

    # x0 = np.array([0.5])
    # y0 = np.array([0.45])
    # x0 = np.array([-0.75])
    # y0 = np.array([-0.25])
    x0 = np.array([-0.3])
    y0 = np.array([-0.7])

    z0 = z(x0, y0)

    size = [3]
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

        color = colorFader(c1, c2, i / n)

        ax.plot_surface(X, Y, Z, cmap="autumn_r", rstride=1, alpha=0.1, antialiased=False)
        ax.scatter(x0_, y0_, z0_, s=size, marker='o', c=color)
        x0s_y0s_plot.plot(x0s, y0s, c="#db78ff")
        x0s_i0s_plot.plot(x0s, z0s, c="#db78ff")
        y0s_i0s_plot.plot(y0s, z0s, c="#db78ff")
        camera.snap()


    def draw_together():
        ax.scatter(x0s, y0s, z0s, s=size, marker='o', c="#db78ff")
        ax.scatter(x0_, y0_, z0_, s=20, marker='o', c="#00ff00")
        ax.plot_surface(X, Y, Z, cmap="autumn_r", rstride=1, alpha=0.1, antialiased=False)
        camera.snap()

    for j in range(0, 20):
        x0s_y0s_plot.plot(x0s, y0s, c="#db78ff")
        x0s_i0s_plot.plot(x0s, z0s, c="#db78ff")
        y0s_i0s_plot.plot(y0s, z0s, c="#db78ff")
        draw_together()

    anim = camera.animate()
    anim.save('../video_outputs/gradient_descendant_3D_surface_3.mp4')

    plt.show()



