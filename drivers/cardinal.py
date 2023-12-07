from ..localPP import LocalInterpolator
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline


N = 15
stencil_size = 4


def cardinal_vec(index):
    ret = np.zeros(N, dtype=float)
    ret[index] = 1.0
    return ret


xs = np.arange(N)
zs = np.linspace(xs[0], xs[-1], 2001)

plot_indices = [0, 1, 2, 3, 7]

fig, axes = plt.subplots(len(plot_indices), 1, figsize=(10, 2*len(plot_indices)))
for index, ax in zip(plot_indices, axes):
    fs = cardinal_vec(index)
    approx = LocalInterpolator(xs, fs, stencil_size=stencil_size)
    spline = CubicSpline(xs, fs)

    ax.plot(xs, fs, "k*")
    ax.plot(zs, spline(zs), "g.", markersize=2, label="Spline")
    ax.plot(zs, approx(zs), "b.", markersize=2, label="LocalPP")
    ax.legend()


plt.suptitle("Some Cardinal Basis Functions")

plt.savefig("images/cardinal_basis.png")
