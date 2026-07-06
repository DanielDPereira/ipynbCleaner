# ipynbcleaner

[![PyPI Version](https://img.shields.io/pypi/v/ipynbcleaner.svg)](https://pypi.org/project/ipynbcleaner/)
[![Python Versions](https://img.shields.io/pypi/pyversions/ipynbcleaner.svg)](https://pypi.org/project/ipynbcleaner/)
[![License](https://img.shields.io/github/license/DanielDPereira/ipynbCleaner.svg)](https://github.com/DanielDPereira/ipynbCleaner/blob/main/LICENSE)
[![CI Status](https://github.com/DanielDPereira/ipynbCleaner/actions/workflows/ci.yml/badge.svg)](https://github.com/DanielDPereira/ipynbCleaner/actions)

`ipynbcleaner` is a lightweight, zero-dependency Python utility designed to strip noise, outputs, and metadata from Jupyter Notebooks (`.ipynb`). It is optimized for preparing notebooks for Large Language Model (LLM) context windows, clean Git version control diffs, and lightweight sharing.

By removing unnecessary metadata and attachments, and optional cell outputs, `ipynbcleaner` reduces file sizes drastically (often by 70% to 90% or more), saving LLM tokens and keeping your repositories tidy.

---

## Key Features

- ⚡ **Zero-Dependency**: Does not require `nbformat` or any other external library. It works purely with Python's built-in `json` module.
- 🧹 **Noisy Metadata Stripping**: Removes notebook-level, cell-level, and execution-level metadata by default.
- 📉 **Rich CLI Metrics**: Prints a clean, visual summary of the cleaning process, showing file size reduction percentage, a terminal progress bar, and notebook structure statistics.
- 💾 **Smart Output Options**: Keeps only the last output of code cells by default (allowing LLMs to see the result of execution), or strips all outputs entirely.
- 🐍 **Flexible API**: Easy to integrate directly into Python scripts or CI/CD pipelines.

---

## Installation

Install directly from [PyPI](https://pypi.org/project/ipynbcleaner/):

```bash
pip install ipynbcleaner
```

---

## Usage

### Command Line Interface (CLI)

```bash
# Clean a notebook (saves output to input_clean.ipynb by default)
ipynbcleaner notebook.ipynb

# Clean a notebook and specify the output destination
ipynbcleaner notebook.ipynb cleaned_output.ipynb

# Clean and strip all outputs entirely
ipynbcleaner notebook.ipynb --drop-outputs
```

#### CLI Options

- `input`: Path to the `.ipynb` notebook file to clean (Required).
- `output`: Optional path to save the cleaned notebook. Defaults to `[input_stem]_clean.ipynb`.
- `--drop-outputs`: Remove all code cell outputs entirely (replaces last-output-only default behavior).
- `--keep-execution-count`: Do not clear execution counts (e.g. `[1]`, `[2]`).
- `--keep-root-metadata`: Preserve notebook-level metadata.
- `--keep-cell-metadata`: Preserve individual cell metadata.
- `--keep-cell-ids`: Preserve cell IDs.
- `--keep-attachments`: Preserve cell attachments (markdown images, etc.).
- `--indent`: Specify JSON indentation level (defaults to `2`).

#### Example CLI Output

Whenever you clean a notebook using the CLI, a beautiful summary is printed in the terminal:

```text
Cleaning Summary:
--------------------------------------------------
File sizes:
  Original:  1.24 MB
  Cleaned:   143.52 KB
  Reduction: [██████████████████░░] 88.67% (-1.10 MB)

Notebook structure:
  Total cells:    32
  Code cells:     18
  Markdown cells: 14
  Lines of code:  247
--------------------------------------------------
Cleaned notebook saved to: notebook_clean.ipynb
```

---

### Python API

You can import and use `ipynbcleaner` in your own Python scripts:

```python
from ipynbcleaner import CleanOptions, clean_notebook_file

# Clean file using default options (retains the last output per code cell)
clean_notebook_file("raw_notebook.ipynb", "clean_notebook.ipynb")

# Clean file and drop all outputs
options = CleanOptions(keep_last_output=False)
clean_notebook_file("raw_notebook.ipynb", "clean_notebook.ipynb", options=options)
```

#### CleanOptions Reference

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `keep_last_output` | `bool` | `True` | Retains only the final output of code cells. If `False`, all outputs are stripped. |
| `keep_execution_count` | `bool` | `False` | Preserves code execution counters. |
| `keep_root_metadata` | `bool` | `False` | Preserves notebook-level metadata. |
| `keep_cell_metadata` | `bool` | `False` | Preserves cell-level metadata. |
| `keep_cell_ids` | `bool` | `False` | Preserves cell IDs. |
| `keep_attachments` | `bool` | `False` | Preserves attachments (e.g., embedded markdown images). |
| `indent` | `int` | `2` | JSON indentation level for output. |

---

## Contributing

Contributions are welcome! Please feel free to open issues, submit pull requests, or request new features on our [GitHub Repository](https://github.com/DanielDPereira/ipynbCleaner).

1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'feat: add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
