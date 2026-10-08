# Brief for every chapter writer

Project root: report/ (LaTeX, compiled with main.tex, report class, IEEEtran bibliography).
READ FIRST: report/DESIGN_SPEC.md (single source of truth: names, parameters, algorithms, ALL numbers) and
report/references.bib (ONLY cite keys that exist there, with \cite{key}; do not invent new references; if you truly need
a new one, it must be a real, well-known publication — add it to the END of references.bib in the same style, and tell me).

Context: BSc (Hons) Computer Science final-year dissertation (Sri Lanka, UGC degree) by P R S Perera (29243),
supervisor Ms. Hirushi Dilpriya. Total report target 15,000–18,000 words body text. Write in formal academic British English,
third person / "this research" / occasional "the author". Past tense, written as if the system has been built and evaluated
(the student is building it exactly to this spec). Do not mention ChatGPT/LLMs. AI is used ONLY for vehicle detection (YOLOv8);
the signal-control algorithm is purely mathematical — emphasise this.

PLACEHOLDER RULE (critical): every measured/experimental number (results, dataset sizes, accuracy, counts, observed timings,
observed demand, runtime, calibration error, etc.) MUST be wrapped as \est{...}, e.g. \est{18.8\%}, \est{47.9} s.
Design parameters chosen by the author (G_min = 10 s, gamma = 0.5, R = 75 m, ...) are NOT wrapped.
Never put \est inside math mode; if needed write \est{$-23.2\%$}. Use only numbers from DESIGN_SPEC.md; if you need a number
not in the spec, make it consistent with the spec and wrap it in \est{} and list it in your final reply.

LaTeX rules: available packages: amsmath, booktabs, tabularx, multirow, siunitx, algorithm2e (ruled,vlined,linesnumbered: use
\KwIn \KwOut \If{}{} \eIf{}{}{} \For{}{} \ForEach{}{} \While{}{} \Return, \caption, \label), tikz (arrows.meta, positioning,
shapes.geometric, fit, calc, backgrounds), pgfplots, subcaption, listings, cleveref (\cref), float, enumitem, xcolor.
Macros: \prism, \vls, \dtx, \sumo, \est{}. Escape % & _ # properly. Use \label{} prefixes: ch:, sec:, fig:, tab:, eq:, alg:.
Figures that need real images (drone frames, screenshots) -> use a framed placeholder:
\begin{figure}[H]\centering\fbox{\parbox[c][5cm][c]{0.85\textwidth}{\centering\textit{[Placeholder: describe image to insert]}}}\caption{..}\label{..}\end{figure}
Prefer TikZ/pgfplots for diagrams and charts you can draw yourself. Keep TikZ simple and robust (it must compile with tectonic).
Each chapter file starts with \chapter{Title}\label{ch:...}. No \documentclass, no \begin{document}.
Cross-reference other chapters with these labels (they will exist): ch:intro, ch:lit, ch:method, ch:design, ch:impl, ch:eval,
ch:conclusion; sec:dtx (design of extraction), sec:vls (design of virtual lidar), sec:prism (control algorithm design),
sec:results (results), sec:futurework, app:params (appendix parameter table), app:code (appendix code listings).
Word count: hit your target for body prose (tables/code do not count much). Be substantive — real technical depth, equations,
justifications of choices against alternatives, Sri Lankan context (heterogeneous traffic, motorcycles & three-wheelers filtering,
police manual control, Piliyandala bypass congestion) — not filler.
When finished, run: cd report && nix shell nixpkgs#tectonic -c tectonic -X compile main.tex  (other chapter files may be missing
while others work — if compile fails only because another chapter file is missing, create an empty stub ONLY if the file doesn't
exist, never overwrite another writer's file). Fix any errors in YOUR files. Report back: file(s) written, approximate word count
(use: detex-free estimate `sed 's/\\[a-zA-Z]*//g' file | wc -w`), and any new \est numbers you introduced.

NOTE: all chapter files already exist as "% stub". Overwrite ONLY the files assigned to you. Compile from the report/ directory
(absolute path: /Users/senul/Library/Application Support/Claude/scratch-workspaces/9e598295-bb80-4f69-a762-c7e68a7cc1cc/e8852f1b-4369-4c26-a9f5-e6fddfee3740/scratch-2026-10-04-842245/report). Several writers compile concurrently: if you get a weird file-lock/aux error, just retry.
