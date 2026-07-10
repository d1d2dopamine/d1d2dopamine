<h1 align="center">d1d2dopamine</h1>
<p align="center"><i>Independent researcher — exploratory computational analysis of ADHD behavioral heterogeneity</i></p>

<p align="center">
  <img src="https://img.shields.io/badge/status-exploratory-orange" alt="status">
  <img src="https://img.shields.io/badge/peer--reviewed-no-red" alt="not peer reviewed">
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="license">
  <img src="https://img.shields.io/badge/python-3.x-blue" alt="python">
</p>

---

> Most of what's here replicates something already known in the ADHD literature. The one thing I can genuinely offer is a clean, honest account of what didn't hold up — including my own early mistakes.

### About

I'm an independent, self-taught researcher exploring how ADHD presents differently across individuals, using open datasets and reproducible code. I am not a professional neuroscientist or academic — this is unaffiliated, independent work, shared openly for scrutiny and reuse.

My interest: whether impulsivity on attention tasks differs consistently between subgroups of people with ADHD — tested against real data rather than assumed.

### Findings so far (short version — full detail in the repo)

- A subgroup of ADHD participants shows significantly higher commission-error rates than clean, non-ADHD controls — significant in one open dataset after correction, a consistent but non-significant trend in a second.
- A hypothesized difference in *how that impulsivity changes over the course of a task* was tested directly with a mixed model and was **not supported** (p = 0.847). Reporting that openly rather than leaving it out.
- No mechanism — dopaminergic, physiological, or otherwise — has been tested or confirmed. "Subtypes" below describes a statistical clustering result, not a validated biological category.

<p align="center">
  <img src="balladeer_impulsivity_by_subtype.png" width="440" alt="Impulsivity by subtype, BALLADEER dataset">
  <img src="balladeer_accuracy_by_subtype.png" width="440" alt="Accuracy by subtype, BALLADEER dataset">
</p>

<p align="center"><sub>Descriptive plots of the clustering used — not evidence of separate neural mechanisms, since mechanism was never measured.</sub></p>

<p align="center">
  <img src="balladeer_eda_change_by_cohort.png" width="500" alt="Skin conductance change by cohort and subtype">
</p>

<p align="center"><sub>The physiological angle that didn't pan out: no clear pattern distinguishing subtypes in skin-conductance change. Shown here rather than quietly dropped.</sub></p>

### Methods

Nearest-anchor clustering (z-scaled Euclidean distance), Mann-Whitney U with Bonferroni correction, label-permutation testing, and mixed-effects modeling (`commission ~ block × cluster`) for within-task dynamics. Known limitations — partial circularity between clustering variables and tested outcomes, small subgroup sizes, no third independent replication yet — are documented in full in the repo.

### Repository

**[the-Allosteric-Sprint-hypothesis](https://github.com/d1d2dopamine/the-Allosteric-Sprint-hypothesis)** — full analysis, code, results (including what didn't work), and a complete log of the methodological corrections made along the way.

`Python` · `pandas` · `NumPy` · `SciPy` · `statsmodels` · `matplotlib`

### Contact

d1d2dopamine@gmail.com — open to methodological critique. Errors get logged, not hidden.
