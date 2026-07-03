import nbformat
from typing import Dict, Any

def calculate_metrics(notebook_path: str) -> Dict[str, Any]:
    """Calculate basic metrics for a Jupyter notebook.

    Parameters
    ----------
    notebook_path: str
        Path to the notebook file.

    Returns
    -------
    dict
        Dictionary containing metrics such as number of cells, code lines, markdown cells, etc.
    """
    nb = nbformat.read(notebook_path, as_version=nbformat.NO_CONVERT)
    total_cells = len(nb.cells)
    code_cells = sum(1 for cell in nb.cells if cell.cell_type == "code")
    markdown_cells = sum(1 for cell in nb.cells if cell.cell_type == "markdown")
    # Count lines of code in code cells
    code_lines = sum(cell.source.count('\n') + 1 for cell in nb.cells if cell.cell_type == "code")
    return {
        "total_cells": total_cells,
        "code_cells": code_cells,
        "markdown_cells": markdown_cells,
        "code_lines": code_lines,
    }
