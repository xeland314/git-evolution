# git-evolution

A blazingly fast, zero-config CLI tool to visualize your Git repository's code evolution by language over time. It parses your commit history and generates a beautiful, interactive stacked area chart embedded in a lightweight, standalone HTML report.

Built with Python and **`uv`**. This project is structured using the **Chain of Responsibility** design pattern for maximum maintainability.

---

## Features

*   **High Performance:** Parses `git log` metrics using strict, non-regex string scanning for optimal CPU efficiency.
*   **Interactive Visualization:** Generates a Plotly-driven, dark-themed stacked area chart (`git-evolution.html`) with unified hover tooltips.
*   **Zero-Dependency Setup:** Leverages `uv` inline script metadata (PEP 723) to manage environments on the fly without polluting your system.
*   **Clean Architecture:** Built as an extensible execution pipeline (Fetch ➔ Parse ➔ Accumulate ➔ Plot ➔ Render).

---

## Prerequisites

You only need [uv](https://docs.astral.sh/uv/) installed on your machine.

---

## Repository Structure

The core tool relies on two files living in the same directory:

```text
├── main.py
|   ...
└── template.html    # The HTML layout template