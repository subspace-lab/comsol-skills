"""Core browser automation logic for COMSOL documentation search."""

from playwright.sync_api import sync_playwright, Page
from typing import List
import time

from .models import SearchResult, DocumentContent
from .config import (
    SEARCH_INPUT_SELECTOR,
    SEARCH_RESULTS_SELECTOR,
    SEARCH_RESULTS_LINK_SELECTOR,
    SEARCH_RESULTS_PATH_SELECTOR,
    SEARCH_HIT_SELECTOR,
    PAGE_LOAD_TIMEOUT,
    SEARCH_BOX_TIMEOUT,
    SEARCH_WAIT_TIME,
    CONTENT_LOAD_WAIT_TIME,
    PAGE_INIT_WAIT_TIME,
    DEFAULT_VERSION,
    DEFAULT_MAX_RESULTS,
    BASE_URL_TEMPLATE,
)


class ComsolDocSearcher:
    """Handles browser automation for COMSOL documentation search and retrieval."""

    def __init__(self, version: str = DEFAULT_VERSION, headless: bool = True):
        """Initialize the searcher.

        Args:
            version: COMSOL version (default: from config)
            headless: Run browser in headless mode
        """
        self.version = version
        self.headless = headless
        self.base_url = BASE_URL_TEMPLATE.format(version=version)

    def search(self, search_term: str, max_results: int = DEFAULT_MAX_RESULTS) -> List[SearchResult]:
        """Search COMSOL documentation for a given term.

        Args:
            search_term: The phrase or keywords to search for
            max_results: Maximum number of results to return

        Returns:
            List of SearchResult objects

        Raises:
            Exception: If browser automation fails
        """
        results = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context()
            page = context.new_page()

            try:
                # Navigate to documentation
                page.goto(self.base_url, wait_until='domcontentloaded', timeout=PAGE_LOAD_TIMEOUT)

                # Wait for search box to be available
                search_box = page.wait_for_selector(SEARCH_INPUT_SELECTOR, timeout=SEARCH_BOX_TIMEOUT)

                if search_box:
                    search_box.fill(search_term)
                    search_box.press('Enter')

                    # Wait for results to load
                    time.sleep(SEARCH_WAIT_TIME)

                    # Extract results from the searchResults panel
                    result_sections = page.query_selector_all(SEARCH_RESULTS_SELECTOR)

                    for section in result_sections:
                        if len(results) >= max_results:
                            break

                        # Get module name from h2
                        module_elem = section.query_selector('h2')
                        module = module_elem.inner_text() if module_elem else "Unknown"

                        # Get ALL result links within this module section (FIX: was only getting first)
                        link_buttons = section.query_selector_all(SEARCH_RESULTS_LINK_SELECTOR)

                        # Get all path containers and snippets
                        path_containers = section.query_selector_all('.searchResultsPath')
                        snippet_elems = section.query_selector_all(SEARCH_HIT_SELECTOR)

                        # Each result is a triplet: link, path, snippet
                        # They appear in order in the DOM
                        for i, link_button in enumerate(link_buttons):
                            if len(results) >= max_results:
                                break

                            title = link_button.inner_text().strip()

                            # Get path for THIS specific result (not all paths in section)
                            path_parts = []
                            if i < len(path_containers):
                                path_elements = path_containers[i].query_selector_all(SEARCH_RESULTS_PATH_SELECTOR)
                                path_parts = [
                                    p.inner_text().strip()
                                    for p in path_elements
                                    if p.inner_text().strip() and '>' not in p.inner_text()
                                ]

                            # Clean and truncate path to avoid token overflow
                            path = ' > '.join(path_parts)
                            # Remove duplicate consecutive segments
                            path_segments = path.split(' > ')
                            cleaned_segments = []
                            last_segment = None
                            for seg in path_segments:
                                if seg != last_segment:
                                    cleaned_segments.append(seg)
                                    last_segment = seg
                            path = ' > '.join(cleaned_segments)

                            # Truncate path if still too long (max 500 chars)
                            if len(path) > 500:
                                # Take last 450 chars and add ellipsis
                                path = '...' + path[-450:]

                            # Get snippet for THIS specific result
                            snippet = ""
                            if i < len(snippet_elems):
                                snippet = snippet_elems[i].inner_text().strip()

                            # Truncate long snippets (increased from 200 to 400)
                            if len(snippet) > 400:
                                snippet = snippet[:400] + '...'

                            result = SearchResult(
                                module=module,
                                title=title,
                                path=path,
                                snippet=snippet,
                                search_term=search_term,
                                version=self.version,
                                url=None  # URL construction could be added here
                            )
                            results.append(result)

                        if len(results) >= max_results:
                            break

            except Exception as e:
                raise Exception(f"Error during search: {e}") from e

            finally:
                browser.close()

        return results

    def retrieve_content(self, url: str) -> DocumentContent:
        """Retrieve full content from a COMSOL documentation URL.

        Args:
            url: Full URL to the documentation page

        Returns:
            DocumentContent object with page content

        Raises:
            Exception: If browser automation fails or content cannot be retrieved
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()

            try:
                # Navigate to the specific documentation page
                page.goto(url, timeout=PAGE_LOAD_TIMEOUT)

                # Wait for content to load (SPA navigation)
                time.sleep(CONTENT_LOAD_WAIT_TIME)

                # Get page title
                title = page.title()

                # Extract breadcrumb if available
                breadcrumb_elements = page.query_selector_all(SEARCH_RESULTS_PATH_SELECTOR)
                breadcrumb = [elem.inner_text().strip() for elem in breadcrumb_elements if elem.inner_text().strip()]

                # Get main content
                # COMSOL uses various content containers, try to get the main text
                body = page.query_selector('body')
                content = body.inner_text() if body else ""

                # Look for specific content sections
                # You could refine this to get only the main documentation content
                content_sections = page.query_selector_all('.v-panel-content')
                if content_sections:
                    # Combine content from all panels
                    content_parts = []
                    for section in content_sections:
                        text = section.inner_text().strip()
                        if text and len(text) > 50:  # Filter out empty or very short sections
                            content_parts.append(text)
                    if content_parts:
                        content = '\n\n'.join(content_parts)

                return DocumentContent(
                    url=url,
                    title=title,
                    content=content,
                    breadcrumb=breadcrumb
                )

            except Exception as e:
                raise Exception(f"Error retrieving content from {url}: {e}") from e

            finally:
                browser.close()
