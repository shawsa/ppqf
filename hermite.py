import sympy as sym


def hermite_interp(interp_list):
    xs = list(range(len(interp_list)))
    fs_flat = [f for fs_list in interp_list for f in fs_list]
    dim = sum(map(len, interp_list))
    x_sym = sym.symbols("x")
    poly_basis = [x_sym**i for i in range(dim)]
    rows = []
    for x, fs_list in zip(xs, interp_list):
        for order, _ in enumerate(fs_list):
            rows.append([p.diff(x_sym, order).subs(x_sym, x) for p in poly_basis])
    coeffs = list(sym.Matrix(rows).solve(sym.Matrix(fs_flat)))
    return coeffs


def hermite_interp_integrate(interp_list, interval):
    x_sym = sym.symbols("x")
    coeffs = hermite_interp(interp_list)
    poly = sum(c * x_sym**i for i, c in enumerate(coeffs))
    return sym.integrate(poly, (x_sym, *interval))


if __name__ == "__main__":

    interp_list = [
        [0, 1],
        [0],
    ]
    coeffs = hermite_interp(interp_list)

    x_sym = sym.symbols("x")
    poly = sum(c * x_sym**i for i, c in enumerate(coeffs))
    print(poly)

    for x, fs_list in enumerate(interp_list):
        for order, f in enumerate(fs_list):
            assert f == poly.diff(x_sym, order).subs(x_sym, x)

    # 4 point stencils
    print("O(4) stencil")

    weights = []

    # f'(0)
    w = 0
    for interp_list, interval in [
            ([[0, 1], [0], [0]], [0, 1]),
    ]:
        w += hermite_interp_integrate(interp_list, interval)
    print("f'(0): ", w)
    weights.append(w)

    # f(0)
    w = 0
    for interp_list, interval in [
            ([[1, 0], [0], [0]], [0, 1]),
            ([[1], [0], [0], [0]], [1, 2]),
    ]:
        w += hermite_interp_integrate(interp_list, interval)
    print("f(0): ", w)
    weights.append(w)

    # f(1)
    w = 0
    for interp_list, interval in [
            ([[0, 0], [1], [0]], [0, 1]),
            ([[0], [1], [0], [0]], [1, 2]),
            ([[1], [0], [0], [0]], [1, 2]),
    ]:
        w += hermite_interp_integrate(interp_list, interval)
    print("f(1): ", w)
    weights.append(w)

    # f(2)
    w = 0
    for interp_list, interval in [
            ([[0, 0], [0], [1]], [0, 1]),
            ([[0], [0], [1], [0]], [1, 2]),
            ([[0], [1], [0], [0]], [1, 2]),
            ([[1], [0], [0], [0]], [1, 2]),
    ]:
        w += hermite_interp_integrate(interp_list, interval)
    print("f(2): ", w)
    weights.append(w)

    # f(3)
    w = 0
    for interp_list, interval in [
            ([[0], [0], [0], [1]], [1, 2]),
            ([[0], [0], [1], [0]], [1, 2]),
            ([[0], [1], [0], [0]], [1, 2]),
            ([[1], [0], [0], [0]], [1, 2]),
    ]:
        w += hermite_interp_integrate(interp_list, interval)
    print("f(3): ", w)
    weights.append(w)

    dw = weights[0]
    qw = weights[1:-1]
    fd_stencil = [sym.Rational(-3, 2), sym.Rational(2, 1), sym.Rational(-1, 2)]

    gregory = [w + dw*c for w, c in zip(qw, fd_stencil)]
    print("Use FD stencil for derivative")
    print("gives the Gregory weights")
    print("weights: ", gregory)

