# Replay receipt (release 0.1.0-candidate, 15 November 2026)

Clean replay before freezing, from fresh copies of the approved package (one copy per run, never the working
directory), on macOS 27.2.1 arm64 with CPython 3.12.11, numpy 2.3.5, scipy 1.17.0, sympy 1.14.0, mpmath 1.3.0 and
matplotlib 3.10.8, using the commands in `ENVIRONMENT.txt`, with the working directory outside the package and
bytecode writing disabled.

| Mode | `certify_rank_gap.py` | `verify_schatten.py` |
|---|---|---|
| normal | STATUS PASS at all nine exponents, exit 0; `rank_gap_certificate.json` byte-identical to the shipped file | status PASS, 128 checks, exit 0; `verification.json` byte-identical |
| `python -O` (assertions removed) | the same | the same |

`plot_bounds.py` regenerated `bounds.png` byte for byte; the regenerated `bounds.pdf` differs only in its embedded
creation date.

Certified values reproduced, for example: p = 3/2, quotient ≥ 1.036425091174 and D_{3/2,2} ≤ 1.036414357334;
p = 17/10, quotient ≥ 1.061667909089 and D_{17/10,2} ≤ 1.061667712714.

**Negative control.** In a copy of the package the p = 17/10 witness was relabelled as p = 9/5 (all other witnesses
removed). Under `python -O` the certificate printed `gap certified: False` and `STATUS FAIL` and exited with status 1,
so the certificate's checks stay active under optimisation and reject a witness that does not beat D_{p,2}.
`verify_schatten.py` contains its own negative controls (section N), which passed in both modes.

The only later changes to the package are text and metadata: the version and DOI line on the paper's title page; the
PDF rebuilt with three pdflatex passes (16 pages, text otherwise unchanged); and the release files (`README.md`,
`AI_INDEX.md`, `REVIEW_SUMMARY.md`, `RESEARCH_GATES.json`, `refs.bib`, `LICENSE.md`, `CITATION.cff`, `.zenodo.json`,
`ENVIRONMENT.txt`, this receipt, the CI workflow and `MANIFEST.sha256`). The scripts, witnesses, recorded outputs and
figure are byte-identical to the replayed copies, so the replay was not repeated after those edits. GitHub CI reruns
the certificate and the checks on Linux in both modes.

This receipt records execution only. Proposition 2.5 is a computer-assisted proof that rests on the certificate; all
other results rest on the written proofs in the paper, which the numerical checks supplement.
