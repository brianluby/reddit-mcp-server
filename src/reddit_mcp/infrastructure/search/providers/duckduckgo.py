import asyncio
import logging
import re
from typing import List, Optional

from ddgs import DDGS

from reddit_mcp.infrastructure.search.base import BaseSearchProvider, SearchResult

logger = logging.getLogger(__name__)

class RedditSearchResult(SearchResult):
    """A search result specifically parsed for Reddit URLs."""
    
    @property
    def post_id(self) -> str:
        """Extract the Reddit post ID from the URL, if present."""
        match = re.search(r"/comments/([a-z0-9]+)", self.url)
        return match.group(1) if match else ""

    @property
    def subreddit(self) -> str:
        """Extract the subreddit name from the URL, if present."""
        match = re.search(r"/r/([a-zA-Z0-9_]+)", self.url)
        return match.group(1) if match else ""

class DuckDuckGoSearchProvider(BaseSearchProvider):
    """
    Asynchronous client for searching Reddit using DuckDuckGo's 'site:' operator.
    This provides a more robust search than Reddit's internal search for general queries.
    """
    
    async def search(
        self,
        query: str,
        subreddit: Optional[str] = None,
        time_filter: str = "all",
        limit: int = 10,
    ) -> List[RedditSearchResult]:
        """
        Searches Reddit using DuckDuckGo.
        Returns a list of RedditSearchResult objects pointing to Reddit threads.
        """
        if subreddit:
            subreddit = subreddit.strip()
            if subreddit.startswith("/r/"):
                subreddit = subreddit[3:]
            elif subreddit.startswith("r/"):
                subreddit = subreddit[2:]
            site_filter = f"site:reddit.com/r/{subreddit}"
        else:
            site_filter = "site:reddit.com"

        full_query = f"{site_filter} {query}"

        logger.info(f"DDG Search Query: {full_query}")

        timelimit = None
        if time_filter == "day":
            timelimit = "d"
        elif time_filter == "week":
            timelimit = "w"
        elif time_filter == "month":
            timelimit = "m"
        elif time_filter == "year":
            timelimit = "y"

        try:
            def _search() -> List[dict]:
                with DDGS() as ddgs:
                    return list(ddgs.text(full_query, timelimit=timelimit, max_results=limit))

            results = await asyncio.to_thread(_search)
        except Exception as e:
            logger.error(f"Error during DuckDuckGo search: {e}")
            return []

        urls: List[RedditSearchResult] = []
        for res in results:
            url = res.get("href", "")
            if "reddit.com" in url:
                urls.append(RedditSearchResult(
                    url=url,
                    title=res.get("title", ""),
                    snippet=res.get("body", ""),
                ))
        return urls
