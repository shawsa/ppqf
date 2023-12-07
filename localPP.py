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


def cardinal_basis(nodes, *, stencil_size=4) -> list[LocalInterpolator]:
    def cardinal(index):
        ret = np.zeros_like(nodes)
        ret[index] = 1.0
        return ret

    return [
        LocalInterpolator(nodes, cardinal(index), stencil_size=stencil_size)
        for index in range(len(nodes))
    ]


def quadrature_weights(nodes, *, stencil_size=4) -> np.ndarray[float]:
    interval = (nodes[0], nodes[-1])
    return np.array(
        [
            phi.integrate(*interval)
            for phi in cardinal_basis(nodes, stencil_size=stencil_size)
        ]
    )


