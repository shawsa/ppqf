from itertools import pairwise
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import Polynomial
from scipy.interpolate import PPoly


class LocalInterpolator(PPoly):
    def __init__(
        self,
        nodes: np.ndarray[float],
        fs: np.ndarray[float],
        stencil_size: int = 4,
    ):
        self.nodes = nodes
        self.fs = fs
        self.stencil_size = stencil_size
        self.interpolate()

    def closest_nodes(self, z: float, k: int) -> list[int]:
        """Return list of indices of k closest nodes to z."""
        temp = [(index, abs(x - z)) for index, x in enumerate(self.nodes)]
        temp.sort(key=lambda tup: tup[1])
        return [tup[0] for tup in temp[: k]]

    def interpolate(self):
        coeffs = []
        for x1, x2 in pairwise(self.nodes):
            center = (x1 + x2) / 2
            stencil_indices = self.closest_nodes(center, self.stencil_size)
            poly = Polynomial.fit(
                self.nodes[stencil_indices] - x1,
                self.fs[stencil_indices],
                deg=self.stencil_size - 1,
                domain=(0, x2-x1),
                window=(0, x2-x1),
            )
            coeffs.append(poly.coef[::-1])
        coeffs = np.array(coeffs)
        super(LocalInterpolator, self).__init__(coeffs.T, self.nodes)


if __name__ == "__main__":
    from scipy.interpolate import CubicSpline
    import sympy as sym
    interval = (-np.pi, np.pi)
    N = 11
    stencil_size = 4

    x_sym = sym.symbols("x")
    # f_sym = sym.sin(x_sym)
    f_sym = 1/(1 + x_sym**2)

    foo = sym.lambdify(x_sym, f_sym)
    dfoo = sym.lambdify(x_sym, f_sym.diff(x_sym))
    d2foo = sym.lambdify(x_sym, f_sym.diff(x_sym, 2))

    xs = np.linspace(*interval, N)
    fs = foo(xs)
    approx = LocalInterpolator(xs, fs, stencil_size=stencil_size)
    spline = CubicSpline(xs, fs)

    zs = np.linspace(*interval, 2001)
    fig, axes = plt.subplots(3, 1, figsize=(10, 10))
    axes[0].set_title("Function")
    axes[0].plot(zs, foo(zs), 'b-', label="True")
    axes[0].plot(xs, fs, 'bo')
    axes[0].plot(zs, approx(zs), 'g--', label="Approx")
    axes[0].plot(zs, spline(zs), 'r--', label="Spline")
    axes[0].legend()

    axes[1].set_title("Derivative")
    axes[1].plot(zs, dfoo(zs), 'b-', label="True")
    axes[1].plot(zs, approx.derivative()(zs), 'g--', label="Approx")
    axes[1].plot(zs, spline.derivative()(zs), 'r--', label="Spline")

    axes[2].set_title("2nd derivative")
    axes[2].plot(zs, d2foo(zs), 'b-', label="True")
    axes[2].plot(zs, approx.derivative(2)(zs), 'g--', label="Approx")
    axes[2].plot(zs, spline.derivative(2)(zs), 'r--', label="Spline")

    plt.figure("Error")
    plt.semilogy(zs, np.abs(foo(zs) - approx(zs)), "g-", label="Approx")
    plt.semilogy(zs, np.abs(foo(zs) - spline(zs)), 'r-', label="Spline")
    plt.legend()
