"""Command-line interface for ipynbcleaner.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .cleaner import CleanOptions, NotebookCleanError, clean_notebook_file
from .metrics import calculate_metrics


def format_size(size_in_bytes: int) -> str:
    """Format bytes into human-readable size string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} TB"


def draw_reduction_bar(reduction_ratio: float, width: int = 20) -> str:
    """Draw a text-based progress bar representing the file reduction."""
    filled_length = int(round(width * reduction_ratio))
    filled_length = max(0, min(width, filled_length))
    
    encoding = (sys.stdout.encoding or 'ascii').lower()
    if 'utf' in encoding or encoding in ('cp65001', 'utf-8'):
        fill_char = '█'
        empty_char = '░'
    else:
        fill_char = '#'
        empty_char = '-'
        
    bar = fill_char * filled_length + empty_char * (width - filled_length)
    return f"[{bar}]"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ipynbcleaner",
        description="Clean Jupyter notebooks by removing noisy metadata and outputs.",
    )
    parser.add_argument("input", type=Path, help="Notebook .ipynb to clean.")
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        help="Destination file. Defaults to *_clean.ipynb.",
    )
    parser.add_argument(
        "--drop-outputs",
        action="store_true",
        help="Remove all outputs from code cells.",
    )
    parser.add_argument(
        "--keep-execution-count",
        action="store_true",
        help="Keep execution counts.",
    )
    parser.add_argument(
        "--keep-root-metadata",
        action="store_true",
        help="Preserve notebook-level metadata.",
    )
    parser.add_argument(
        "--keep-cell-metadata",
        action="store_true",
        help="Preserve per-cell metadata.",
    )
    parser.add_argument(
        "--keep-cell-ids",
        action="store_true",
        help="Preserve Jupyter cell IDs.",
    )
    parser.add_argument(
        "--keep-attachments",
        action="store_true",
        help="Preserve cell attachments.",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation level.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    options = CleanOptions(
        keep_last_output=not args.drop_outputs,
        keep_execution_count=args.keep_execution_count,
        keep_root_metadata=args.keep_root_metadata,
        keep_cell_metadata=args.keep_cell_metadata,
        keep_cell_ids=args.keep_cell_ids,
        keep_attachments=args.keep_attachments,
        indent=args.indent,
    )

    try:
        metrics_before = calculate_metrics(args.input)
    except Exception:
        metrics_before = {
            "total_cells": 0,
            "code_cells": 0,
            "markdown_cells": 0,
            "code_lines": 0,
            "file_size_bytes": 0,
        }

    try:
        output_path = clean_notebook_file(args.input, args.output, options)
    except FileNotFoundError:
        print(f"Error: file not found: {args.input}", file=sys.stderr)
        return 1
    except (json.JSONDecodeError, NotebookCleanError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    try:
        metrics_after = calculate_metrics(output_path)
    except Exception:
        metrics_after = {
            "total_cells": 0,
            "code_cells": 0,
            "markdown_cells": 0,
            "code_lines": 0,
            "file_size_bytes": 0,
        }

    original_size = metrics_before["file_size_bytes"]
    final_size = metrics_after["file_size_bytes"]

    if original_size > 0:
        reduction_bytes = original_size - final_size
        reduction_ratio = max(0.0, reduction_bytes / original_size)
        reduction_percentage = reduction_ratio * 100
    else:
        reduction_bytes = 0
        reduction_ratio = 0.0
        reduction_percentage = 0.0

    print("\nCleaning Summary:")
    print("-" * 50)
    print("File sizes:")
    print(f"  Original:  {format_size(original_size)}")
    print(f"  Cleaned:   {format_size(final_size)}")
    saved_str = format_size(abs(reduction_bytes))
    diff_prefix = "-" if reduction_bytes >= 0 else "+"
    print(f"  Reduction: {draw_reduction_bar(reduction_ratio)} {reduction_percentage:.2f}% ({diff_prefix}{saved_str})")
    print("\nNotebook structure:")
    print(f"  Total cells:    {metrics_after['total_cells']}")
    print(f"  Code cells:     {metrics_after['code_cells']}")
    print(f"  Markdown cells: {metrics_after['markdown_cells']}")
    print(f"  Lines of code:  {metrics_after['code_lines']}")
    print("-" * 50)
    print(f"Cleaned notebook saved to: {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
