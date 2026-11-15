# AI index: Sharp constants for sums of matrix moduli when 1<p<2 (v0.1.0-candidate)

Machine-oriented map of claims, evidence and limits. Human readers should start with [README.md](README.md) ("In plain
terms") and the paper [manuscript.pdf](manuscript.pdf) (source [manuscript.tex](manuscript.tex); Section 1 is a plain
introduction and Section 2 states every result). DOI 10.5281/zenodo.24237738 (concept 10.5281/zenodo.24237737).
Status: unrefereed candidate; internal AI-assisted review only.

## Normalisation

A_1..A_m in M_n(C); |A| = (A*A)^{1/2}; ||X||_p = (Tr |X|^p)^{1/p}. c_p(m,n) = smallest c with
||sum_k A_k||_p <= c ||sum_k |A_k| ||_p for all such families; c_p(m) = sup_n c_p(m,n) (Lee's problem: m = 2).
Throughout 1 < p < 2 and q = p/(2-p), so 1/p = 1/2 + 1/(2q). For d >= 2, a = d-1:
F_{p,d}(x) = sqrt(x+a) (x^q+a)^{1/(2q)} / (x^p+a)^{1/p}, x >= 1, with unique maximiser x_{p,d} > 1;
D_{p,d} = F_{p,d}(x_{p,d}), D_{p,1} = 1, and the endpoint values D_{1,d} = 1, D_{2,d} = sqrt((1+sqrt d)/2).
Examples: D_{3/2,2} = ((107+51 sqrt 17)/256)^{1/6} = 1.0364143573..., D_{6/5,2} = 1.0073249657....

## Claims and where they are proved

| ID | Claim | Location in the paper | Status / credit |
|---|---|---|---|
| T2.1 | ||sum A_k||_p <= D_{p,r} ||B||_p <= D_{p,n} ||B||_p, B = sum |A_k|, r = rank B; c_p(m,n) = D_{p,n} for m >= n; c_p(m,n) < D_{p,n} for m < n | Theorem 2.1; Sections 3–5 | extends T. Zhang's p = 2 proof (Theorem 6.2 of arXiv:2603.01046) to 1 < p < 2; sharpness family is Pang's with re-optimised parameter; new in the bounded search |
| C2.2 | Rank-one summands: best constant D_{p,min(m,n)} in every dimension; dimension-free rank-one constant D_{p,m} | Corollary 2.2; Corollary 5.3 | new in the bounded search; p = 3/2, m = 2 value due to Zeng–Liu–Ratnavelu |
| T5.2 | Equality cases: every nonzero summand rank one, weighted frame of a special shape | Theorem 5.2, Corollary 5.3 | new in the bounded search |
| L3.1 | Scalar extremum on the simplex: maximiser one large coordinate, rest equal; unique optimal ratio | Lemma 3.1 | special case of Harremoës (2009) and Sakai–Iwata; self-contained proof with uniqueness |
| T2.3 | 1/p -> log c_p(m,n) and 1/p -> log c_p(m) are convex on 1 <= p <= infinity | Theorem 2.3; Section 7 | new in the bounded search; interpolation antecedents in Qiu and Li are cited |
| C2.4 | c_p(m,n) <= ((1+sqrt min(m,n))/2)^{1-1/p}; D_{p,m} <= c_p(m) <= ((1+sqrt m)/2)^{1-1/p} < m^{(p-1)/(2p)} for m >= 2; bracket ratio -> 2^{(2-p)/p} | Corollary 2.4; Table 2; Figure 1 | improves the Tang–Zhang bound m^{(p-1)/(2p)} |
| P2.5 | c_p(2,3) > D_{p,2} (hence c_p(2) > D_{p,2}) for p in {11/10, 6/5, 5/4, 13/10, 4/3, 7/5, 3/2, 8/5, 17/10} | Proposition 2.5; Section 8; Table 3 | computer-assisted proof in exact rational and interval arithmetic; extends Qiu's single numerical example at p = 6/5 |
| P6.2 | D_{p,d} ~ 2^{-1/p} (d-1)^{(p-1)/(2p)} as d -> infinity; limits D_{p,d} -> 1 (p -> 1) and sqrt((1+sqrt d)/2) (p -> 2) | Proposition 6.2, Remark 6.3 | slow convergence recorded |
| C9.1 | Concave-function consequence via Li's transfer theorem | Corollary 9.1 | consequence of Li (arXiv:2608.25989) and T2.1 |
| S8 | Rank gap near p = 2: about 8e-10 at p = 1.8, none detected at 1.9 | Section 8 ("What the numerics suggest") | numerical only, not certified |

Not claimed: the exact dimension-free constant c_p(m), including Lee's m = 2 case; c_p(m,n) for m < n; sharpness of
the interpolation bound; a gap for p in an interval or near 2; anything for p > 2 or p = 1 beyond what is cited.

## Evidence files

- [verification/certify_rank_gap.py](verification/certify_rank_gap.py) with data
  [verification/witnesses.json](verification/witnesses.json) (output
  [verification/output/rank_gap_certificate.json](verification/output/rank_gap_certificate.json)): the proof of P2.5.
  For each p, A_k = O_k H_k with O_k the Cayley transform of an exact rational skew-symmetric matrix and
  H_k = C_k^T C_k; exact orthogonality and symmetry checked; eigenvalues of the 3x3 Gram matrices isolated exactly
  (sympy, width 1e-40); p-th powers enclosed in mpmath interval arithmetic; D_{p,2} bounded above through a certified
  sign bracket of the critical-point equation and 50 sub-intervals; control below D_{p,3}. Exit 1 on any failure.
- [verification/verify_schatten.py](verification/verify_schatten.py) (128 checks; output
  [verification/output/verification.json](verification/output/verification.json)): sections A–N. Per claim: L3.1, P6.2
  -> A and H; T2.1, T5.2 -> B (equality families), C (random families), D (adversarial BFGS for m >= n and m < n);
  D_{3/2,2} radical -> E; Qiu's example -> F; C2.4, Table 2 -> G; S8 -> I; negative controls -> N.
- [verification/plot_bounds.py](verification/plot_bounds.py): Figure 1
  ([verification/bounds.png](verification/bounds.png), [verification/bounds.pdf](verification/bounds.pdf)).
- [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md): clean replay before freezing, normal and `python -O`, byte-identical outputs,
  negative control. [ENVIRONMENT.txt](ENVIRONMENT.txt), [requirements.txt](requirements.txt): versions.
- [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md): internal review objections and dispositions.
- [RESEARCH_GATES.json](RESEARCH_GATES.json): contribution map, sources read, limitation triage.
- [refs.bib](refs.bib): bibliography from Crossref and arXiv records. [LICENSE.md](LICENSE.md): CC0-1.0 text and data,
  MIT code. [CITATION.cff](CITATION.cff), [.zenodo.json](.zenodo.json): citation metadata. CI:
  [.github/workflows/replay.yml](.github/workflows/replay.yml). [MANIFEST.sha256](MANIFEST.sha256): SHA-256 of every file.

## Limits

No human peer review, independent human reproduction or formal verification. Proposition 2.5 trusts sympy's exact
root isolation and mpmath's interval elementary functions. The certified excess over D_{p,2} is small (1.96e-7 at
p = 17/10 to about 3.6e-5) and covers nine exponents only. Several cited works are arXiv preprints or GitHub
manuscripts (Pang, Qiu, Li, Zeng–Liu–Ratnavelu). Priority rests on a bounded search.
