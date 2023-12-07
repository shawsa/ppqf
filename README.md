# ppqf
A family of quadrature formulae based on piecewise polynomial interpolation.
I am not aware of this quadrature rule being previously discovered.
Trapezoidal rule is a special case.
This is distinct from spline based quadratures.
I haven't proven convergence orders, but I expect them to be prescribed by the stencil size parameter.

# Some Sample QF on equally spaced points.
For even orders, the weights are symmetric, and far enough from the boundary all weights are $\frac{1}{h}$.
For $\mathcal{O}(h^2)$:
$\frac{1}{2h} \big[ 1 \ 2 \ 2 \2 \2 ...$

For $\mathcal{O}(h^4)$:
$\frac{1}{24h} \big[ 8 \ 31 \ 20 \ 25 \ 24 \ 24 \24 ...$

For $\mathcal{O}(h^6)$:
$\frac{1}{1440h} \big[ 459 \ 1982 \ 944 \ 1746 \ 1333 \ 1456 \ 1440 \ 1440 \ 1440 ...$

# Piecewise Polynomial Interpolation
Lorem
