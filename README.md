# Sharp constants for sums of matrix moduli when 1 < p < 2

*The square case, an interpolation bound for Lee's problem, and certified failure of rank-one extremisers.*

Version 0.1.0-candidate, 15 November 2026. DOI [10.5281/zenodo.24237738](https://doi.org/10.5281/zenodo.24237738)
(all versions: [10.5281/zenodo.24237737](https://doi.org/10.5281/zenodo.24237737)). Unrefereed research candidate.
Creator: Anonymous. Release page: https://evidencepress.org/releases/schatten-sum-of-moduli-constants/

## In plain terms

**The everyday fact, and how it breaks for matrices.** For ordinary numbers, |a + b| ≤ |a| + |b|: the size of a sum
is never more than the sum of the sizes. A matrix A also has a natural "absolute value", |A| = (A*A)^(1/2), the
positive part of A once its rotation is removed. For matrices the rule can fail: the sum A + B can be *larger* than
|A| + |B|, even when size is measured by a norm. The question is how much larger, at worst. The answer is a constant
c, and the problem is to find the smallest c that always works.

**How size is measured.** The Schatten p-norms are the standard family of matrix sizes: p = 1 is the trace norm (the
sum of the singular values), p = 2 is the Frobenius norm (the square root of the sum of squared entries) and p = ∞
is the operator norm. For m matrices A₁, …, A_m of size n × n, the question is the smallest c with

  ‖A₁ + … + A_m‖_p ≤ c · ‖ |A₁| + … + |A_m| ‖_p.

**Who asked, and what was known.** Eun-Young Lee (2010, 2012) proved that c = √m always works and asked for the best
constant for two matrices in the Schatten norms; this is now called Lee's problem. Lin and Zhang (2022) solved it for
p = 2. Tang and Zhang extended the question to m matrices and conjectured a formula; T. Zhang introduced the version
with the matrix size n fixed. Qiu (August 2026) proved the formula for every p ≥ 2. Below p = 2 the formula fails:
Zeng, Liu and Ratnavelu, Pang, and Qiu gave counterexamples, all built from rank-one matrices. The October 2026
survey of Bourin and Zhang lists the range 1 < p < 2 as open.

**What this paper proves (always 1 < p < 2).**

1. *The square case.* When there are at least as many matrices as the matrix size (m ≥ n), the best constant is an
   explicit one-variable maximum D_{p,n} (Theorem 2.1). It depends only on the rank of |A₁| + … + |A_m|, every
   extreme case is described, and when m < n the best constant is strictly smaller. For rank-one matrices, the
   building blocks of every known counterexample, the problem is completely solved in every dimension: the answer is
   D_{p,min(m,n)} (Corollary 2.2). Example: D_{3/2,2} = 1.0364143573….
2. *A new bound for any number of matrices in any dimension.* The best constant changes log-convexly with 1/p
   (Theorem 2.3), so the known answers at p = 1 and p = 2 squeeze it in between. This gives
   c ≤ ((1 + √m)/2)^(1 − 1/p) (Corollary 2.4), better than the previous bound m^((p − 1)/(2p)) for every m ≥ 2. For two
   matrices at p = 3/2 the upper bound drops from 1.1225 to 1.0648; the true value is at least 1.0364.
3. *Rank one is not the whole story.* For two 3 × 3 matrices with exact rational entries, a computer-assisted proof
   in exact rational and interval arithmetic shows that the best rank-one value is beaten at nine exponents
   between 11/10 and 17/10 (Proposition 2.5). For example, at p = 3/2 the certified quotient is at least
   1.036425091174, while D_{3/2,2} ≤ 1.036414357334. So rank-one examples cannot settle Lee's problem there.

**How.** Write the sum as a product of two block matrices and apply Hölder's inequality. The problem then depends
only on the eigenvalues of |A₁| + … + |A_m|, and becomes a comparison of two Rényi entropies of that spectrum, whose
extreme case is "one large eigenvalue, the rest equal". This extends T. Zhang's argument for p = 2; the matching
examples are Pang's, with a re-tuned parameter. Credit: Zhang (the method at p = 2), Pang (the examples), Zeng, Liu
and Ratnavelu (the p = 3/2 two-matrix value and factorisation), Harremoës and Sakai–Iwata (the eigenvalue shape),
Qiu (p ≥ 2 and the first numerical higher-rank example, at p = 6/5), Li (transfer to concave functions).

**Limits.** The exact constant for two matrices of arbitrary size (Lee's original problem) is still open for
1 < p < 2, as is the case m < n. The new upper bound is not sharp. The certified excess of general over rank-one
matrices is tiny (from about 3.6 × 10⁻⁵ down to 2 × 10⁻⁷) and may vanish for p near 2; the certificate covers nine
specific exponents, not an interval. The paper has not been refereed; it was checked only by internal AI-assisted
review.

## For specialists

- Fixed-dimension constant: c_p(m, n) = D_{p,n} for m ≥ n, with the sharper rank form
  ‖Σ A_k‖_p ≤ D_{p,r} ‖B‖_p, r = rank B, B = Σ|A_k|; strict inequality c_p(m, n) < D_{p,n} for m < n; equality
  classified (rank-one summands forming a weighted frame of a special shape, Theorem 5.2).
- D_{p,d} = max_{x ≥ 1} √(x + d − 1)(x^q + d − 1)^{1/(2q)} / (x^p + d − 1)^{1/p}, q = p/(2 − p); asymptotically
  D_{p,d} ~ 2^{−1/p} d^{(p−1)/(2p)} (Proposition 6.2), against Zhang's bound min(m, n)^{(p−1)/(2p)}.
- Log-convexity of p ↦ c_p(m, n) and c_p(m) in 1/p via a variational formula and the three-lines theorem
  (Theorem 2.3); D_{p,m} ≤ c_p(m) ≤ ((1 + √m)/2)^{1−1/p}, with ratio → 2^{(2−p)/p} as m → ∞ (against 2^{1/p}).
- Lee's problem at p = 3/2: 1.036425 ≤ c_{3/2}(2) ≤ 1.0647523 (previous upper bound 2^{1/6} = 1.12247).
- Certified c_p(2, 3) > D_{p,2} at p ∈ {11/10, 6/5, 5/4, 13/10, 4/3, 7/5, 3/2, 8/5, 17/10}; numerically the gap is
  about 8 × 10⁻¹⁰ at p = 1.8 and not detected at 1.9 (Section 8; numerical only).
- A consequence for concave functions via Li's transfer theorem (Section 9). Open problems: Section 10.

## Contents

| Path | What it is |
|---|---|
| `manuscript.tex`, `manuscript.pdf` | The paper (16 pages; LaTeX source and PDF, pdflatex three passes) |
| `verification/certify_rank_gap.py` | Computer-assisted proof of Proposition 2.5: exact rational matrices, exact eigenvalue isolation, interval arithmetic |
| `verification/witnesses.json` | The exact rational witnesses for the nine exponents |
| `verification/verify_schatten.py` | 128 numerical checks (sections A–N): scalar constant, equality families, random and adversarial searches, the p = 3/2 radical, Qiu's example, the bounds table, asymptotics, negative controls |
| `verification/plot_bounds.py`, `verification/bounds.pdf`, `verification/bounds.png` | Figure 1 and its script |
| `verification/output/rank_gap_certificate.json`, `verification/output/verification.json` | Recorded outputs |
| `requirements.txt`, `ENVIRONMENT.txt` | Versions used for the recorded outputs |
| `REPLAY_RECEIPT.md` | Clean replay before release (normal and `python -O`), negative control |
| `AI_INDEX.md` | Machine-oriented map of claims, evidence and limits |
| `REVIEW_SUMMARY.md` | Internal review objections and how each was handled (no scores) |
| `RESEARCH_GATES.json` | Contribution map, sources read, limitation triage |
| `refs.bib` | Bibliography built from Crossref and arXiv records |
| `CITATION.cff`, `.zenodo.json`, `LICENSE.md` | Citation metadata and licences |
| `.github/workflows/replay.yml` | CI: manifest check, certificate and checks in normal and `-O` mode |
| `MANIFEST.sha256` | SHA-256 of every other file |

## Reproduce

From any directory outside the package (uv selects Python 3.12):

    uv run --no-project --python 3.12 --with numpy==2.3.5 --with scipy==1.17.0 --with sympy==1.14.0 \
        --with mpmath==1.3.0 python3 -I -B verification/certify_rank_gap.py --out OUTDIR      # about 10 s
    uv run --no-project --python 3.12 --with numpy==2.3.5 --with scipy==1.17.0 --with sympy==1.14.0 \
        --with mpmath==1.3.0 python3 -I -B verification/verify_schatten.py --out OUTDIR       # about 45 s

(use absolute paths to the scripts). Each prints `STATUS PASS` or a JSON `"status": "PASS"` and exits 0; any failed
check exits 1, also under `python -O` (no `assert` statements). The certificate is a proof; the other checks
supplement the written proofs and do not replace them.

## Cite

Anonymous (2026). *Sharp constants for sums of matrix moduli when 1<p<2*. Version 0.1.0-candidate. Evidence Press.
https://doi.org/10.5281/zenodo.24237738

## Licence

Text, paper, figures and data: CC0-1.0. Code: MIT. See `LICENSE.md`.
