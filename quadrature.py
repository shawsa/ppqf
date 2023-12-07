import numpy as np
from .interpolate import LocalInterpolator


def get_weights(nodes, *, stencil_size=4) -> np.ndarray[float]:
    interval = (nodes[0], nodes[-1])
    return np.array(
        [
            phi.integrate(*interval)
            for phi in get_cardinal_basis(nodes, stencil_size=stencil_size)
        ]
    )


def get_cardinal_basis(nodes, *, stencil_size=4) -> list[LocalInterpolator]:
    def cardinal(index):
        ret = np.zeros_like(nodes)
        ret[index] = 1.0
        return ret

    return [
        LocalInterpolator(nodes, cardinal(index), stencil_size=stencil_size)
        for index in range(len(nodes))
    ]


if __name__ == "__main__":
    import sympy as sym
    x_sym = sym.symbols("x")
    from collections import defaultdict

    N = 21
    stencil_size = 6
    interval = (-1, 1)
    f_sym = 1 / (1 + (5 * x_sym) ** 2)

    # convenient denominators for weights
    weight_factors = defaultdict(lambda: 1, {
        2: 2,
        4: 24,
        6: 1440,
    })
    weight_factor = weight_factors[stencil_size]

    print(f"f(x) = {f_sym}")
    print(f"on {interval}")

    foo = sym.lambdify(x_sym, f_sym)
    I = sym.integrate(f_sym, (x_sym, *interval)).evalf()
    print(f"{I=}")

    xs = np.linspace(*interval, N)
    h = (xs[-1] - xs[0])/(N-1)
    weights = get_weights(xs, stencil_size=stencil_size)
    Q = weights @ foo(xs)
    print(f"{Q=}")
    E = abs((I - Q)/I)
    print(f"{E=}")

    print(f"({weight_factor}/h)*weights:")
    for w in weights:
        print(f"\t{np.round(w*weight_factor/h, 8)}")
