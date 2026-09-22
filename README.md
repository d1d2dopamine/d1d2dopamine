<p align="center">
  <img src="./bannerforreadme.png" alt="Profile banner" width="100%">
</p>

# d1d2dopamine

I build small software tools and run open research around learning, attention, sleep and repeated measurements.

Most of the code in these repositories is written with AI models. My part is usually the problem, the direction and the decisions about what the project should actually do. I use AI for implementation, research, analysis, review and sometimes for technical decisions when I do not know the area well enough yet. I still inspect the result, test the important parts and decide what gets published.

[Website](https://d1d2dopamine.is-a.dev/) ·
[Email](mailto:d1d2dopamine@gmail.com) ·
[@d1d2dopamine on X](https://x.com/d1d2dopamine)

<!-- STATS:START -->
![public repos](https://img.shields.io/badge/public_repos-10-3a3a3a?style=flat-square) ![followers](https://img.shields.io/badge/followers-2-3a3a3a?style=flat-square) ![longest streak](https://img.shields.io/badge/longest_streak-18d-3a3a3a?style=flat-square) ![last commit](https://img.shields.io/badge/last_commit-2026--09--22-3a3a3a?style=flat-square)
<!-- STATS:END -->

## Projects

| Project | What it is |
| --- | --- |
| [ikna](https://github.com/d1d2dopamine/ikna) | A language-learning app built around the idea that studying should take attention, not administration. It learns phrases in context, uses FSRS-6 and controls how much new material enters the day. |
| [vespian](https://github.com/d1d2dopamine/vespian) | A local sleep-onset forecasting project. Instead of telling you when you should sleep, it estimates when sleep is likely and reports how uncertain that estimate is. |
| [allostatic-sprint-hypothesis](https://github.com/d1d2dopamine/allostatic-sprint-hypothesis) | An exploratory open-data project testing whether ADHD-related task performance is better described by instability than by uniform slowing or stable subtypes. Positive and null results stay together. |
| [MVS Analyzer](https://github.com/d1d2dopamine/MVS-analyzer) | A reproducible analysis engine for repeated measurements. It compares summary metrics through simulation and keeps the calibration, diagnostics and run metadata needed to inspect the result later. Current development is CLI/Python-first. |
| [gitctap!](https://github.com/d1d2dopamine/Gitctap) | A small Git helper for publishing one local repository to several forges with one command. Git still does the actual work. |
| [trial3lib](https://github.com/d1d2dopamine/trial3lib) | A Compose design system for Android that deliberately avoids Material geometry, elevation and ripple in favor of simple rectangular, high-contrast interfaces. |

## How I work

A lot of projects start with something that annoys me enough to investigate it. Sometimes the result is an app, sometimes a statistical tool, sometimes just a hypothesis that survives long enough to test.

I try to keep the same rule across all of them: the implementation can be complicated, but the claim should stay narrow. If a result is null, inconclusive or breaks the original idea, I would rather keep that visible than rewrite the project around the result I wanted.

For software, I prefer local data, explicit network access and documented limitations. For research, I keep seeds, checksums, validation code and the assumptions that matter for reproducing the analysis.

## AI and authorship

The repositories are AI-assisted by design. In practice, AI often writes most or all of the code, drafts documentation, searches technical options and helps analyze results.

That does not mean every implementation choice started with me. Some decisions are mine, some come from the model, and some are mixed. What I try to own is the direction of the project, the problem being solved, the evidence I accept and the final decision to keep, change or throw something away.

Because of that, I do not use the code itself as evidence that I personally know every language or framework in these repositories. The useful question for me is whether I can understand the result well enough to test it, notice when it is wrong and keep the project moving in a sensible direction.

## A few rules I try to keep

- Null and inconclusive results stay next to positive ones.
- Known gaps are written down instead of being hidden behind a finished-looking interface.
- Network access should have a reason. Several projects work fully locally.
- Reproducibility matters more than making an analysis look certain.
- A project does not need to solve a problem for everyone. Solving one concrete problem well is enough.

Repository documentation is usually in English, and some projects also include Russian documentation or interfaces. Research repositories are exploratory unless they explicitly say otherwise, and health-related projects are not diagnostic or medical tools.
