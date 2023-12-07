from ..localPP import LocalInterpolator
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline
import sympy as sym


interval = (-np.pi, np.pi)
N = 11
stencil_size = 4

x_sym = sym.symbols("x")
# f_sym = sym.sin(x_sym)
f_sym = 1 / (1 + x_sym**2)

foo = sym.lambdify(x_sym, f_sym)
dfoo = sym.lambdify(x_sym, f_sym.diff(x_sym))
d2foo = sym.lambdify(x_sym, f_sym.diff(x_sym, 2))

xs = np.linspace(*interval, N)
fs = foo(xs)
approx = LocalInterpolator(xs, fs, stencil_size=stencil_size)
spline = CubicSpline(xs, fs)

zs = np.linspace(*interval, 2001)
fig, axes = plt.subplots(3, 1, figsize=(10, 10))
plt.suptitle(f"Stencil size = {stencil_size}")
axes[0].set_title(f"f(x) = {f_sym}")
axes[0].plot(zs, foo(zs), "b-", label="True")
axes[0].plot(xs, fs, "bo")
axes[0].plot(zs, approx(zs), "g--", label="Approx")
axes[0].plot(zs, spline(zs), "r--", label="Spline")

axes[1].set_title("Derivative")
axes[1].plot(zs, dfoo(zs), "b-", label="True")
axes[1].plot(zs, approx.derivative()(zs), "g--", label="Approx")
axes[1].plot(zs, spline.derivative()(zs), "r--", label="Spline")

axes[2].set_title("2nd derivative")
axes[2].plot(zs, d2foo(zs), "b-", label="True")
axes[2].plot(zs, approx.derivative(2)(zs), "g--", label="Approx")
axes[2].plot(zs, spline.derivative(2)(zs), "r--", label="Spline")

for ax in axes:
    ax.legend()

plt.tight_layout()

plt.savefig("images/not_spline.png")

# plt.figure("Error")
# plt.semilogy(zs, np.abs(foo(zs) - approx(zs)), "g-", label="Approx")
# plt.semilogy(zs, np.abs(foo(zs) - spline(zs)), "r-", label="Spline")
# plt.legend()
