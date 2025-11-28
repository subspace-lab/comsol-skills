"""Data models for COMSOL documentation search."""

from dataclasses import dataclass, asdict
from typing import Optional, List


@dataclass
class SearchResult:
    """Represents a single search result from COMSOL documentation.

    Attributes:
        module: COMSOL module name (e.g., "Heat Transfer Module")
        title: Title of the documentation entry
        path: Breadcrumb path to the document
        snippet: Text snippet/preview from the document
        search_term: The search term that produced this result
        version: COMSOL version (e.g., "6.4")
        url: Optional direct URL to the documentation page
    """
    module: str
    title: str
    path: str
    snippet: str
    search_term: str
    version: str
    url: Optional[str] = None

    def to_dict(self):
        """Convert to dictionary for backward compatibility."""
        return asdict(self)


@dataclass
class DocumentContent:
    """Represents retrieved documentation content.

    Attributes:
        url: Full URL of the documentation page
        title: Page title
        content: Full text content of the page
        breadcrumb: List of breadcrumb items showing document location
    """
    url: str
    title: str
    content: str
    breadcrumb: List[str]

    def to_dict(self):
        """Convert to dictionary."""
        return asdict(self)
