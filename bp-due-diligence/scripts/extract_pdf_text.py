#!/usr/bin/env python3
"""Extract text from one or more PDF files for BP due diligence."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def safe_name(path: Path) -> str:
    stem = re.sub(r"[^\w.\-\u4e00-\u9fff]+", "_", path.stem, flags=re.UNICODE).strip("_")
    return f"{stem or 'document'}.txt"


def extract_pdf(pdf_path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency: pypdf. Use the Codex bundled Python runtime when available, "
            "or install pypdf in the active Python environment."
        ) from exc

    reader = PdfReader(str(pdf_path))
    chunks: list[str] = [f"SOURCE: {pdf_path.name}", f"PAGES: {len(reader.pages)}", ""]
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        chunks.append(f"\n--- PAGE {i} ---\n{text.strip()}\n")
    return "\n".join(chunks).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdfs", nargs="+", help="PDF files to extract")
    parser.add_argument("--out-dir", default="reports/extracted", help="Output directory")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for item in args.pdfs:
        pdf_path = Path(item).expanduser().resolve()
        if not pdf_path.exists():
            print(f"[ERROR] Missing PDF: {pdf_path}", file=sys.stderr)
            return 2
        output = out_dir / safe_name(pdf_path)
        output.write_text(extract_pdf(pdf_path), encoding="utf-8")
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
