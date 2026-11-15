"""Numerical and exact checks for "Sharp constants for sums of matrix moduli when 1<p<2".

The checks supplement, and do not replace, the proofs in the manuscript. Sections:
  A  scalar constant D_{p,d}: unique critical point (sign pattern), monotone in d, log-convex in 1/p (Remark 7.1)
  B  explicit equality families (Section 4 construction, harmonic frames of Remark 5.4) attain D_{p,n}
  C  random complex families never exceed the bound D_{p,rank B}
  D  adversarial optimisation (BFGS): m>=n approaches D_{p,n} but never exceeds it; m<n stays below D_{p,n}
  E  exact p=3/2 radical (sympy) agrees with the numerical D_{3/2,2}
  F  Qiu's p=6/5 example: D_{6/5,2} < ratio < D_{6/5,3}
  G  interpolation bound of Corollary 2.4: D_{p,m} <= ((1+sqrt m)/2)^{1-1/p} < m^{(p-1)/(2p)}; table values
  H  asymptotics of Proposition 6.2 and Remark 6.3 (slow convergence recorded)
  I  numerical (uncertified) size of the rank gap c_p(2,3)-D_{p,2} near p=2
  N  negative controls: a constant lowered by 1e-6 relative is violated; a perturbed equality family loses equality
Every check is explicit (no assert); exit status 1 if any check fails. Output: <out>/verification.json.
Usage: python3 -I verify_schatten.py [--out DIR] [--quick]
Requires numpy, scipy, sympy. Seed 20261112.
"""
import argparse, json, math, sys
from pathlib import Path
import numpy as np
from scipy.optimize import brentq, minimize
import sympy as sp

CHECKS = []


def check(name, ok, **info):
    CHECKS.append({"name": name, "ok": bool(ok), **info})
    if not ok:
        print("FAIL:", name, info)


def scalar(p, d):
    """(x_{p,d}, D_{p,d}) via the critical equation in log variables."""
    if d == 1:
        return 1.0, 1.0
    q = p / (2 - p)
    a = d - 1

    def g(lx):  # critical numerator divided by its leading power (sign of F')
        return (2 * math.exp(-(p - 1) * lx) - math.exp(-(q - 1) * lx) - 1
                + a * (math.exp(-(p + q - 1) * lx) + math.exp(-p * lx) - 2 * math.exp(-q * lx)))

    lo = 1e-6
    if g(lo) <= 0:
        lo = 1e-4
    if g(lo) <= 0:
        raise RuntimeError("no positive start for the critical equation")
    hi = 1.0
    while g(hi) > 0:
        hi *= 2
    lx = brentq(g, lo, hi, xtol=1e-14)
    logC = (0.5 * np.logaddexp(lx, math.log(a)) + np.logaddexp(q * lx, math.log(a)) / (2 * q)
            - np.logaddexp(p * lx, math.log(a)) / p)
    return math.exp(lx), float(math.exp(logC))


def F(p, d, x):
    q = p / (2 - p)
    a = d - 1
    return math.sqrt(x + a) * (x ** q + a) ** (1 / (2 * q)) / (x ** p + a) ** (1 / p)


def modulus(A):
    u, s, vh = np.linalg.svd(A, full_matrices=False)
    return (vh.conj().T * s) @ vh


def snorm(A, p):
    return float(np.sum(np.linalg.svd(A, compute_uv=False) ** p) ** (1 / p))


def ratio(family, p):
    return snorm(sum(family), p) / snorm(sum(modulus(A) for A in family), p)


def extremisers(p, n, m):
    """Equality family of Theorem 5.2 with m >= n nonzero summands (harmonic frame)."""
    x, C = scalar(p, n)
    q = p / (2 - p)
    alpha, beta = x / (x + n - 1), 1 / (x + n - 1)
    lam = np.array([alpha] + [beta] * (n - 1))
    S = float(np.sum(lam ** q))
    V = np.array([[math.sqrt(lam[j]) * np.exp(2j * np.pi * j * k / m) for k in range(m)] for j in range(n)])
    U = (lam ** ((q - 1) / 2) / math.sqrt(S))[:, None] * V
    return [np.outer(U[:, k], V[:, k].conj()) / m for k in range(m)], C


def real_family(x, n, m):
    """A_k = O_k H_k, O_k Cayley-orthogonal, H_k = C_k^T C_k (so |A_k| = H_k)."""
    k = n * (n - 1) // 2
    fam, i = [], 0
    for _ in range(m):
        K = np.zeros((n, n))
        K[np.triu_indices(n, 1)] = x[i:i + k]
        K = K - K.T
        i += k
        O = (np.eye(n) - K) @ np.linalg.inv(np.eye(n) + K)
        C = x[i:i + n * n].reshape(n, n)
        i += n * n
        fam.append(O @ (C.T @ C))
    return fam


def best_real_ratio(p, n, m, starts, rng):
    dim = m * (n * (n - 1) // 2 + n * n)
    best = 0.0
    for _ in range(starts):
        r = minimize(lambda x: -ratio(real_family(x, n, m), p), rng.normal(size=dim), method="BFGS",
                     options={"gtol": 1e-12, "maxiter": 20000})
        best = max(best, -r.fun)
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=".")
    ap.add_argument("--quick", action="store_true", help="fewer optimisation starts")
    args = ap.parse_args()
    rng = np.random.default_rng(20261112)
    starts = 4 if args.quick else 12
    rec = {"seed": 20261112}

    # A. scalar constant
    table = {}
    for p in [1.1, 1.2, 1.5, 1.8, 1.95]:
        prev = 1.0
        for d in range(2, 11):
            x, C = scalar(p, d)
            grid = np.exp(np.linspace(1e-6, math.log(x) * 4 + 5, 4000))
            vals = np.array([F(p, d, t) for t in grid])
            sign_changes = int(np.sum(np.diff(np.sign(np.diff(vals))) != 0))
            check(f"A unique interior maximum p={p} d={d}", sign_changes == 1 and abs(F(p, d, x) - C) < 1e-12
                  and C >= vals.max() - 1e-12, sign_changes=sign_changes)
            check(f"A strict increase in d p={p} d={d}", C > prev)
            prev = C
            table[f"{p},{d}"] = {"x": x, "D": C}
    for d in [2, 3, 5, 10]:
        s = np.linspace(0.5, 1.0, 41)
        vals = []
        for t in s:
            p = 1 / t
            if abs(p - 1) < 1e-12:
                vals.append(0.0)
            elif abs(p - 2) < 1e-12:
                vals.append(0.5 * math.log((1 + math.sqrt(d)) / 2))
            else:
                vals.append(math.log(scalar(p, d)[1]))
        sec = np.diff(vals, 2)
        check(f"A log D_(p,{d}) convex in 1/p for p in [1,2]", sec.min() > -1e-12, min_second_difference=float(sec.min()))
    rec["scalar_table"] = table

    # B. equality families
    max_err = 0.0
    for p in [1.1, 1.2, 1.5, 1.8, 1.95]:
        for n in [2, 3, 5]:
            for m in [n, n + 2]:
                fam, C = extremisers(p, n, m)
                max_err = max(max_err, abs(ratio(fam, p) - C))
    check("B equality families attain D_{p,n}", max_err < 1e-11, max_abs_error=max_err)
    rec["max_extremiser_abs_error"] = max_err

    # C. random complex families
    max_frac, trials = 0.0, 0
    for p in [1.2, 1.5, 1.8]:
        for n in [2, 3, 4]:
            for m in [1, 2, 3, 5]:
                for _ in range(25):
                    fam = [rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)) for _ in range(m)]
                    r = np.linalg.matrix_rank(sum(modulus(A) for A in fam))
                    frac = ratio(fam, p) / scalar(p, r)[1]
                    max_frac = max(max_frac, frac)
                    trials += 1
    check("C random families obey D_{p,rank B}", max_frac < 1 + 1e-10, trials=trials, max_fraction=max_frac)
    rec.update(random_trials=trials, max_random_ratio_to_bound=max_frac)

    # D. adversarial optimisation
    adv = []
    for p, n, m in [(1.5, 2, 2), (1.5, 2, 3), (1.2, 3, 3), (1.5, 3, 2), (1.2, 3, 2)]:
        best = best_real_ratio(p, n, m, starts, rng)
        Dn = scalar(p, n)[1]
        adv.append({"p": p, "n": n, "m": m, "best_ratio": best, "D_pn": Dn})
        check(f"D adversarial never exceeds D_(p,n) p={p} n={n} m={m}", best <= Dn * (1 + 1e-10))
        if m >= n:
            check(f"D adversarial reaches D_(p,n) p={p} n={n} m={m}", best >= Dn * (1 - 1e-7))
        else:
            check(f"D strictly below D_(p,n) for m<n p={p} n={n} m={m}", best < Dn * (1 - 1e-4))
    rec["adversarial"] = adv

    # E. exact radical
    y = (1 + sp.sqrt(17)) / 2
    special = sp.radsimp(y ** 4 * (y * y - 3) / (y ** 3 - 3 * y + 2) ** 2)
    exact_ok = sp.simplify(special - (107 + 51 * sp.sqrt(17)) / 256) == 0
    t = sp.Symbol("t")
    fac = sp.factor(t ** 6 - t ** 5 - t ** 4 - 2 * t ** 3 - t ** 2 - t + 1)
    specialC = float(special ** sp.Rational(1, 6))
    check("E radical identity exact", exact_ok)
    check("E radical equals numerical D_{3/2,2}", abs(specialC - scalar(1.5, 2)[1]) < 1e-12, value=specialC)
    check("E sextic has spurious factor t^2+1", sp.expand(fac - (t ** 2 + 1) * (t ** 4 - t ** 3 - 2 * t ** 2 - t + 1)) == 0)
    rec["special_value"] = specialC

    # F. Qiu's obstruction
    A = np.diag([1., 0., 0.])
    Bq = np.array([[.68128169, .59021564, -.00149331], [.32727794, .28426802, 0.], [0., 0., 0.]])
    qr = ratio([A, Bq], 1.2)
    D2, D3 = scalar(1.2, 2)[1], scalar(1.2, 3)[1]
    check("F Qiu example between D_{6/5,2} and D_{6/5,3}", D2 < qr < D3)
    rec["qiu_obstruction"] = {"p": 1.2, "m": 2, "n": 3, "observed": qr, "rankone_m2": D2, "dimension_n3": D3}

    # G. interpolation bound
    comp = []
    for p in [1.2, 1.5, 1.8]:
        for m in [2, 3, 5, 10, 100]:
            Dm = scalar(p, m)[1]
            interp = ((1 + math.sqrt(m)) / 2) ** (1 - 1 / p)
            tz = math.sqrt(m) ** (1 - 1 / p)
            comp.append({"p": p, "m": m, "D_pm": Dm, "interpolation_bound": interp, "tang_zhang_bound": tz})
            check(f"G D_(p,m) <= interpolation bound < Tang-Zhang p={p} m={m}", Dm <= interp < tz)
    rec["interpolation_comparison"] = comp

    # H. asymptotics
    asym = []
    for p in [1.2, 1.5, 1.8]:
        for d in [100, 10000, 1000000]:
            x, C = scalar(p, d)
            a = d - 1
            asym.append({"p": p, "d": d, "x_over_a_pow": x / a ** (1 / p),
                         "C_over_asymptotic": C / (2 ** (-1 / p) * a ** ((p - 1) / (2 * p)))})
    trend_ok = all(abs(asym[3 * i + 2]["C_over_asymptotic"] - 1) < abs(asym[3 * i]["C_over_asymptotic"] - 1)
                   for i in range(3))
    check("H asymptotic ratio moves toward 1 as d grows", trend_ok)
    rec["asymptotics"] = asym

    # I. numerical rank gap near p=2 (not certified)
    gaps = []
    for p in [1.8, 1.9]:
        best = best_real_ratio(p, 3, 2, starts, rng)
        gaps.append({"p": p, "best_ratio": best, "D_p2": scalar(p, 2)[1], "difference": best - scalar(p, 2)[1]})
    rec["numerical_rank_gap_near_2"] = gaps

    # N. negative controls
    fam, C = extremisers(1.5, 3, 3)
    check("N lowered constant is violated", ratio(fam, 1.5) > C * (1 - 1e-6))
    pert = [M + 1e-3 * rng.normal(size=M.shape) for M in fam]
    check("N perturbed family loses equality", ratio(pert, 1.5) < C - 1e-9)

    rec["checks"] = CHECKS
    rec["total_checks"] = len(CHECKS)
    rec["status"] = "PASS" if all(c["ok"] for c in CHECKS) else "FAIL"
    od = Path(args.out)
    od.mkdir(parents=True, exist_ok=True)
    (od / "verification.json").write_text(json.dumps(rec, indent=2))
    print(json.dumps({k: rec[k] for k in ["status", "total_checks", "random_trials", "max_random_ratio_to_bound",
                                          "max_extremiser_abs_error", "special_value", "qiu_obstruction",
                                          "numerical_rank_gap_near_2"]}, indent=2))
    sys.exit(0 if rec["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
