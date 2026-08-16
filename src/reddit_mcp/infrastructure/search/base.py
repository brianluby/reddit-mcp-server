from abc import ABC, abstractmethod
from typing import List, Optional

class SearchResult:
    """A generic search result."""
    def __init__(self, url: str, title: str, snippet: str) -> None:
        self.url = url
        self.title = title
        self.snippet = snippet

class BaseSearchProvider(ABC):
    """
    Abstract base class for search engine providers.
    Follows the Strategy Pattern to allow easy addition of new search engines.
    """
    
    @abstractmethod
    async def search(
        self,
        query: str,
        subreddit: Optional[str] = None,
        time_filter: str = "all",
        limit: int = 10,
    ) -> List[SearchResult]:
        """
        Execute a search query and return a list of SearchResults.
        """
        pass
