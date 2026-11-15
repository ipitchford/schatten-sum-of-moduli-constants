"""Figure 1: bracket for the dimension-free constant c_p(m) (Corollary 2.4).
Lower curve D_{p,m} (Theorem 2.1 / Corollary 2.2), new upper bound ((1+sqrt m)/2)^{1-1/p} (Corollary 2.4),
previous upper bound m^{(p-1)/(2p)} (Tang-Zhang). Usage: python3 -I plot_bounds.py [--out DIR]"""
import argparse, math, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(Path(__file__).parent))
from verify_schatten import scalar  # noqa: E402

ap = argparse.ArgumentParser(); ap.add_argument("--out", default="."); args = ap.parse_args()
ms = list(range(1, 41))
fig, axes = plt.subplots(1, 3, figsize=(10, 3.3), sharey=False)
for ax, p in zip(axes, [1.2, 1.5, 1.8]):
    D = [scalar(p, m)[1] for m in ms]
    new = [((1 + math.sqrt(m)) / 2) ** (1 - 1 / p) for m in ms]
    tz = [math.sqrt(m) ** (1 - 1 / p) for m in ms]
    ax.plot(ms, tz, color="0.55", ls="--", lw=1.4, label=r"previous upper bound $m^{(p-1)/(2p)}$")
    ax.plot(ms, new, color="tab:blue", lw=1.8, label=r"new upper bound $((1+\sqrt{m})/2)^{1-1/p}$")
    ax.plot(ms, D, color="tab:red", lw=1.8, label=r"lower bound $D_{p,m}$ (rank one)")
    ax.set_title(f"p = {p}")
    ax.set_xlabel("number of summands m")
    ax.grid(alpha=0.3)
axes[0].set_ylabel(r"bounds for $c_p(m)$")
axes[0].legend(fontsize=7, loc="upper left")
fig.tight_layout()
od = Path(args.out); od.mkdir(parents=True, exist_ok=True)
fig.savefig(od / "bounds.pdf"); fig.savefig(od / "bounds.png", dpi=200)
print("wrote", od / "bounds.pdf")
