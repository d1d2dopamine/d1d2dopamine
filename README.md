<p align="center">
  <img src="./banner5.jpeg" alt="Profile banner" width="100%">
</p>

# d1d2dopamine

I build software and run data analysis on attention, impulsivity and sleep:
two Android apps, one open-data study, one Windows desktop analysis app, one
Android design system and one Git command-line tool. Kotlin, C# and Python. The
apps work without required network access, and each repository states what is
not tested yet.

[Project notes](https://d1d2dopamine.github.io/) ·
[d1d2dopamine@gmail.com](mailto:d1d2dopamine@gmail.com) ·
[@d1d2dopamine on X](https://x.com/d1d2dopamine)

## Projects

| Project | What it does | Stack, license |
| --- | --- | --- |
| [ikna](https://github.com/d1d2dopamine/ikna) | Learns phrases in context, brings your Anki decks over and decides how much new material a day can carry | Kotlin, GPL-3.0 |
| [vespian](https://github.com/d1d2dopamine/vespian) | Predicts when you will fall asleep, not when you should | Kotlin, GPL-3.0 |
| [allostatic-sprint-hypothesis](https://github.com/d1d2dopamine/allostatic-sprint-hypothesis) | Tests one ADHD hypothesis on four public datasets, nulls included | Python, MIT |
| [MVS Analyzer](https://github.com/d1d2dopamine/MVS-analyzer) | Ranks ten metrics on your data by false alarms, power, robustness, repeatability and coverage before the real group comparison | C# / .NET 8, MIT |
| [Gitctap](https://github.com/d1d2dopamine/Gitctap) | Creates, pushes and compares one project across several Git forges | Python, MIT |
| [trial3lib](https://github.com/d1d2dopamine/trial3lib) | A non-Material Compose design system for rectangular, high-contrast Android interfaces | Kotlin / Jetpack Compose |

### ikna

Spaced repetition where the scheduler is allowed to say no.

- Your Anki decks come over: any `.apkg`, old export or current one, read on
  the phone itself. Each deck's language is worked out rather than asked for,
  cloze gaps and phrases inside sentences survive the crossing, and your answer
  history is replayed through the scheduler instead of being trusted as stored
  state. A card that cannot be rebuilt faithfully is refused and counted, never
  stored mangled.
- A load governor forecasts today's review cost from backlog, recent accuracy
  and missed days. It can refuse new material without cancelling the session,
  and the day's plan may only shrink.
- Answers are swipes: direction, distance and speed map to four grades, judged
  against a rolling window of your own previous answers.
- FSRS-6, all 21 weights, running separately per level (recognition, cloze,
  production) over a second, word-level memory layer. 20% same-day amnesty, no
  streaks, no visible backlog counter. The optimiser that fits those weights to
  your own log runs on the device, as an estimator only.
- Nothing about your learning leaves the phone. The only network feature is the
  update and catalogue check; switched off in Settings it opens no socket at
  all, and an import from Anki never touches the network. Reviews are an
  append-only log exported to `Documents/ikna/`; a restore replays every answer
  through the scheduler instead of trusting stored state.
- Android 10+. The signing key is committed deliberately so anyone can rebuild
  a comparable APK; `docs/KEYSTORE.md` explains that trade-off.

[Latest ikna release](https://github.com/d1d2dopamine/ikna/releases/latest)

### vespian

A sleep-onset forecast for delayed sleep phase, built for one documented
hardware setup.

- Two-process model (Borbély, 1982) driven by a particle filter over Health
  Connect sleep, stage and heart-rate records plus the phone's light sensor.
- The forecast declares its own precision from measured hit rate: exact time at
  75% or above, time plus range at 50-74%, range only below that.
- No server and no account. Room database on the device; raw heart rate and
  light are kept 90 days.
- Verified against a Xiaomi Smart Band 9 Active and a realme GT Neo 5, written
  up as a reference implementation with `HealthRepo.kt` as the porting entry
  point.
- Open gaps are listed rather than hidden: SpO2 is stored but unused, and the
  behavioural layer needs about 30 nights before it means anything.

### allostatic-sprint-hypothesis

The claim under test: in ADHD the measurable problem is variability of
reaction time rather than its average.

- ADHD Pupil, 28 off-medication ADHD against 22 controls, 10,720 trials:
  median RT −19.5 ms (p = 0.45), RT MAD +61.75 ms and IQR +99.63 ms (Holm
  p = 0.0088), accuracy −0.275 (Holm p = 0.0010). Dispersion moves, central
  tendency does not.
- UCLA CNP / OpenNeuro ds000030, 41 against 126: every primary endpoint
  non-significant, published as a substantive null.
- HYPERAKTIV and BALLADEER reached nominal p = 0.031 and p = 0.011, then were
  marked corrected-nonsignificant and task-specific rather than promoted.
- The two-subtype reading failed its own gates: `stable_two_cluster = False`
  after BIC, silhouette, minimum size and bootstrap stability checks.
- 5,000 label permutations, 2,000 bootstraps, fixed seed, checksum-verified
  downloads, no participant data redistributed.
  `python scripts/validator_core.py --self-test --json` re-runs the checks.
- AI-assisted development is disclosed in the repository. Not a diagnostic
  tool.

### MVS Analyzer

A Windows desktop app for choosing a summary metric before an analysis, or
checking that a conclusion does not depend on one lucky metric.

- Ten metrics over 2–10 independent groups. Calibration replays the actual rows
  in a null world and a planted-effect world, then measures false-alarm rate,
  power, robustness, split-half repeatability and interval coverage.
- The run uses Mann–Whitney *U* for two groups or Kruskal–Wallis *H* for three to
  ten, with Cliff's delta, a bootstrap interval, equivalence testing and MDE.
  Verdicts include difference, no difference, not enough data and not applicable.
- The MVS Score combines five measured components in a frozen, hashed formula.
  The candidate set is allowed to be empty when no metric clears the gates.
- Each run hashes its input and outputs in `run_manifest.json` and enters a
  hash-chained local journal. Audit checks modified, missing and hidden runs,
  formula changes, engine differences and unstable candidate sets offline.
- Pure .NET 8 and WinForms, zero NuGet dependencies, no accounts, telemetry or
  networking code. Windows 10+ x64. MIT.
- Independent groups only for now: paired and repeated-measures designs and
  Kruskal–Wallis post-hoc comparisons are listed as limitations.

### Gitctap

- `setup`, `create --on`, `push`, `status`, `check` across GitHub, Codeberg,
  GitLab, Gitea, Framagit, Salsa, Disroot, self-hosted instances and bare
  repositories on disk.
- No force push anywhere in the code, no delete refspec, no commits made on
  your behalf. A partial failure stays partial and exits 1.
- No tokens stored: environment variable, then the forge's own CLI, then a
  hidden one-time prompt. Config sits outside the repository in
  `~/.config/gitctap`, mode 0600.
- Every forge is also a plain Git remote, so `git push codeberg main` keeps
  working with or without the tool.
- One file, standard library only, Python 3.8+, 30 offline tests that use bare
  repositories as stand-in forges.

### trial3lib

A Compose design system for Android that deliberately does not use Material.

- No elevation, ripple, rounded corners or tonal surfaces. One-pixel lines,
  rectangular controls, geometry and contrast carry the interface instead.
- Twelve hand-authored palettes each ship in dark and light versions. Contrast
  tests cover both, including pure black OLED and paper-white conditions.
- The library depends on `compose.foundation` and nothing else. Material 3 is
  not a dependency, and a test asserts that its classes are not loadable.
- Tokens cover colour, fifteen typography slots, spacing, strokes, opacity and
  motion; reduced-motion behaviour follows the system setting.
- `dev.trial3lib.ui.compat` mirrors Material call signatures so an existing app
  can migrate by changing imports while the compatibility surface is counted.
- The reviewed public API contains 245 declarations. Design, test-signature and
  API-snapshot checks run without an Android SDK.

## How I work

- Null and inconclusive results stay in the repository next to the positive
  ones.
- Runs are reproducible: fixed seeds, checksummed inputs, self-tests committed
  alongside the analysis.
- Local by default. Network access is an explicit feature, not a default.
- Untested areas and known gaps are written down in the docs.

Repository documentation is written in English and Russian. The apps are not
medical devices and the analyses are not diagnostic tools.

<p align="center">
  <img src="./banner7.png" alt="Travis points upward" width="100%">
</p>
