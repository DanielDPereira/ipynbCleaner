"""Core notebook cleaning utilities."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


class NotebookCleanError(ValueError):
    """Raised when the notebook structure is invalid."""


@dataclass(slots=True)
class CleanOptions:
    """Configuration for notebook cleaning."""

    keep_last_output: bool = True
    keep_execution_count: bool = False
    keep_root_metadata: bool = False
    keep_cell_metadata: bool = False
    keep_cell_ids: bool = False
    keep_attachments: bool = False
    indent: int = 2


def _as_mapping(value: Any, error_message: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise NotebookCleanError(error_message)
    return value


def _clean_cell(cell: Any, options: CleanOptions) -> dict[str, Any]:
    cell_data = _as_mapping(cell, "Each cell must be a JSON object.")
    cell_type = cell_data.get("cell_type", "")

    cleaned_cell: dict[str, Any] = {
        "cell_type": cell_type,
        "metadata": deepcopy(cell_data.get("metadata", {})) if options.keep_cell_metadata else {},
        "source": cell_data.get("source", []),
    }

    if options.keep_cell_ids and "id" in cell_data:
        cleaned_cell["id"] = cell_data["id"]

    if cell_type == "code":
        cleaned_cell["execution_count"] = (
            cell_data.get("execution_count") if options.keep_execution_count else None
        )

        outputs = cell_data.get("outputs", [])
        if options.keep_last_output and isinstance(outputs, list) and outputs:
            cleaned_cell["outputs"] = [deepcopy(outputs[-1])]
        else:
            cleaned_cell["outputs"] = []
    else:
        if options.keep_attachments and "attachments" in cell_data:
            cleaned_cell["attachments"] = deepcopy(cell_data["attachments"])

    return cleaned_cell


def clean_notebook(notebook: Any, options: CleanOptions | None = None) -> dict[str, Any]:
    """Return a cleaned notebook dictionary."""

    notebook_data = _as_mapping(notebook, "Notebook must be a JSON object.")
    config = options or CleanOptions()

    cleaned_notebook: dict[str, Any] = {
        "nbformat": notebook_data.get("nbformat", 4),
        "nbformat_minor": notebook_data.get("nbformat_minor", 0),
        "metadata": deepcopy(notebook_data.get("metadata", {})) if config.keep_root_metadata else {},
        "cells": [],
    }

    cells = notebook_data.get("cells", [])
    if not isinstance(cells, list):
        raise NotebookCleanError("Notebook cells must be a list.")

    for cell in cells:
        cleaned_notebook["cells"].append(_clean_cell(cell, config))

    return cleaned_notebook


def _default_output_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}_clean{input_path.suffix}")


def load_notebook(input_path: Path | str) -> dict[str, Any]:
    path = Path(input_path)
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_notebook(notebook: dict[str, Any], output_path: Path | str, indent: int = 2) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(notebook, handle, indent=indent, ensure_ascii=False)
        handle.write("\n")
    return path


def clean_notebook_file(
    input_path: Path | str,
    output_path: Path | str | None = None,
    options: CleanOptions | None = None,
) -> Path:
    """Clean a notebook file and return the written output path."""

    config = options or CleanOptions()
    input_file = Path(input_path)
    destination = Path(output_path) if output_path is not None else _default_output_path(input_file)

    cleaned = clean_notebook(load_notebook(input_file), config)
    return save_notebook(cleaned, destination, indent=config.indent)