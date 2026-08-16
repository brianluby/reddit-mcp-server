# Search Providers

This directory contains the integration logic for various search engines. 
By default, we use **DuckDuckGo** as it doesn't require an API key and performs well for `.reddit.com` searches.

## 🤝 How to contribute a new Search Provider

Want to add Google Search, Tavily, or Bing? It's extremely easy:
1. Create a new file in this directory (e.g., `google_search.py`).
2. Import the base class: `from reddit_mcp.infrastructure.search.base import BaseSearchProvider, SearchResult`.
3. Create your class and make it inherit from `BaseSearchProvider`.
4. Implement the async `search()` method.
5. Update `src/reddit_mcp/application/tools.py` to use your new provider!