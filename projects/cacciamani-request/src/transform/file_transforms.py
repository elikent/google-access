from pathlib import Path
from typing import Iterable, Callable, Optional, Sequence
from PyPDF2 import PdfMerger

def combine_pdfs(
    sources: Iterable[Path] | Path,
    output_file: Path,
    *,
    match: Optional[Callable[[Path], bool]] = None,
    patterns: Optional[Sequence[str]] = None,
    sort_key: Optional[Callable[[Path], object]] = None,
    dry_run: bool = False,
) -> list[Path]:
    """Combine PDFs into one file.

    Args:
        sources: A directory Path (to scan) or an iterable of Paths (files/dirs).
        output_file: Where to write the merged PDF.
        match: Optional predicate(Path)->bool to filter files.
        patterns: Optional list of glob patterns (e.g., ["*single*.pdf", "*2025*.pdf"]).
        recursive: If True, descend into subdirectories when scanning dirs.
        sort_key: Optional key function to sort matched PDFs (default: by name).
        dry_run: If True, don't write output—just return matched files.

    Returns:
        The list of PDF Paths that would be (or were) merged, in order.
    """
    # Normalize sources to a list of paths to scan
    if isinstance(sources, Path):   # if sources is a Path, put it in a list and store in scan_paths
        scan_paths = [sources]
    else:                           # else, just store in scan_paths
        scan_paths = list(sources)

    # Collect candidate files
    pdfs: list[Path] = []   # create empty list of paths pdfs
    for p in scan_paths:
        if p.is_file():     # if p is a pdf file, add it to pdfs
            pdfs.append(p)
        elif p.is_dir():    # if p is a directory, 
            if patterns:    
                for pat in patterns:
                    pdfs.extend(p.glob(pat)) 
            else:
                it = p.glob("*.pdf")
                pdfs.extend(it)
        else:
            # silently skip non-existent
            continue

    # Deduplicate & keep only files
    uniq = []
    seen = set()
    for f in pdfs:
        try:
            fp = f.resolve()
        except Exception:
            continue
        if fp.is_file() and fp.suffix.lower() == ".pdf" and fp not in seen:
            uniq.append(fp)
            seen.add(fp)

    # Apply predicate filter if provided
    if match:
        uniq = [p for p in uniq if match(p)]

    # Sort
    if sort_key is None:
        uniq.sort(key=lambda p: p.name.lower())
    else:
        uniq.sort(key=sort_key)

    # Dry run?
    if dry_run:
        return uniq

    # Ensure parent dir exists
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Merge
    merger = PdfMerger()
    try:
        for pdf in uniq:
            merger.append(str(pdf))
        merger.write(str(output_file))
    finally:
        merger.close()

    return uniq



def combine_pdfs(
    sources: Iterable[Path] | Path,
    output_file: Path,
    *,
    match: Optional[Callable[[Path], bool]] = None,
    patterns: Optional[Sequence[str]] = None,
    recursive: bool = False,
    sort_key: Optional[Callable[[Path], object]] = None,
    dry_run: bool = False,
) -> list[Path]:
    """Combine PDFs into one file.

    Args:
        sources: A directory Path (to scan) or an iterable of Paths (files/dirs).
        output_file: Where to write the merged PDF.
        match: Optional predicate(Path)->bool to filter files.
        patterns: Optional list of glob patterns (e.g., ["*single*.pdf", "*2025*.pdf"]).
        recursive: If True, descend into subdirectories when scanning dirs.
        sort_key: Optional key function to sort matched PDFs (default: by name).
        dry_run: If True, don't write output—just return matched files.

    Returns:
        The list of PDF Paths that would be (or were) merged, in order.
    """
    # Normalize sources to a list of paths to scan
    if isinstance(sources, Path):   # if sources is a Path, put it in a list and store in scan_paths
        scan_paths = [sources]
    else:                           # else, just store in scan_paths
        scan_paths = list(sources)

    # Collect candidate files
    pdfs: list[Path] = []   # create empty list of paths pdfs
    for p in scan_paths:
        if p.is_file():     # if p is a file, add it to pdfs
            pdfs.append(p)
        elif p.is_dir():    # if p is a directory, 
            if patterns:    
                for pat in patterns:
                    pdfs.extend(p.rglob(pat) if recursive else p.glob(pat))
            else:
                it = p.rglob("*.pdf") if recursive else p.glob("*.pdf")
                pdfs.extend(it)
        else:
            # silently skip non-existent
            continue

    # Deduplicate & keep only files
    uniq = []
    seen = set()
    for f in pdfs:
        try:
            fp = f.resolve()
        except Exception:
            continue
        if fp.is_file() and fp.suffix.lower() == ".pdf" and fp not in seen:
            uniq.append(fp)
            seen.add(fp)

    # Apply predicate filter if provided
    if match:
        uniq = [p for p in uniq if match(p)]

    # Sort
    if sort_key is None:
        uniq.sort(key=lambda p: p.name.lower())
    else:
        uniq.sort(key=sort_key)

    # Dry run?
    if dry_run:
        return uniq

    # Ensure parent dir exists
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Merge
    merger = PdfMerger()
    try:
        for pdf in uniq:
            merger.append(str(pdf))
        merger.write(str(output_file))
    finally:
        merger.close()

    return uniq

