from itertools import pairwise
import numpy as np
from numpy.polynomial.polynomial import Polynomial
from scipy.integrate import quadrature
from scipy.interpolate import CubicSpline

interval = (-1, 1)
N = 41
stencil_size = 4

nodes = np.linspace(*interval, N)
pieces = list(pairwise(nodes))


def cardinal_vec(N, index):
    ret = np.zeros(N, dtype=float)
    ret[index] = 1.0
    return ret


partition_weights = []
for piece in pieces:
    center = np.sum(piece) / 2
    temp = [(index, abs(center - x)) for index, x in enumerate(nodes)]
    temp.sort(key=lambda tup: tup[1])
    stencil_indices = [index for index, dist in temp[:stencil_size]]
    xs = nodes[stencil_indices]
    for local_index, global_index in enumerate(stencil_indices):
        fs = cardinal_vec(stencil_size, local_index)
        poly = Polynomial.fit(xs, fs, deg=len(xs) - 1).integ()
        w = poly(piece[-1]) - poly(piece[0])
        partition_weights.append((global_index, w))

weights = np.array(
    [sum(w for i, w in partition_weights if i == index) for index in range(len(nodes))]
)


def quad(foo):
    return weights @ foo(nodes)


def foo(x):
    return 1 / (1 + x**2)


exact = quadrature(foo, *interval, tol=1e-13)[0]
approx = quad(foo)
print((approx - exact) / exact)
h = (nodes[-1] - nodes[0]) / (N - 1)
print(weights / h)


spline_weights = np.array([
    CubicSpline(nodes, cardinal_vec(N, index)).integrate(*interval)
    for index in range(len(nodes))
])
print(spline_weights/h)
