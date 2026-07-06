import json
from pathlib import Path
from typing import Dict, Any

def calculate_metrics(notebook_path: Path | str) -> Dict[str, Any]:
    """Calculate basic metrics for a Jupyter notebook.

    Parameters
    ----------
    notebook_path: Path | str
        Path to the notebook file.

    Returns
    -------
    dict
        Dictionary containing metrics such as number of cells, code lines, markdown cells, and file size.
    """
    path = Path(notebook_path)
    
    # Handle missing or invalid file
    if not path.exists():
        return {
            "total_cells": 0,
            "code_cells": 0,
            "markdown_cells": 0,
            "code_lines": 0,
            "file_size_bytes": 0,
        }

    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception:
        return {
            "total_cells": 0,
            "code_cells": 0,
            "markdown_cells": 0,
            "code_lines": 0,
            "file_size_bytes": path.stat().st_size,
        }

    cells = data.get("cells", []) if isinstance(data, dict) else []
    total_cells = len(cells)
    code_cells = 0
    markdown_cells = 0
    code_lines = 0

    for cell in cells:
        if not isinstance(cell, dict):
            continue
        
        cell_type = cell.get("cell_type", "")
        if cell_type == "code":
            code_cells += 1
            source = cell.get("source", "")
            if isinstance(source, list):
                source_str = "".join(source)
            else:
                source_str = str(source)
            
            if source_str:
                code_lines += source_str.count('\n') + 1
        elif cell_type == "markdown":
            markdown_cells += 1

    file_size_bytes = path.stat().st_size

    return {
        "total_cells": total_cells,
        "code_cells": code_cells,
        "markdown_cells": markdown_cells,
        "code_lines": code_lines,
        "file_size_bytes": file_size_bytes,
    }
