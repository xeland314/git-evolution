# git-evolution

A blazingly fast, zero-config CLI tool to visualize your Git repository's code evolution by language over time. It parses your commit history and generates a beautiful, interactive stacked area chart embedded in a lightweight, standalone HTML report.

Built with Python and **`uv`**. This project is structured using the **Chain of Responsibility** design pattern for maximum maintainability.

---

## Features

* **High Performance:** Parses `git log` metrics using strict, non-regex string scanning for optimal CPU efficiency.
* **Interactive Visualization:** Generates a Plotly-driven, dark-themed stacked area chart (`git-evolution.html`) with unified hover tooltips.
* **Reliable on Small Repos:** The X axis range is computed explicitly instead of relying on Plotly's autorange, so repositories with just 1-2 commits still render a visible, correctly-scaled chart (autorange collapses to a sub-millisecond window on very small date spans).
* **Report Metadata:** Every generated report is stamped with the repository name, generation timestamp, and total commit count, pulled straight from `git`.
* **Polished Report Layout:** The HTML output ships with a dark-themed header/footer and a card-style container around the chart, not just a bare `<div>`.
* **Zero-Dependency Setup:** Leverages `uv` inline script metadata (PEP 723) to manage environments on the fly without polluting your system.
* **Standalone Binary:** Can be compiled into a single self-contained executable with PyInstaller (orchestrated through `uv`) — no Python or `uv` needed at runtime, and the HTML template ships embedded inside the binary.
* **Clean Architecture:** Built as an extensible execution pipeline (Fetch ➔ Parse ➔ Accumulate ➔ Plot ➔ Render).

---

## Prerequisites

You only need [uv](https://docs.astral.sh/uv/) installed on your machine. Everything else (Python interpreter, `plotly`) is resolved automatically.

---

## Usage

Run it from inside any Git repository you want to analyze:

```bash
uv run main.py
```

This produces `git-evolution.html` in the current directory — open it in any browser.

### Using the compiled binary

If you built the standalone executable (see below), no `uv`/Python setup is required at all:

```bash
./git-evolution
```

Just run it from inside the target repository; it works exactly the same way.

---

## Building a Standalone Binary

`build.sh` orchestrates a full PyInstaller build using `uv` for environment management — no manual `pip`/`venv` juggling required.

```bash
./build.sh
```

Under the hood it:

1. Creates an isolated build environment with `uv venv .venv-build`.
2. Installs `plotly` and `pyinstaller` into it with `uv pip install`.
3. Runs PyInstaller in `--onefile` mode, embedding `template.html` directly into the executable (resolved at runtime via `sys._MEIPASS`) and collecting all `plotly` submodules.

The resulting binary is written to `dist/git-evolution`. It is platform-specific — PyInstaller does not cross-compile, so build on each target OS (Linux, macOS, Windows) separately.

---

## Report Structure

Each generated report includes:

* **Header:** repository name, generation date/time, and total commits analyzed.
* **Chart:** a stacked area chart of cumulative lines of code per file extension over time, with zoom/pan controls and unified hover tooltips.
* **Footer:** attribution line.

---

## Repository Structure

```text
├── main.py                # Entry point; wires up and runs the handler chain
├── handler.py              # Abstract base class for the Chain of Responsibility pattern
├── evolution_context.py    # Shared state object passed through the pipeline
├── git_log_fetch.py        # [1/5] Fetches git log, repo name, and commit count
├── git_log_parse.py        # [2/5] Parses numstat output into per-extension, per-date deltas
├── metrics.py               # [3/5] Computes cumulative time series per extension
├── plot_generator.py       # [4/5] Builds the Plotly figure and fixes the small-dataset X axis range
├── html_renderer.py        # [5/5] Injects the figure and metadata into template.html
├── template.html            # HTML/CSS layout for the final report
├── build.sh                 # Builds a standalone binary via uv + PyInstaller
└── pyproject.toml           # Project metadata and dependencies
```

---

## How It Works

The pipeline runs as a sequential Chain of Responsibility, each handler enriching a shared `EvolutionContext`:

```
Fetch ➔ Parse ➔ Accumulate ➔ Plot ➔ Render
```

1. **Fetch** — runs `git log --numstat` plus `git rev-parse`/`git rev-list` to capture the raw log, repository name, and commit count.
2. **Parse** — scans the raw log line by line (no regex) to tally added/removed lines per file extension and date.
3. **Accumulate** — turns per-date deltas into a running cumulative total per extension.
4. **Plot** — builds a dark-themed Plotly stacked area chart, with an explicitly padded date range so the chart stays visible regardless of how few or how many commits exist.
5. **Render** — fills `template.html` with the chart and the repo's metadata, producing `git-evolution.html`.
