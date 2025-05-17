import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update(
    {
        "font.size": 12,
        "text.usetex": True,
        "mathtext.fontset": "stix",
        "font.family": "STIXGeneral",
    }
)

xs = np.arange(20)

line1 = 0
line2 = 0.5

line3 = 2
line4 = 2.5

fig = plt.figure(figsize=(8, 2))

plt.plot(xs, line1 + 0*xs, "k.-")
plt.plot(xs, line1 + 0*xs, "k|", markersize=10)

plt.plot(xs[:2], line2 + 0*xs[:2], "r-")
plt.plot(xs[:4], line2 + 0*xs[:4], "r.")

plt.plot(xs[10:12], line2 + 0*xs[10:12], "r-")
plt.plot(xs[9:13], line2 + 0*xs[9:13], "r.")


plt.plot(xs, line3 + 0*xs, "k.-")
plt.plot([xs[0], xs[-1]], [line3, line3], "k|", markersize=10)
halfs = xs[0:-1] + 0.5
plt.plot(halfs, line3 + 0*halfs, "k|", markersize=10)

plt.plot([xs[0], halfs[0]], [line4, line4], "r-")
plt.plot(xs[0:3], 3*[line4], "r.")


plt.plot(halfs[10:12], [line4, line4], "r-")
plt.plot(xs[10:13], 3*[line4], "r.")

plt.axis("off")
plt.title("Points, partitions, and stencils")

plt.savefig("images/stencil.png", dpi=300)
