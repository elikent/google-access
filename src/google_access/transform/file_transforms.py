from pathlib import Path
import logging
from typing import Iterable, Callable, Optional, Sequence
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PyPDF2.errors import PdfReadError

from google_access import report

# to do: change report() -> report() and make changes suggested by coach

logger = logging.getLogger(__name__)

def combine_pdfs(
    sources: Iterable[Path] | Path,
    output_file: Path,
    *,
    match: Optional[Callable[[Path], bool]] = None,
    patterns: Optional[Sequence[str]] = None,
    sort_key: Optional[Callable[[Path], object]] = None,
    dry_run: bool = False,
    verbose: bool = False
) -> list[Path]:
    """Combine PDFs into one file.

    Args:
        sources: A directory Path (to scan) or an iterable of Paths (files/dirs).
        output_file: Where to write the merged PDF.
        match: Optional predicate(Path)->bool to filter files.
        patterns: Optional list of glob patterns (e.g., ["*single*.pdf", "*2025*.pdf"]).
        sort_key: Optional key function to sort matched PDFs (default: by name).
        dry_run: If True, don't write output—just return matched files.

    Steps:
        1. normalizes sources to a list of paths to scan
        2. scans sources and extracts all pdfs. if p is a file and is not a pdf, warning is logged
        3. deduplicates list of pdfs
        4. filters by match if passed
        5. applies sort_by if passed. else, sorts alphabetically
        6. if dry_run, returns list of pdfs to be merged
        7. ensures output_path exists
        8. create merger object, append each pdf to merger object, write to output_path and close merger

    Returns:
        The list of PDF Paths that would be (or were) merged, in order.
    """



    # Normalize sources to a list of paths to scan
    if isinstance(sources, Path):   # if sources is a Path, put it in a list and store in scan_paths
        scan_paths = [sources]
    else:                           # else, just store in scan_paths
        scan_paths = list(sources)
    msg = f'{len(scan_paths)} paths passed to scan_paths'
    report(msg)

    # Collect candidate files
    pdfs: list[Path] = []   # create empty list of paths pdfs
    for p in scan_paths:
        if p.is_file() and p.suffix.lower() == ".pdf":     # if p is a file, add it to pdfs
            pdfs.append(p)
        elif p.is_file() and p.suffix.lower() != '.pdf':
            msg = f'{p} is not a pdf file. removed from pdf list'
            report(msg, 'warning')
        elif p.is_dir():    # if p is a directory, gather files in that directory
            if patterns:    # if patterns, gather only that match any of the patterns
                for pat in patterns:
                    pdfs.extend(p.glob(pat))
            else:
                it = p.glob("*.pdf")
                pdfs.extend(it)
        else:
            # silently skip non-existent
            continue
    msg = f'{len(pdfs)} pdfs found'
    report(msg)

    # Deduplicate & keep only files
    uniq = []
    seen = set()
    for f in pdfs:
        try:
            fp = f.resolve()
        except Exception:
            continue
        if fp.is_file() and fp not in seen:
            uniq.append(fp)
            seen.add(fp)
    uniq_count1 = len(uniq)
    msg = f'{uniq_count1} unique pdfs found'
    report(msg)

    # Apply predicate filter if provided
    if match:
        uniq = [p for p in uniq if match(p)]
        msg1 = f'{len(uniq)} pdfs after predicate filter'
        msg2 = f'{uniq_count1 - len(uniq)} pdfs removed by predicate filter'
        report(msg1)
        report(msg2)

    # Sort
    if sort_key is None:
        uniq.sort(key=lambda p: p.name.lower())
    else:
        uniq.sort(key=sort_key)
    msg = f'pdfs sorted by {sort_key if sort_key else "name"}'
    report(msg)

    # Dry run?
    if dry_run:
        return uniq

    # Ensure parent dir exists
    output_file = Path(output_file)

    # Merge
    merger = PdfMerger()
    try:
        for pdf in uniq:
            try:
                merger.append(str(pdf))
            except (FileNotFoundError, PermissionError, PdfReadError) as e:
                msg = f'Failed to append {pdf}: {e}'
                report(msg, 'error')
                continue

        output_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            merger.write(str(output_file))
            msg = f'wrote {len(merger)} to {output_file}'
            report(msg)
        except PermissionError as e:
            msg = f'Failed to write {output_file}: {e}'
            report(msg, 'critical')
            raise

    finally:
        merger.close()

def remove_pages(input_pdf: Path, output_pdf: Path, pages_to_remove: list[int]) -> None:
    """
    Remove 1-based page numbers in `pages_to_remove` from input_pdf and write output_pdf.
    Example: pages_to_remove=[27] removes page 27.
    """
    reader = PdfReader(str(input_pdf))
    writer = PdfWriter()

    # convert 1-based → 0-based indices and validate
    bad = []
    zero_based = set()
    for p in pages_to_remove:
        i = p - 1
        if 0 <= i < len(reader.pages):
            zero_based.add(i)
        else:
            bad.append(p)
    if bad:
        msg = f"Warning: pages out of range and skipped: {bad}"
        report(msg, "warning")

    for i, page in enumerate(reader.pages):
        if i not in zero_based:
            writer.add_page(page)

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with open(output_pdf, "wb") as f:
        writer.write(f)

# usage: remove page 27
'''remove_pages(
    input_pdf=Path("projects/cacciamani_request/data/raw/pdfs/source.pdf"),
    output_pdf=Path("projects/cacciamani_request/data/processed/source_no_p27.pdf"),
    pages_to_remove=[27],
)
'''
