#!/usr/bin/env python3
"""Approximate body-prose word count of LaTeX chapter files.

Excludes comments, floats (figure/table), tikz, pgfplots, algorithms, listings,
equations and tabulars; strips commands but keeps their text arguments.
Usage: python3 tools/wordcount.py chapters/01_introduction.tex [...]
"""
import re
import sys

SKIP_ENVS = ["figure", "table", "tikzpicture", "axis", "algorithm", "lstlisting",
             "equation", "equation*", "align", "align*", "tabular", "tabularx",
             "longtable", "ganttchart", "landscape"]


def count(text):
    text = re.sub(r"(?<!\\)%.*", "", text)
    for env in SKIP_ENVS:
        e = re.escape(env)
        text = re.sub(r"\\begin\{" + e + r"\}.*?\\end\{" + e + r"\}", " ", text, flags=re.S)
    text = re.sub(r"\$[^$]*\$", " x ", text)
    text = re.sub(r"\\(label|ref|cref|Cref|cite|input|includegraphics|est)\b\*?(\[[^\]]*\])?\{([^}]*)\}",
                  lambda m: " x " if m.group(1) == "est" else " ", text)
    text = re.sub(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?", " ", text)
    text = re.sub(r"[{}\\~]", " ", text)
    return len([w for w in text.split() if re.search(r"[A-Za-z0-9]", w)])


total = 0
for path in sys.argv[1:]:
    n = count(open(path, encoding="utf-8").read())
    total += n
    print(f"{n:6d}  {path}")
if len(sys.argv) > 2:
    print(f"{total:6d}  TOTAL")
