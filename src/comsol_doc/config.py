"""Configuration constants for COMSOL documentation search."""

# Selectors for COMSOL documentation website
SEARCH_INPUT_SELECTOR = '.searchInput'
SEARCH_RESULTS_SELECTOR = '.searchResults .v-verticallayout'
SEARCH_RESULTS_LINK_SELECTOR = '.searchResultsLink'
SEARCH_RESULTS_PATH_SELECTOR = '.searchResultsPathLink'
SEARCH_HIT_SELECTOR = '.searchHit'

# Timeouts (in milliseconds for Playwright, seconds for sleep)
PAGE_LOAD_TIMEOUT = 60000  # 60 seconds
SEARCH_BOX_TIMEOUT = 30000  # 30 seconds

# Wait times (in seconds)
SEARCH_WAIT_TIME = 5  # Wait after submitting search
CONTENT_LOAD_WAIT_TIME = 8  # Wait for direct URL content loading
PAGE_INIT_WAIT_TIME = 3  # Wait for initial page load

# Defaults
DEFAULT_VERSION = '6.4'
DEFAULT_MAX_RESULTS = 20

# URL templates
BASE_URL_TEMPLATE = 'https://doc.comsol.com/{version}/docserver/'
