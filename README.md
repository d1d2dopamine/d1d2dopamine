<h1 align="center">d1d2dopamine</h1>
<p align="center"><i>Independent researcher — exploratory computational analysis of ADHD behavioral heterogeneity</i></p>

<p align="center">
  <img src="https://img.shields.io/badge/status-exploratory-orange" alt="status">
  <img src="https://img.shields.io/badge/peer--reviewed-no-red" alt="not peer reviewed">
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="license">
  <img src="https://img.shields.io/badge/python-3.x-blue" alt="python">
</p>

---

> I built a hypothesis I was sure was going to be big. Most of it wasn't. This is the honest version — what held up, what didn't, and why I'm posting the failures too.

### About

Independent, self-taught. No lab, no institution, no degree — just open datasets, reproducible code, and a habit of trying to break my own results before someone else does.

The question: does impulsivity on attention tasks differ *consistently* between subgroups of people with ADHD — not assumed, tested.

### Scorecard

<p align="center">
  <img src="https://img.shields.io/badge/BALLADEER%20impulsivity-p%3D0.011%20✓-brightgreen" alt="balladeer significant">
  <img src="https://img.shields.io/badge/HYPERAKTIV%20trend-p%3D0.031%2C%20ns-yellow" alt="hyperaktiv trend">
  <img src="https://img.shields.io/badge/temporal%20dynamics-not%20supported-red" alt="temporal dynamics not supported">
  <img src="https://img.shields.io/badge/mechanism-untested-lightgrey" alt="mechanism untested">
</p>

- **Held up:** a subgroup of ADHD participants shows significantly higher commission-error rates than clean, non-ADHD controls — significant in BALLADEER after correction, a consistent but non-significant trend in HYPERAKTIV.
- **Didn't hold up:** the idea that this splits into two subtypes with *different trajectories over a task* (steady-but-impulsive vs. progressive fatigue). Tested directly with a mixed model — flat, p = 0.847. Posted here instead of quietly dropped.
- **Never claimed:** any dopaminergic or physiological mechanism. Untested is untested, not "probably true."

<table>
<tr>
<td width="50%"><img src="balladeer_impulsivity_by_subtype.png" alt="Impulsivity by subtype, BALLADEER dataset" width="100%"></td>
<td width="50%"><img src="balladeer_accuracy_by_subtype.png" alt="Accuracy by subtype, BALLADEER dataset" width="100%"></td>
</tr>
</table>

<p align="center"><sub>Descriptive plots of the clustering used — not evidence of separate neural mechanisms, since mechanism was never measured.</sub></p>

<p align="center">
  <img src="balladeer_eda_change_by_cohort.png" width="500" alt="Skin conductance change by cohort and subtype">
</p>

<p align="center"><sub>The physiological angle that didn't pan out: no clear pattern distinguishing subtypes in skin-conductance change. Shown here rather than quietly dropped.</sub></p>

### Methods

Nearest-anchor clustering (z-scaled Euclidean distance), Mann-Whitney U with Bonferroni correction, label-permutation testing, mixed-effects modeling (`commission ~ block × cluster`) for within-task dynamics. Full limitations — partial circularity between clustering variables and tested outcomes, small subgroup sizes, no third independent replication yet — documented in the repo, not buried in a footnote.

### Repository

**[the-Allosteric-Sprint-hypothesis](https://github.com/d1d2dopamine/the-Allosteric-Sprint-hypothesis)** — full analysis, code, results including what didn't work, and a complete log of every correction made along the way.

`Python` · `pandas` · `NumPy` · `SciPy` · `statsmodels` · `matplotlib`

### Contact

d1d2dopamine@gmail.com — open to methodological critique. Errors get logged, not hidden.
