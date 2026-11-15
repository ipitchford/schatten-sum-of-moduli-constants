# Review summary (public, rating-free)

Internal AI-assisted review of the first version and of its revision (14–15 November 2026). This is not human peer
review, independent reproduction or formal verification.

**Who reviewed.** First round: five reviewer roles run as separate AI agents (editor, methodology, domain specialist,
cross-disciplinary perspective, devil's advocate), one adversarial review by a second AI model, and a clean replay of
the shipped script. Second round, on the revision: a re-review of everything that changed, a proof audit of the new
and rewritten proofs (with its own reruns and independent recomputations), and an audit of the new proofs by the
second model.

## Outcome

No reviewer in either round found a mathematical error in any main result, and none found a counterexample. The
proofs were checked line by line by the methodology reviewer, the devil's advocate and the second model, and every
cited theorem on which a proof depends was checked against its source (T. Zhang, Theorem 6.2 and Lemma 6.1; Lin–Zhang;
Tang–Zhang, Theorem 1.1; Pang's two-Gram family; Zeng–Liu–Ratnavelu, Lemma 3.1; Harremoës; Sakai–Iwata; Qiu,
Section 5; Li's transfer theorem). The requested changes concerned presentation for readers, positioning against
earlier work, several sentences of rigour, the verification script, and tractable extensions. One revision round
addressed them, including two new results; the second round found no failing result and led to the line-level
repairs listed at the end.

## Objections and how each was handled

| Objection | Disposition |
|---|---|
| The paper was hard to read for non-specialists: no plain account of the question, why it matters, what was known or what is new | New Section 1: the scalar triangle inequality and its failure for matrix moduli, Lee's question, the results of Lin–Zhang, Tang–Zhang, T. Zhang and Qiu, the failure below p = 2, a table of what was known, the results in words, the idea of the proof and a roadmap. All results are stated together in Section 2 before any proof; q and F_{p,d} are explained in words; every section opens with a sentence saying what it does |
| The method extends T. Zhang's p = 2 argument, and this was not credited plainly | The factorisation, the spectral reduction and the sharpness family are credited to Zhang's Theorem 6.2 (and its Lemma 6.1 and Step 3); the paper presents itself as the extension to 1 < p < 2. Pang's examples, Zeng–Liu–Ratnavelu's p = 3/2 factorisation, and Harremoës and Sakai–Iwata for the eigenvalue shape are credited where used |
| Zhang's fixed-dimension bound min(m,n)^{(p−1)/(2p)} was not compared | Stated and compared: the exact value is smaller by a factor tending to 2^{−1/p}; for m < n the paper notes that D_{p,n} can be weaker than known m-dependent bounds and gives the best bound it knows |
| Is rank one extremal when m < n? Three reviewers found 3 × 3 examples that beat the rank-one value | Turned into a theorem: Proposition 2.5 certifies, in exact rational and interval arithmetic, that two 3 × 3 matrices beat D_{p,2} at nine exponents from 11/10 to 17/10, so rank-one families do not solve Lee's problem there |
| What does the paper say about Qiu's dimension-free question? | Stated exactly: the rank-one dimension-free constant is D_{p,m}; for general rank only brackets are given |
| Missing citations (Lee 2010 and 2012, Lin–Zhang, the Bourin–Zhang survey, published versions of Tang–Zhang and Zhang, Thompson) | Added, from Crossref and arXiv records |
| Rigour: the second variation in the scalar lemma, the rescaling step in the rectangular Hölder equality case, the nonzero hypothesis in the rank-one equality corollary, uniform convergence as p → 2, the p = 3/2 radical, the slow asymptotics, the splitting observation | Each step written out (Lemma 3.1, Lemma 5.1, Corollary 5.3, Proposition 6.2, Example 6.1, Remark 6.3, Remark 4.1); the p = 3/2 radical is presented as an example credited to Zeng–Liu–Ratnavelu |
| The verification script used `assert`, wrote to fixed paths and lacked adversarial searches and negative controls | Rewritten: explicit checks, exit 1 on failure (also under `python -O`), an output-directory argument, a PASS field, adversarial BFGS optimisation for m ≥ n and m < n, and negative controls; a new figure script |
| Extension: can the gap between the rank-one constant and the old general bound be narrowed? | Proved: the best constant is log-convex in 1/p (Theorem 2.3), giving c_p(m) ≤ ((1+√m)/2)^{1−1/p} (Corollary 2.4), better than m^{(p−1)/(2p)} for every m ≥ 2; for Lee's problem at p = 3/2 the upper bound falls from 1.12247 to 1.0647523 |
| Extension: does the rank gap hold for every 1 < p < 2? | Attempted by local perturbation; only a heuristic criterion was obtained, and the numerics suggest the gap may vanish above some p* < 2. Recorded as an open problem, not claimed |

## Second round (re-review, proof audit, second-model audit)

No result fails. Repairs made in response:

- In the proof of the scalar lemma a factor c^{−1} was removed from one identity (the sign argument was unaffected).
- The lower bound quoted after Corollary 2.4 now reads 1.03641 (the rank-one value), with 1.036425 attributed to
  Proposition 2.5.
- The equality proof now says explicitly that D_{p,r} < D_{p,n} for r < n forces full rank; Remark 6.3 now limits the
  failure of rank-one extremisers to the cases actually certified.
- The certificate script checks the number of isolated eigenvalues, and its JSON now reports p-th roots computed in
  interval arithmetic with outward decimal rounding (previously some displayed decimals were rounded in the unsafe
  direction; the decisions themselves were always made in interval arithmetic).
- Notation: the analytic half-power is written Z^{ζ(w)/2}; the endpoint values D_{1,d} and D_{2,d} are defined;
  "for every n" corrected to "for every n ≥ 2"; interpolation antecedents in Qiu and Li are cited.

## Limits of this review

The review was carried out by AI systems working from the manuscript, the scripts and the cited sources. It is not
peer review. No proof-assistant formalisation was attempted; the computer-assisted proof trusts sympy's exact root
isolation and mpmath's interval arithmetic. The prior-art search is bounded; its record is `RESEARCH_GATES.json`.
