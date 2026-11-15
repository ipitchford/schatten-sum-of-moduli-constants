"""Certified lower bounds c_p(2,3) > D_{p,2} (Proposition 2.5 of the manuscript).

For each exponent p in witnesses.json the script
  1. rebuilds two real 3x3 matrices A_k = O_k H_k in exact rational arithmetic
     (O_k orthogonal by the Cayley transform, H_k = C_k^T C_k positive semidefinite, so |A_k| = H_k exactly);
  2. isolates the eigenvalues of N^T N (N = A_1 + A_2) and of B = H_1 + H_2 exactly (sympy real-root isolation of
     the rational characteristic polynomials, intervals of width <= 1e-40);
  3. encloses ||N||_p^p = sum lambda^(p/2) and ||B||_p^p = sum mu^p with mpmath interval arithmetic;
  4. encloses D_{p,2}^p = max_{x>1} F_{p,2}(x)^p from above: the unique critical point (Lemma 3.1) is bracketed by
     exact rational bisection with interval sign checks, F is increasing before and decreasing after the bracket,
     and F^p is enclosed on the bracket by interval evaluation;
  5. reports PASS for p only if lower(ratio^p) > upper(D_{p,2}^p).
Consistency control (Theorem 2.1): it also checks upper(ratio^p) < lower(D_{p,3}^p), i.e. the witness obeys the
dimension bound. Exit status 1 if anything fails. No assert statements (safe under python -O).

Usage: python3 -I certify_rank_gap.py [--witnesses witnesses.json] [--out DIR]
"""
import argparse, json, sys
from pathlib import Path
import sympy as sp
import mpmath as mp

iv = mp.iv
iv.dps = 60
mp.mp.dps = 60


def qiv(r):
    r = sp.Rational(r)
    return iv.mpf(int(r.p)) / iv.mpf(int(r.q))


def build(summ):
    n = 3
    O_H = []
    for s in summ:
        K = sp.zeros(n)
        idx = [(0, 1), (0, 2), (1, 2)]
        for (a, b), v in zip(idx, s["K_upper"]):
            K[a, b] = sp.Rational(v)
            K[b, a] = -sp.Rational(v)
        O = (sp.eye(n) - K) * (sp.eye(n) + K).inv()
        C = sp.Matrix(n, n, [sp.Rational(v) for v in s["C_rowmajor"]])
        O_H.append((O, C.T * C))
    return O_H


def eig_enclosures(S):
    lam = sp.Symbol("l")
    P = sp.Poly(S.charpoly(lam).as_expr(), lam)
    out = []
    for (lo, hi), mult in P.intervals(eps=sp.Rational(1, 10**40)):
        for _ in range(mult):
            out.append(iv.mpf([qiv(lo).a, qiv(hi).b]))
    return out if len(out) == S.shape[0] else None


def down(x, k):
    """Decimal string with k digits after the point, rounded toward -infinity (x > 0)."""
    s = mp.floor(mp.mpf(x) * mp.mpf(10) ** k)
    return _fmt(s, k)


def up(x, k):
    """Decimal string with k digits after the point, rounded toward +infinity (x > 0)."""
    s = mp.ceil(mp.mpf(x) * mp.mpf(10) ** k)
    return _fmt(s, k)


def _fmt(s, k):
    n = int(s)
    sign = "-" if n < 0 else ""
    n = abs(n)
    return f"{sign}{n // 10**k}.{n % 10**k:0{k}d}"


def ipow(I, e):
    lo = max(I.a, mp.mpf(0))
    return iv.mpf([lo, I.b]) ** e


def D_power_bounds(pf, a):
    """Return (lower, upper) enclosure of max_{x>1} F_{p,d}(x)^p, d=a+1."""
    q = pf / (2 - pf)
    A = qiv(a)

    def Fp(X):
        return ((X + A) ** (pf / 2)) * ((X ** q + A) ** (pf / (2 * q))) / (X ** pf + A)

    def crit(X):
        return 1 / (X + A) + X ** (q - 1) / (X ** q + A) - 2 * X ** (pf - 1) / (X ** pf + A)

    lo = hi = None
    prev = sp.Rational(1) + sp.Rational(1, 200)
    for j in range(2, 400000):
        cur = 1 + sp.Rational(j, 200)
        if crit(qiv(prev)).a > 0 and crit(qiv(cur)).b < 0:
            lo, hi = prev, cur
            break
        prev = cur
    if lo is None:
        return None
    for _ in range(80):
        mid = (lo + hi) / 2
        cm = crit(qiv(mid))
        if cm.a > 0:
            lo = mid
        elif cm.b < 0:
            hi = mid
        else:
            break
    sub = 50
    upper = mp.mpf(0)
    for j in range(sub):
        I = iv.mpf([qiv(lo + (hi - lo) * sp.Rational(j, sub)).a, qiv(lo + (hi - lo) * sp.Rational(j + 1, sub)).b])
        upper = max(upper, Fp(I).b)
    lower = Fp(qiv(lo)).a  # a value of F^p at an admissible point
    return lower, upper, (float(lo), float(hi))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--witnesses", default=str(Path(__file__).with_name("witnesses.json")))
    ap.add_argument("--out", default=".")
    args = ap.parse_args()
    data = json.loads(Path(args.witnesses).read_text())
    results, ok_all = [], True
    for w in data["witnesses"]:
        p = sp.Rational(w["p"])
        pf = qiv(p)
        O_H = build(w["summands"])
        checks_ok = all(O.T * O == sp.eye(3) and H == H.T for O, H in O_H)
        N = O_H[0][0] * O_H[0][1] + O_H[1][0] * O_H[1][1]
        B = O_H[0][1] + O_H[1][1]
        eN, eB = eig_enclosures(N.T * N), eig_enclosures(B)
        checks_ok = checks_ok and eN is not None and eB is not None
        if not checks_ok:
            ok_all = False
            results.append({"p": str(p), "status": "FAIL", "reason": "orthogonality/symmetry or eigenvalue count"})
            continue
        num = sum(ipow(l, pf / 2) for l in eN)
        den = sum(ipow(l, pf) for l in eB)
        rp = num / den
        D2 = D_power_bounds(pf, 1)
        D3 = D_power_bounds(pf, 2)
        gap_ok = D2 is not None and rp.a > D2[1]
        control_ok = D3 is not None and rp.b < D3[0]
        ok = checks_ok and gap_ok and control_ok
        ok_all &= ok
        inv_p = 1 / pf  # interval exponent
        r_lo = (iv.mpf(rp.a) ** inv_p).a            # p-th roots taken in interval arithmetic
        d2_hi = (iv.mpf(D2[1]) ** inv_p).b if D2 else None
        d3_lo = (iv.mpf(D3[0]) ** inv_p).a if D3 else None
        ratio_lo, D2_hi = float(down(r_lo, 12)), float(up(d2_hi, 12)) if D2 else None
        results.append({
            "p": str(p), "exact_orthogonality_and_symmetry": checks_ok,
            "ratio_lower": down(r_lo, 15),
            "D_p2_upper": up(d2_hi, 15) if D2 else None,
            "certified_gap_lower": down((iv.mpf(r_lo) - iv.mpf(d2_hi)).a, 10) if D2 else None,
            "D_p3_lower": down(d3_lo, 15) if D3 else None,
            "certified_c_p23_gt_D_p2": gap_ok, "control_below_D_p3": control_ok, "status": "PASS" if ok else "FAIL",
            "rounding": "lower bounds rounded down, upper bounds rounded up (decimal strings)",
        })
        print(f"p={p}: ratio >= {down(r_lo, 12)}, D_p,2 <= {up(d2_hi, 12)}, gap certified: {gap_ok}, control: {control_ok}")
    out = {"status": "PASS" if ok_all else "FAIL", "results": results}
    od = Path(args.out)
    od.mkdir(parents=True, exist_ok=True)
    (od / "rank_gap_certificate.json").write_text(json.dumps(out, indent=2))
    print("STATUS", out["status"])
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
