import logging
import re
from typing import Dict, Any, List, Optional, Tuple

from reddit_mcp.domain.models import RedditPost, RedditComment, RedditThread
from reddit_mcp.application.utils import truncate_text, format_timestamp, build_comment_url
from reddit_mcp.infrastructure.http import ResilientHTTPClient
from reddit_mcp.infrastructure.search.base import BaseSearchProvider

logger = logging.getLogger(__name__)

class RedditClientError(Exception):
    """Base exception for Reddit client errors."""
    pass

class RedditClient:
    """
    Asynchronous client for interacting with the Reddit API using a resilient HTTP client.
    """
    def __init__(self, http_client: ResilientHTTPClient, search_provider: BaseSearchProvider):
        self.http_client = http_client
        self.search_provider = search_provider

    async def close(self):
        """Close underlying resources."""
        await self.http_client.close()

    def _map_submission(self, data: Dict[str, Any]) -> RedditPost:
        """Map Reddit JSON submission data to our enriched RedditPost model."""
        created_utc = data.get("created_utc")
        from reddit_mcp.application.utils import calculate_age_in_days
        
        return RedditPost(
            id=data.get("id", ""),
            title=data.get("title", ""),
            subreddit=data.get("subreddit", ""),
            score=data.get("score", 0),
            upvote_ratio=data.get("upvote_ratio", 0.0),
            num_comments=data.get("num_comments", 0),
            url=f"https://www.reddit.com{data.get('permalink', '')}",
            age_in_days=calculate_age_in_days(created_utc),
            created_at_human=format_timestamp(created_utc),
            text_preview=truncate_text(data.get("selftext", ""), 500)
        )

    def _map_comment(self, data: Dict[str, Any], post_id: str, subreddit: str) -> Optional[RedditComment]:
        """Map Reddit JSON comment data to our refined RedditComment model."""
        body = data.get("body")
        if not body:
            return None
            
        comment_id = data.get("id", "")
        return RedditComment(
            id=comment_id,
            author=data.get("author", "[deleted]"),
            score=data.get("score", 0),
            body=truncate_text(body, 2000),
            comment_url=build_comment_url(subreddit, post_id, comment_id),
            created_at_human=format_timestamp(data.get("created_utc"))
        )

    def _extract_post_id(self, url: str) -> Optional[str]:
        """Extract the Reddit post ID from a standard URL."""
        match = re.search(r"/comments/([a-z0-9]+)", url)
        return match.group(1) if match else None

    async def get_subreddit_trends(
        self, 
        subreddit: str, 
        category: str = "hot", 
        time_filter: str = "all", 
        limit: int = 10,
        after: Optional[str] = None,
        before: Optional[str] = None
    ) -> Tuple[List[RedditPost], Optional[str]]:
        """Fetch trending posts from a subreddit."""
        subreddit = subreddit.strip()
        if subreddit.startswith("/r/"):
            subreddit = subreddit[3:]
        elif subreddit.startswith("r/"):
            subreddit = subreddit[2:]
            
        url = f"https://oauth.reddit.com/r/{subreddit}/{category}.json"
        params = {"limit": limit, "t": time_filter}
        if after:
            params["after"] = after
        if before:
            params["before"] = before

        try:
            response = await self.http_client.get(url, params=params)
            data = response.json()
            
            posts = []
            for child in data.get("data", {}).get("children", []):
                if child.get("kind") == "t3":
                    posts.append(self._map_submission(child["data"]))
                    
            new_after = data.get("data", {}).get("after")
            return posts, new_after
        except Exception as e:
            raise RedditClientError(f"Error fetching subreddit trends: {e}")

    async def get_post_thread(self, post_url: str, max_comments: int = 50) -> RedditThread:
        """Fetch a specific post and its top comments, parsing the comment tree."""
        post_id = self._extract_post_id(post_url)
        if not post_id:
            raise RedditClientError("Invalid Reddit post URL provided.")
            
        url = f"https://oauth.reddit.com/comments/{post_id}.json"
        params = {"limit": max_comments + 20} # Buffer for 'more' items
        
        try:
            response = await self.http_client.get(url, params=params)
            data = response.json()
            
            if not isinstance(data, list) or len(data) < 2:
                raise RedditClientError("Unexpected response format from Reddit API.")
                
            post_data = data[0]["data"]["children"][0]["data"]
            post = self._map_submission(post_data)
            
            comments = []
            comment_children = data[1].get("data", {}).get("children", [])
            
            def parse_comments(children: List[Dict[str, Any]]):
                for child in children:
                    if len(comments) >= max_comments:
                        return
                        
                    kind = child.get("kind")
                    c_data = child.get("data", {})
                    
                    if kind == "t1": # Comment
                        mapped = self._map_comment(c_data, post.id, post.subreddit)
                        if mapped:
                            comments.append(mapped)
                            
                        # Recursively parse replies if they exist
                        replies = c_data.get("replies")
                        if isinstance(replies, dict):
                            parse_comments(replies.get("data", {}).get("children", []))
                            
                    elif kind == "more":
                        # We ignore 'more' comments to avoid excessive API requests.
                        # This guarantees we only use the comments returned in the initial payload.
                        continue

            parse_comments(comment_children)
            
            return RedditThread(post=post, comments=comments)
        except Exception as e:
            raise RedditClientError(f"Error fetching thread: {e}")

    async def native_reddit_search(
        self,
        query: str,
        subreddit: Optional[str] = None,
        sort: str = "relevance",
        time_filter: str = "all",
        limit: int = 10,
        after: Optional[str] = None
    ) -> Tuple[List[RedditPost], Optional[str]]:
        """Search using Reddit's official API. Ideal for metrics like upvote_ratio and native sorting."""
        url = "https://oauth.reddit.com/search.json"
        params = {
            "q": query,
            "sort": sort,
            "t": time_filter,
            "limit": limit
        }
        if subreddit:
            url = f"https://oauth.reddit.com/r/{subreddit}/search.json"
            params["restrict_sr"] = True
        if after:
            params["after"] = after

        try:
            response = await self.http_client.get(url, params=params)
            data = response.json()
            
            posts = []
            for child in data.get("data", {}).get("children", []):
                if child.get("kind") == "t3":
                    posts.append(self._map_submission(child["data"]))
                    
            new_after = data.get("data", {}).get("after")
            return posts, new_after
        except Exception as e:
            raise RedditClientError(f"Error during native Reddit search: {e}")

    async def search(
        self, 
        query: str, 
        subreddit: Optional[str] = None, 
        sort: str = "relevance", 
        time_filter: str = "all", 
        limit: int = 10,
        after: Optional[str] = None,
        before: Optional[str] = None
    ) -> Tuple[List[RedditPost], Optional[str]]:
        """
        Search Reddit using the injected SearchProvider (e.g. DDG).
        Useful for general knowledge finding where native search fails.
        """
        try:
            search_results = await self.search_provider.search(
                query=query, 
                subreddit=subreddit, 
                time_filter=time_filter, 
                limit=limit
            )
            
            if not search_results:
                return [], None
                
            post_ids = []
            for res in search_results:
                if hasattr(res, 'post_id') and res.post_id:
                    post_ids.append(f"t3_{res.post_id}")
                    
            if not post_ids:
                return [], None
                
            url = "https://oauth.reddit.com/api/info.json"
            params = {"id": ",".join(post_ids)}
            
            response = await self.http_client.get(url, params=params)
            data = response.json()
            
            posts = []
            for child in data.get("data", {}).get("children", []):
                if child.get("kind") == "t3":
                    posts.append(self._map_submission(child["data"]))
                    
            # Search providers like DDG don't natively return Reddit pagination tokens
            return posts, None
            
        except Exception as e:
            raise RedditClientError(f"Error during web search: {e}")
