"""Command-line interface for ipynbcleaner.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .cleaner import CleanOptions, NotebookCleanError, clean_notebook_file


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
        output_path = clean_notebook_file(args.input, args.output, options)
    except FileNotFoundError:
        print(f"Erro: arquivo não encontrado: {args.input}", file=sys.stderr)
        return 1
    except (json.JSONDecodeError, NotebookCleanError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1

    print(f"Notebook limpo salvo em: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
