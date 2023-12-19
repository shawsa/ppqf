"""Derive Hermite quadrature nodes."""

from collections import defaultdict
from dataclasses import dataclass
from itertools import pairwise
import numpy as np
from sympy import integrate, Matrix, Rational
from sympy.abc import x

Number = int | float | Rational


@dataclass(eq=True, frozen=True)
class Node:
    value: Number
    order: int


class HermiteStencil:
    def __init__(self, nums: list[Number]):
        nums = sorted(nums)
        nodes = [Node(nums[0], 0)]
        for num in nums[1:]:
            if num == nodes[-1].value:
                nodes.append(Node(num, nodes[-1].order + 1))
            else:
                nodes.append(Node(num, 0))
        self.nodes = nodes

    def weights(self, left: Number, right: Number):
        dim = len(self.nodes)
        poly_basis = [x**i for i in range(dim)]
        rows = []
        for node in self.nodes:
            rows.append([p.diff(x, node.order).subs(x, node.value) for p in poly_basis])
        coef_mat = Matrix(rows).inv().T
        polys = [
            sum(c * x**i for i, c in enumerate(row)) for row in coef_mat.tolist()
        ]
        weights = [integrate(poly, (x, left, right)) for poly in polys]
        return {node: weight for node, weight in zip(self.nodes, weights)}


class HermiteQuadrature:
    def __init__(self, stencil_size: int, order: int):
        self.stencil_size = stencil_size
        self.order = order

        self._init_nodes()
        self._init_partition()
        self._init_subdomains()
        self._init_weights()

    def _init_nodes(self):
        N = self.stencil_size * 2 + 1
        end_repeats = self.order
        self.nodes = [0] * end_repeats + list(range(N)) + [N - 1] * end_repeats

    def _init_partition(self):
        nodes = sorted(list(set(self.nodes)))
        if self.stencil_size % 2 == 0:
            partition = nodes
        else:
            partition = [0]
            for node1, node2 in pairwise(nodes):
                partition.append(Rational(1, 2) * (node1 + node2))
            partition.append(nodes[-1])
        self.partition = partition

    def find_stencil(self, left: int, right: int) -> HermiteStencil:
        nodes = HermiteStencil(self.nodes).nodes
        center = Rational(1, 2) * (left + right)
        nodes.sort(key=lambda node: (abs(center - node.value), node.order))
        return HermiteStencil([node.value for node in nodes[: self.stencil_size]])

    def _init_subdomains(self):
        self.sub_domains = [
            (interval, self.find_stencil(*interval))
            for interval in pairwise(self.partition)
        ]

    def _init_weights(self):
        weights_list = [stencil.weights(a, b) for (a, b), stencil in self.sub_domains]
        quad_weights = defaultdict(lambda: 0)
        for weight_dict in weights_list:
            for node, weight in weight_dict.items():
                quad_weights[node] += weight
        self.weights_dict = quad_weights

    def __repr__(self):
        return str(self.weights_dict)

    def print_weights(self, pre=""):
        items = list(self.weights_dict.items())
        items.sort(key=lambda pair: (pair[0].value, -pair[0].order))
        for node, weight in items:
            print(f"{pre}{node}: \t{weight}")


def get_fd_weights(order: int, stencil_size: int) -> list[Number]:
    nodes = list(range(stencil_size))
    rows = []
    poly_basis = [x**i for i in range(stencil_size)]
    for node in nodes:
        rows.append([p.subs(x, node) for p in poly_basis])
    coef_mat = Matrix(rows).inv().T
    polys = [sum(c * x**i for i, c in enumerate(row)) for row in coef_mat.tolist()]
    return [p.diff(x, order).subs(x, 0) for p in polys]


def gregory(order: int):
    derivative_order = 1
    stencil_size = order
    weights_dict = HermiteQuadrature(
        stencil_size=stencil_size, order=derivative_order
    ).weights_dict
    fd_weights = get_fd_weights(1, stencil_size=stencil_size - 1)
    cancel_node = Node(0, order=1)
    factor = weights_dict[cancel_node]
    weights_dict[cancel_node] -= factor
    for num, w in enumerate(fd_weights):
        node = Node(num, 0)
        weights_dict[node] += factor * w
    weights = [
        w
        for node, w in weights_dict.items()
        if node.value < order - 1 and node.order == 0
    ]
    return weights


def gregory_coefficients(order: int):
    """See https://oeis.org/A002206"""
    weights = gregory(order)
    d_weights = []
    for d_order in range(order-2, 0, -1):
        fd_weights = get_fd_weights(d_order, stencil_size=len(weights))
        factor = (weights[-1] - 1) / fd_weights[-1]
        weights = [w - factor*fdw for w, fdw in zip(weights, fd_weights)]
        assert weights[-1] == 1
        weights = weights[:-1]
        d_weights.append(factor)
    return weights + d_weights[::-1]


if __name__ == "__main__":

    print(f"Gregory coefficients: {gregory_coefficients(7)}")
    for order in range(2, 8):
        print(f"{order=}")
        print(gregory(order))
