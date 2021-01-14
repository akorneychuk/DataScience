import matplotlib.pyplot as plt
import numpy as np
from celluloid import Camera
from mpl_toolkits.mplot3d import Axes3D # <--- This is important for 3d plotting


def z(x, y):
    res = np.sin(np.pi * x) * np.sin(np.pi * y)
    return res


if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    camera = Camera(fig)

    X, Y = np.mgrid[-1:1:30j, -1:1:30j]
    Z = z(X, Y)

    for counter_x in range(len(X[0])):
        for counter_y in range(len(Y[0])):
            _x = X[counter_x][0]
            _y = Y[0][counter_y]
            _z = np.sin(np.pi * _x) * np.sin(np.pi * _y)

    size = [1]

    x0s = []
    y0s = []
    z0s = []

    X_range = X[:, 0]
    Y_range = Y[0, :]

    combinations = []
    for i in range(100):
        n = 1
        X_rand_index = np.random.choice(X_range.shape[0], n, replace=False)
        Y_rand_index = np.random.choice(Y_range.shape[0], n, replace=False)

        X_I = X_range[X_rand_index]
        Y_I = Y_range[Y_rand_index]
        Z_I = z(X_I, Y_I)

        combinations.append((X_I, Y_I, Z_I))

        ax.plot_surface(X, Y, Z, cmap="autumn_r", rstride=1, alpha=0.1, antialiased=False)
        ax.scatter(*zip(*combinations), s=size, marker='o')
        camera.snap()

    sorted_combinations = sorted(combinations, key=lambda x: x[2])

    # Lowest point
    lowest_point = sorted_combinations[0]

    # Highest point
    highest_point = sorted_combinations[len(sorted_combinations)-1]

    ax.plot_surface(X, Y, Z, cmap="autumn_r", rstride=1, alpha=0.1, antialiased=False)
    ax.scatter(*zip(*combinations), s=size, marker='o')
    ax.scatter(lowest_point[0], lowest_point[1], lowest_point[2], s=30, marker='o', c="#00ff00")
    ax.scatter(highest_point[0], highest_point[1], highest_point[2], s=30, marker='o', c="#ff0000")

    camera.snap()

    anim = camera.animate()
    anim.save('random_search_3D_surface.mp4')

    plt.show()