from itertools import pairwise, takewhile
import numpy as np
from sympy import integrate, latex, Matrix, Rational
from sympy.abc import x as x_sym
from sympy.polys.polyfuncs import interpolate


Number = float | Rational


def sympy_poly_quad(
    xs: tuple[Number], fs: tuple[Number], left: Number, right: Number
) -> Number:
    poly = interpolate(list(zip(xs, fs)), x_sym)
    return integrate(poly, (x_sym, left, right))


class Subdomain:
    def __init__(self, left: Number, right: Number, stencil: tuple[Number]):
        self.left = left
        self.right = right
        self.stencil = stencil

    def __repr__(self):
        return f"({self.left}, {self.right})"


class Quadrature:
    def __init__(self, partition: list[Subdomain]):
        self.partition = partition
        self.nodes = list(
            {node for subdomain in partition for node in subdomain.stencil}
        )
        self._weights = None

    def subdomains_containing(self, x: Number):
        return [subdomain for subdomain in self.partition if x in subdomain.stencil]

    def find_weights(self, poly_quad=sympy_poly_quad):
        weights = []
        for x in self.nodes:
            w = 0
            for sub in self.subdomains_containing(x):
                fs = [int(x == y) for y in sub.stencil]
                w += poly_quad(sub.stencil, fs, sub.left, sub.right)
            weights.append(w)
        self._weights = weights

    @property
    def weights(self):
        if self._weights is None:
            self.find_weights()
        return self._weights

    def nodes_and_weights(self):
        return np.array(self.nodes, dtype=float), np.array(self.weights, dtype=float)


class Equispaced(Quadrature):
    def __init__(self, left: Number, right: Number, num_points: int, order: int):
        h = (right - left) / (num_points - 1)
        nodes = [left + h * i for i in range(num_points - 1)] + [right]
        if order % 2 == 0:
            break_points = nodes.copy()
        if order % 2 == 1:
            h2 = h / 2
            break_points = [left]
            break_points += [left + h2 + h * i for i in range(num_points - 1)]
            break_points += [right]
        intervals = list(pairwise(break_points))
        subdomains = []
        for interval in intervals:
            center = sum(interval) / 2
            nodes.sort(key=lambda x: abs(x - center))
            stencil = nodes[:order]
            stencil.sort()
            subdomains.append(Subdomain(*interval, tuple(stencil)))
        nodes.sort()
        super().__init__(subdomains)


def wrap_HTML(order, weights):
    def wrap_math_td(string):
        return "\t<td>$" + string + "$</td>\n"
    ret = "<tr>\n"
    ret += wrap_math_td(f"\\mathcal{{O}}({order})")
    for w in weights:
        ret += wrap_math_td(latex(w))
    ret += "</tr>"
    return ret


if __name__ == "__main__":
    # order = 3
    for order in range(2, 17):
        N = 2*order + 3
        equi = Equispaced(Rational(0, 1), Rational(N - 1, 1), N, order)
        boundary_weights = list(takewhile(lambda w: w != 1, equi.weights))
        print(wrap_HTML(order, boundary_weights))
