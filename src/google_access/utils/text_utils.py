"""
Utilities for normalizing and cleaning up text.
"""

import unicodedata
import re

def remove_diacritics(text: str) -> str:
    """Return text without accents/diacritics.
    
    Example:
        >>> remove_diacritics("Señor Niño")
        'Senor Nino'
    """
    nfkd_form = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in nfkd_form if not unicodedata.combining(ch))

def canon(name: str) -> str:
    """Canonicalize a filename or text string for matching.

    - Removes diacritics
    - Lowercases
    - Normalizes dashes/underscores to spaces
    - Collapses multiple spaces
    - Strips leading/trailing spaces

    Example:
        >>> canon(" Recíbo---de_dopaje.PDF ")
        'recibo de dopaje.pdf'
    """
    # remove diacritics
    s = remove_diacritics(name)
    # lowercase
    s = s.lower()
    # normalize dashes/underscores to spaces
    s = re.sub(r"[-_]+", " ", s)
    # collapse multiple spaces
    s = re.sub(r"\s+", " ", s)
    # strip leading/trailing spaces
    s = s.strip()
    return s
