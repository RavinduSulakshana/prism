# WRITER_BRIEF — shared conventions for every chapter writer

The master specification is `/Users/senul/Downloads/Ravindu/MEMORY.md` (read ALL of it first; it wins over
`DESIGN_SPEC.md`, `AGENT_BRIEF.md` and the old drafts). This file fixes the cross-chapter conventions so that
chapters written in parallel agree with each other. **Do not change anything defined here.**

## 1. Files and ownership
| Writer | Owns (only edit these) | Bib file |
|---|---|---|
| W1 | `chapters/01_introduction.tex` | `refs/ch1.bib` |
| W2 | `chapters/02_literature_review.tex` | `refs/ch2.bib` |
| W3 | `chapters/03_methodology.tex`, `appendices/F_drone_log.tex` | `refs/ch3.bib` |
| W4 | `chapters/04_srs.tex` | `refs/ch4.bib` |
| W5 | `chapters/05_implementation.tex`, `appendices/B_parameters.tex`, `appendices/D_code.tex`, `appendices/E_phases.tex` | `refs/ch5.bib` |
| W6 | `chapters/06_testing_evaluation.tex`, `appendices/C_tests.tex` | `refs/ch6.bib` |
| W7 | `chapters/07_concluding_remarks.tex`, `appendices/G_meetings.tex` | `refs/ch7.bib` |
| lead | `main.tex`, `preamble.tex`, front matter, abbreviations, `appendices/A_letters.tex`, `references.bib` | — |

- **Never edit** `preamble.tex`, `main.tex`, `references.bib`, another writer's files, or the abbreviations list.
  If you need a package or macro, define it locally at the top of your chapter only if harmless, and report it.
- Old drafts (reuse good prose, but they are WRONG on phasing — they assume 4-arm split phasing and a 120 s
  cycle): `chapters/old_drafts/`. The correct plan is MEMORY §5 (φ1 bypass through 21 s, φ2 bypass right 8 s,
  φ3 cross through 15 s, φ4 cross right 14 s; 3 s amber + 2 s all-red; cycle 78 s; left turns free on slip lanes).
- Study-site image: `figures/junction_clean.png` (2000×1111). Never use the annotated image.

## 2. Citations
- Existing keys: `references.bib` (63 entries; read it). Cite with `\cite{key}` (IEEE numeric).
- New references go ONLY in your own `refs/chN.bib`. **Every new reference must be verified on the web**
  (WebSearch/WebFetch: title, authors, venue, year, volume/pages or DOI). Never invent. Prefer 2021–2026.
- Before adding, grep `references.bib refs/*.bib` for the same title to avoid duplicates; if another writer
  already added it, cite their key. Make keys `firstauthorYEARword` (e.g. `wei2021recent`).

## 3. Numbers
- Every measured/experimental/observed/estimated number → `\est{...}` (yellow). Design parameters chosen by
  the author (G_min = 10 s, θ = 0.25, R = 75 m, γ, δ, κ, seeds, step length, etc.) are NOT wrapped.
- Never put `\est` inside math mode. Write `\est{$-23.2\%$}` or `\est{104.7~s}`.
- In pgfplots coordinates you cannot use `\est`; put `% PLACEHOLDER DATA` on the line above instead, and wrap
  the numbers in the surrounding text/table.
- Use ONLY the numbers in MEMORY §5–§13. If you genuinely need a number not given there (e.g. number of unit
  tests), make it plausible and consistent, wrap it in `\est{}`, and list it in your final report.

## 4. Formatting rules (preamble already implements the styling — just use standard commands)
- `\chapter{Title in Title Case}` (rendered as bold caps automatically), `\section{Sentence case}`,
  `\subsection{Sentence case}`, `\subsubsection{...}`. No deeper than subsubsection except `\paragraph`.
- Tables: `\begin{table}[htbp]\centering\caption{...}\label{tab:...}` **caption BEFORE the tabular**; booktabs
  rules; **no cell shading/colour**. Figures: caption AFTER content. Use `[htbp]`, not `[H]` unless needed.
- Long tables: `longtable` with caption at top.
- Pseudocode: `algorithm2e` (`\begin{algorithm}[htbp] ... \caption{...}\label{alg:...}\end{algorithm}`).
- Code: `\begin{lstlisting}[style=py,caption={...},label={lst:...}]`.
- Image placeholders: `\placeholder[0.85\textwidth]{6cm}{Description of what to insert}` inside a figure.
- Macros: `\prism{}`, `\vls{}`, `\dtx{}`, `\sumo{}`. Phases in maths: `$\phi_1$`…`$\phi_4$`.
- Expand every abbreviation at its first use **in your chapter**, e.g. "Passenger Car Unit (PCU)". Report any
  abbreviation you use that is not already in `chapters/00_abbreviations.tex`.
- Diagrams in TikZ (keep them compact, fit within `\textwidth`; use `\resizebox{\textwidth}{!}{...}` if needed).
  Black/grey/white palette (light fills like `black!5` are fine for diagram boxes; not in tables).

## 5. Fixed labels (create the ones in your chapter; you may `\cref` any of them)
- Chapters: `ch:intro`, `ch:lit`, `ch:method`, `ch:srs`, `ch:impl`, `ch:eval`, `ch:conc`.
- Appendices: `app:letters`, `app:params`, `app:tests`, `app:code`, `app:phases`, `app:drone`, `app:meetings`.
- Ch1: `sec:intro-problem`, `sec:intro-rq`, `sec:intro-objectives`, `sec:intro-scope`, `fig:intro-site`,
  `fig:intro-richpicture`, `tab:intro-hardware`, `tab:intro-software`, `tab:intro-scope`.
- Ch2: `sec:lit-existing`, `sec:lit-algorithms`, `sec:lit-design`, `sec:lit-reflection`, `fig:lit-conceptmap`,
  `tab:lit-systems` (comparison of existing systems).
- Ch3: `sec:method-paradigm`, `sec:method-strategy`, `sec:method-workflow`, `sec:method-pm`,
  `sec:method-ethics`, `fig:method-gantt`, `tab:method-workflow`.
- Ch4: `sec:srs-stakeholders`, `sec:srs-operationalisation`, `sec:srs-usecase`, `sec:srs-class`,
  `sec:srs-activity`, `sec:srs-sequence`, `sec:srs-arch`, `sec:srs-requirements`, `fig:srs-onion`,
  `fig:srs-usecase`, `fig:srs-class`, `fig:srs-activity`, `fig:srs-seq-dtx`, `fig:srs-seq-control`,
  `fig:srs-seq-experiment`, `fig:srs-arch`, `tab:srs-fr`, `tab:srs-nfr`.
- Ch5: `sec:impl-dtx`, `sec:impl-sumo`, `sec:impl-vls`, `sec:impl-prism`, `sec:impl-baselines`,
  `sec:impl-tech`, `sec:impl-key`, `alg:dtx`, `alg:vls`, `alg:prism`, `eq:pressure`, `eq:phase-pressure`,
  `eq:urgency`, `eq:score`, `eq:greq`, `fig:impl-prism-flow`.
- Ch6: `sec:eval-plan`, `sec:eval-nonfunctional`, `sec:eval-functional`, `sec:eval-workflow`, `sec:eval-mock`,
  `sec:eval-dtx`, `sec:eval-calibration`, `sec:eval-results`, `sec:eval-sensitivity`, `sec:eval-review`,
  `tab:eval-wait`.
- Ch7: `sec:conc-objectives`, `sec:conc-problems`, `sec:conc-future`.

## 6. Shared content (use verbatim; do not redefine)
**Research question (RQ):** *How can a LiDAR-driven, PCU-weighted, pressure-based adaptive signal controller,
calibrated with drone-observed heterogeneous traffic, reduce the average waiting time of road users at the
Maviththara junction compared with the existing fixed-time signal plan?*
- SRQ1: What are the demand, composition, turning and waiting characteristics of traffic at the Maviththara
  junction, and how can they be extracted reliably from nadir drone video?
- SRQ2: How can a purely mathematical control law account for heterogeneous vehicle classes, fairness between
  phases and imperfect LiDAR sensing?
- SRQ3: How does the proposed controller perform against fixed-time, actuated and Webster-optimised control,
  and how sensitive is it to sensor noise and to its own parameters?

**Aim:** To design, implement and evaluate a LiDAR-driven, PCU-weighted, pressure-based adaptive traffic signal
controller (PRISM) that reduces the waiting time of all road users at the Maviththara junction, using a SUMO
model calibrated with drone-observed Sri Lankan traffic.

**Objectives (IDs O1–O7):**
- O1 — To identify the operational problems of the Maviththara junction and the needs of its stakeholders
  through literature, observation and discussion with the Piliyandala Traffic Police and the RDA.
- O2 — To analyse existing adaptive signal control systems, control algorithms, sensing technologies and
  simulation tools critically, and to identify the research gap.
- O3 — To design and develop a drone-video trajectory extraction pipeline (DTX) that measures demand,
  composition, turning ratios, saturation flow and per-vehicle waiting time.
- O4 — To develop a SUMO model of the junction, first verified with mock demand and then calibrated and
  validated with the drone-extracted data.
- O5 — To design and implement a Virtual LiDAR Sensor (VLS) that reproduces realistic LiDAR noise, dropout,
  occlusion and size-class confusion.
- O6 — To design and implement the PRISM control algorithm with guaranteed safety, bounded fairness and
  explainable decisions, using mathematics only (no machine learning in control).
- O7 — To evaluate PRISM against fixed-time (B1), actuated (B2) and Webster-optimised (B3) control and an
  oracle-sensor variant (PRISM-GT), with statistical testing and sensitivity analysis.

**Functional requirements (IDs; priority = MoSCoW):**
FR01 Stabilise drone video against hover drift (M) · FR02 Detect the seven vehicle classes (M) · FR03 Track
vehicles with persistent IDs (M) · FR04 Convert pixel tracks to metric ground coordinates (M) · FR05 Compute
per-vehicle waiting time and control delay (M) · FR06 Derive flows, turning ratios, saturation flow and export
SUMO route files and an observed-KPI CSV (M) · FR07 Provide a SUMO network with 2+2 lanes per arm, give-way slip
lanes and a 4-phase signal (M) · FR08 Generate a noisy LiDAR object list every 1 s (M) · FR09 Track and map-match
LiDAR objects to approaches/lanes (M) · FR10 Compute movement/phase pressures and select phases (M) · FR11 Enforce
G_min, G_max, amber and all-red (M) · FR12 Enforce the starvation cap T_starve (M) · FR13 Fall back to the
observed fixed-time plan on sensor failure (S) · FR14 Apply the spillback guard (S) · FR15 Run baselines B1–B3 and
PRISM-GT (M) · FR16 Run batch experiments over seeds and export KPIs (M) · FR17 Perform statistical tests and
produce plots (S) · FR18 Visualise runs in SUMO-GUI with phase/decision overlays (C) · FR19 Emergency-vehicle
pre-emption (W — future work) · FR20 Web dashboard (W — results shown through SUMO-GUI only).

**Non-functional requirements:** NFR01 Performance — decision ≤ 10 ms per step (M) · NFR02 Safety — never
conflicting greens, always full intergreen (M) · NFR03 Robustness — graceful degradation under sensor noise and
dropout (M) · NFR04 Explainability — every decision logged with its reason and scores (S) · NFR05 Reproducibility —
fixed seeds, versioned configs (M) · NFR06 Scalability/efficiency — one simulated hour in ≤ 3 min wall clock (S) ·
NFR07 Privacy — no personally identifiable data stored (M) · NFR08 Portability — controller consumes only a
sensor-agnostic object list (S) · NFR09 Maintainability — modular code with automated tests (S).

**Test cases:** IDs `TC01`–`TC10` appear in Chapter 6 (W6 decides their content); further cases `TC11`+ go in
Appendix C. Each test case links to FR/NFR IDs above.

**Baselines:** B1 observed fixed-time (78 s), B2 SUMO actuated, B3 Webster-optimised fixed-time, PRISM-GT oracle.
**Seeds:** tuning 1–5, evaluation 6–15. Warm-up 300 s + 3600 s measured. Step 0.5 s; decision every 1 s.

## 7. Style
Formal British English; "this research", "the author"; past tense as if built and evaluated; critical,
justified, Sri Lankan context throughout; no mention of ChatGPT/LLMs/AI writing tools. AI is used only for
vehicle detection (YOLOv8); the controller is pure mathematics.

## 8. Test compile (do this before finishing; fix all errors in your files)
Create `report/_test_chN.tex` (N = your chapter number):
```latex
\documentclass[12pt,a4paper,oneside]{report}
\input{preamble}
\begin{document}
\setcounter{chapter}{N-1}   % write the actual number, e.g. 3 for chapter 4
\input{chapters/<your file>}
% appendix writers: \appendix \input{appendices/<file>}
\bibliographystyle{IEEEtran}\bibliography{references,refs/ch1,refs/ch2,refs/ch3,refs/ch4,refs/ch5,refs/ch6,refs/ch7}
\end{document}
```
Run from `report/`: `nix shell nixpkgs#tectonic -c tectonic -X compile _test_chN.tex --outdir _build_chN`
Undefined cross-references to other chapters are expected; LaTeX errors are not. Optionally render pages
(`nix shell nixpkgs#poppler-utils -c pdftoppm -r 50 -png -f 1 -l 5 _build_chN/_test_chN.pdf /tmp/chN`) and
look at diagrams to make sure they fit. **Delete `_test_chN.tex` and `_build_chN/` when done.**
Word count: `python3 tools/wordcount.py chapters/<file>` (body prose only).

## 9. Final report (your last message)
≤ 250 words: file(s) written, body word count, new bib keys added, any new `\est` numbers you invented (value +
meaning), abbreviations used that are missing from the list, any cross-chapter assumption others must match.
