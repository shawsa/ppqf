from ..localPP import quadrature_weights
from itertools import product
import matplotlib.gridspec as gs
import matplotlib.pyplot as plt
import numpy as np
import sympy as sym
from tqdm import tqdm

# generate errors
interval = (-1, 1)
Ns = [1 + 2**i for i in range(5, 10)]
hs = [(interval[-1] - interval[0]) / (N - 1) for N in Ns]
# stencil_sizes = [2, 4, 6]
stencil_sizes = list(range(2, 7))
x_sym = sym.symbols("x")

test_functions = [
    ("exp", sym.exp(x_sym)),
    ("runge", 1 / (1 + (5 * x_sym) ** 2)),
    ("abs", sym.cos(x_sym) * sym.Abs(x_sym - sym.Rational(1, 3))),
    ("poly", (x_sym - 0.5) ** 5 + 1),
]


error_dict = {}
for stencil_size, N in tqdm(list(product(stencil_sizes, Ns))):
    xs = np.linspace(*interval, N)
    weights = quadrature_weights(xs, stencil_size=stencil_size)
    for desc, f_sym in test_functions:
        foo = sym.lambdify(x_sym, f_sym)
        exact = float(sym.integrate(f_sym, (x_sym, *interval)).evalf())
        approx = weights @ foo(xs)
        error = abs((exact - approx) / exact)
        error_dict[(desc, stencil_size, N)] = error


# make figure
plt.rcParams.update(
    {
        "font.size": 12,
        "text.usetex": True,
        "mathtext.fontset": "stix",
        "font.family": "STIXGeneral",
    }
)

figsize = (8, 8)
fig = plt.figure("Convergence Plots", figsize=figsize)
grid = gs.GridSpec(2, 2)
ax_exp = fig.add_subplot(grid[0, 0])
ax_runge = fig.add_subplot(grid[1, 0], sharex=ax_exp, sharey=ax_exp)
ax_abs = fig.add_subplot(grid[0, 1], sharex=ax_exp, sharey=ax_exp)
ax_poly = fig.add_subplot(grid[1, 1], sharex=ax_exp, sharey=ax_exp)
ax_dict = {
    "exp": ax_exp,
    "runge": ax_runge,
    "abs": ax_abs,
    "poly": ax_poly,
}

for desc, f_sym in test_functions:
    ax = ax_dict[desc]
    for k in stencil_sizes:
        errors = [error_dict[(desc, k, N)] for N in Ns]
        order = np.round(
            np.log(errors[-2] / errors[-1]) / np.log(hs[-2] / hs[-1]),
            2,
        )
        ax.loglog(
            hs, errors, ".-", label=f"{k=}~$\\mathcal{{O}}(h^{{{order}}})$", base=2
        )

    ax.legend()
    ax.set_title(f"$f(x)={sym.latex(f_sym)}$")
    ax.grid()

for ax in [ax_poly, ax_runge]:
    ax.set_xlabel("$h$")
    ax.set_xticks(hs, [f"$2^{{{np.log2(h)}}}$" for h in hs])
for ax in [ax_exp, ax_runge]:
    ax.set_ylabel("Relative Erorr")
plt.tight_layout()

plt.savefig("images/convergence.png", dpi=300)
