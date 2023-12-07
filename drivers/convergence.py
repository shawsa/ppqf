from ..localPP import quadrature_weights
from itertools import product
import matplotlib.pyplot as plt
import numpy as np
import sympy as sym
from tqdm import tqdm

x_sym = sym.symbols("x")

interval = (-1, 1)
# f_sym = sym.exp(x_sym)
# f_sym = 1 / (1 + (5 * x_sym) ** 2)
f_sym = sym.cos(x_sym) * sym.Abs(x_sym - sym.Rational(1, 3))
# f_sym = (x_sym-.5)**5 + 1

Ns = [1 + 2**i for i in range(3, 10)]
hs = [(interval[-1] - interval[0]) / (N - 1) for N in Ns]
stencil_sizes = [2, 4, 6]


foo = sym.lambdify(x_sym, f_sym)
exact = float(sym.integrate(f_sym, (x_sym, *interval)).evalf())

error_dict = {}

for stencil_size, N in tqdm(list(product(stencil_sizes, Ns))):
    xs = np.linspace(*interval, N)
    weights = quadrature_weights(xs, stencil_size=stencil_size)
    approx = weights @ foo(xs)
    E = abs((exact - approx) / exact)
    error_dict[(stencil_size, N)] = E


plt.figure(f"Convergence for f(x)={f_sym}")
for k in stencil_sizes:
    errors = [error_dict[(k, N)] for N in Ns]
    order = np.round(
        np.log(errors[-2] / errors[-1]) / np.log(hs[-2] / hs[-1]),
        2,
    )
    plt.loglog(hs, errors, ".-", label=f"{k=}~$\mathcal{{O}}(h^{{{order}}})$", base=2)

plt.legend()
plt.title(f"Convergence for f(x)={f_sym}")
plt.xticks(hs, [f"$2^{{{np.log2(h)}}}$" for h in hs])
plt.xlabel("$h$")
plt.ylabel("Relative Error")
plt.grid()
plt.tight_layout()

plt.savefig("images/convergence.png")
