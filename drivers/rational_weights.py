

from functools import partial
from itertools import pairwise
import sympy as sym
from sympy.polys.polyfuncs import interpolate




def cardinal(stencil, node):
    return [int(index == node) for index in stencil]


def get_stencil(interval, nodes, k):
    x1, x2 = interval
    center = (x1+x2)/2
    stencil = nodes.copy()
    stencil.sort(key=lambda x: abs(x - center))
    stencil = stencil[:k]
    return sorted(stencil)


def interval_stencil_pairs(nodes, stencil_size):
    return [
        (interval, get_stencil(interval, nodes, stencil_size))
        for interval in pairwise(nodes)
    ]


def filter_node_in_stencil(node, pair):
    return node in pair[1]


def wrap_HTML(order, weights):
    def wrap_math_td(string):
        return "\t<td>$" + string + "$</td>\n"
    ret = "<tr>\n"
    ret += wrap_math_td(f"\\mathcal{{O}}({order})")
    for w in weights:
        ret += wrap_math_td(sym.latex(w))
    ret += "</tr>"
    return ret


x = sym.symbols("x")

max_order = 16
nodes = list(range(max_order*3))
for k in range(2, max_order+1, 2):
    weights = []
    for node in nodes:
        my_filter = partial(filter_node_in_stencil, node)
        pairs = interval_stencil_pairs(nodes, k)
        my_pairs = list(filter(my_filter, pairs))
        w = 0
        for interval, stencil in my_pairs:
            p = interpolate(list(zip(stencil, cardinal(stencil, node))), x)
            w += sym.integrate(p, (x, *interval))
        if w == 1:
            break
        weights.append(w)
    # print(k, weights)
    print(wrap_HTML(k, weights))
