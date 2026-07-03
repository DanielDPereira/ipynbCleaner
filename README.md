# ipynbCleaner

`ipynbcleaner` is a small Python utility for reducing the noise in Jupyter Notebook files before sharing them with other developers, storing them in version control, or sending them to LLMs.

It removes notebook-level metadata by default, strips cell metadata, clears execution counters, and keeps only the last output from code cells unless you choose to drop outputs entirely.

## Why this exists

Notebook files often carry a lot of extra data that is useful for interactive execution but not useful when the goal is to review code or feed the notebook to an LLM. That extra payload makes the file heavier and burns context budget quickly.

This project keeps the notebook structure intact while trimming the parts that usually add noise.

## Features

- Removes notebook-level metadata by default.
- Removes cell metadata, cell IDs, and attachments by default.
- Keeps code and markdown source intact.
- Keeps only the last code cell output by default.
- Can drop all outputs when needed.
- Exposes both a Python API and a CLI.

## Installation

From source:

```bash
pip install .
```

For development:

```bash
pip install -e .
```

## Usage

### CLI

```bash
ipynbcleaner notebook.ipynb
ipynbcleaner notebook.ipynb notebook_clean.ipynb
ipynbcleaner notebook.ipynb --drop-outputs
```

Available options:

- `--drop-outputs` removes every output from code cells.
- `--keep-execution-count` preserves execution counts.
- `--keep-root-metadata` preserves notebook-level metadata.
- `--keep-cell-metadata` preserves cell metadata.
- `--keep-cell-ids` preserves Jupyter cell IDs.
- `--keep-attachments` preserves markdown attachments.

### Python API

```python
from ipynbcleaner import CleanOptions, clean_notebook_file

clean_notebook_file("notebook.ipynb", options=CleanOptions(keep_last_output=True))
```

## Project status

This repository is now structured as a distributable Python package with a console script entry point and basic regression tests, so it is ready for iteration toward a PyPI release.
