# Piecewise Polynomial Quadrature Formulae
A family of quadrature formulae based on piecewise polynomial interpolation.
I am not aware of this quadrature rule being previously discovered.
Trapezoidal rule is a special case.
This is distinct from spline based quadratures.
I haven't proven convergence orders, but I expect them to be prescribed by the stencil size parameter.

# Some Sample QF on equally spaced points.
For even orders, the weights are symmetric, and far enough from the boundary all weights are $\frac{1}{h}$.

For $\mathcal{O}(h^2)$:
$\frac{1}{2h} \big[ 1 \ 2 \ 2 \ 2 \ 2 ...$

For $\mathcal{O}(h^4)$:
$\frac{1}{24h} \big[ 8 \ 31 \ 20 \ 25 \ 24 \ 24 \ 24 ...$

For $\mathcal{O}(h^6)$:
$\frac{1}{1440h} \big[ 459 \ 1982 \ 944 \ 1746 \ 1333 \ 1456 \ 1440 \ 1440 \ 1440 ...$

# Piecewise Polynomial Interpolation
This quadrature is an interpolation based quadrature.
The interpolants found are piecewise polynomials with breakpoints at the nodes.
The interpolants will be continuous, but we do not enforce any degree of smoothness over the break points (unlike splines).

Select a target order $k$.
Over each subdomain ($(x_i, x_{i+1})$) we select the $k$ closest nodes to this interval to be our *stencil*.
We interpolate the stencil points with a dregree $k-1$ polynoial, then restrict the domain of this polynomial to the subdomain.

These quadrature rules are equivalent to integrating exactly this resulting interpolant.

# Not Splines
These interpolants are not the traditional splines.
Like splines, they are continuous piecewise polynomials.
Unlike splines, they do not enforce smoothness.
The figure below compares a function to the local interpolant (our interpolant) of degree 3 and also to a cubic spline with not-a-not boundary conditions.
It also plots the first and second derivatives of each of these functions.
<!---
![Not Splines](images/not_spline.png)
--->
<img src="images/not_spline.png"/>
Note that the second derivative of the local interpolant is discontinuous at some of the breakpoints.
This demonstrates that it is distinct from splines.

We can also compare the cardinal basis for the space of interpolants to the cardinal spline basis.

<!---
![Cardinal Basis](images/cardinal_basis.png)
--->
<img src="images/cardinal_basis.png"/>

We see from the cardinal basis that the local interpolant is not smooth over the breakpoints.
It is not easy to see from this plot, but the cubic spline basis functions are supported over the entire interval.
A consequence of this is that the interpolant over each piece depends on all of the function values over the entire interval.
In contrast, the cardinal basis functions for local interpolation are supported only over a continguous set of $k-$ sub domains.
This means that an individual piece of the interpolant is only sensitive to nearby function values.
It is also the reason for the repeated quadrature weights far from the boundary, as the cardinal basis functions are simply translates of one another.

# Convergence
I've tested convergence of the even order equally spaced quadrature formulae above on several test functions. 

We see that convergence is roughly $\mathcal{O}(h^k)$ for smooth functions.
<img src="images/convergence_exp.png"/>

We avoid error from Runge's phenomenon.
<img src="images/convergence_Runge.png"/>

Furthermore we are exact up to numerical error on polynomials of degree less than $k$.
<img src="images/convergence_poly.png"/>

Lastly, convergence is limited by the smoothness of our function.
<img src="images/convergence_kink.png"/>
