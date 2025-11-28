"""COMSOL Documentation Search Package.

A Python package for searching and retrieving COMSOL Multiphysics documentation
using browser automation.
"""

from .core import ComsolDocSearcher
from .models import SearchResult, DocumentContent
from .formatters import OutputFormatter
from .config import DEFAULT_VERSION, DEFAULT_MAX_RESULTS

__version__ = "0.2.0"

__all__ = [
    "ComsolDocSearcher",
    "SearchResult",
    "DocumentContent",
    "OutputFormatter",
    "search_comsol_docs_advanced",  # Backward compatibility
]


# Backward compatibility wrapper
def search_comsol_docs_advanced(search_term, max_results=20, version='6.4', headless=True):
    """Legacy function for backward compatibility.

    This function maintains the original API from comsol_doc_search.py
    for existing code that depends on it.

    Args:
        search_term: The phrase or keywords to search for
        max_results: Maximum number of results to return
        version: COMSOL version (default: 6.4)
        headless: Run browser in headless mode (default: True)

    Returns:
        List of dictionaries with search results (legacy format)
    """
    searcher = ComsolDocSearcher(version=version, headless=headless)
    results = searcher.search(search_term, max_results)
    # Convert to old dict format for backward compatibility
    return [r.to_dict() for r in results]
