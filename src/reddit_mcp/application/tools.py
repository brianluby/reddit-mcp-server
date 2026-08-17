import logging
from typing import Annotated, Literal

from pydantic import Field

from reddit_mcp.application.utils import (
    build_meta_context,
    is_high_quality_comment,
    llm_timeout,
)
from reddit_mcp.domain.models import (
    PaginatedCommentResponse,
    PaginatedPostResponse,
)
from reddit_mcp.infrastructure.arctic_shift_client import (
    ArcticShiftClient,
    ArcticShiftError,
)
from reddit_mcp.infrastructure.auth import RedditAuthManager
from reddit_mcp.infrastructure.http import ResilientHTTPClient
from reddit_mcp.infrastructure.reddit_client import (
    RedditClient,
    RedditClientError,
)
from reddit_mcp.infrastructure.search.base import SearchProviderError
from reddit_mcp.infrastructure.search.providers.duckduckgo import (
    DuckDuckGoSearchProvider,
)

logger = logging.getLogger(__name__)

DEGRADED_MESSAGE = (
    "Reddit retrieval failed and the fallback flow could not complete. Try again later."
)
ARCHIVE_LAG_MESSAGE = "Served via the Arctic Shift archive; scores may lag live Reddit."


class DependencyContainer:
    """Simple container for lazy-loading and injecting dependencies."""

    _reddit_client: RedditClient | None = None
    _arctic_shift_client: ArcticShiftClient | None = None
    _search_provider: DuckDuckGoSearchProvider | None = None

    @classmethod
    def _init_dependencies(cls):
        if cls._reddit_client is None:
            from reddit_mcp.infrastructure.settings import get_settings

            settings = get_settings()
            user_agent = settings.reddit_user_agent
            auth_manager = RedditAuthManager(user_agent=user_agent)
            http_client = ResilientHTTPClient(
                auth_manager=auth_manager, user_agent=user_agent
            )
            cls._search_provider = DuckDuckGoSearchProvider()
            cls._reddit_client = RedditClient(
                http_client=http_client, search_provider=cls._search_provider
            )
            cls._arctic_shift_client = ArcticShiftClient(http_client=http_client)

    @classmethod
    def get_reddit_client(cls) -> RedditClient:
        cls._init_dependencies()
        return cls._reddit_client

    @classmethod
    def get_arctic_shift_client(cls) -> ArcticShiftClient:
        cls._init_dependencies()
        return cls._arctic_shift_client

    @classmethod
    def get_search_provider(cls) -> DuckDuckGoSearchProvider:
        cls._init_dependencies()
        return cls._search_provider

    @classmethod
    def override_reddit_client(cls, client: RedditClient) -> None:
        """Used for injecting mock clients during testing."""
        cls._reddit_client = client


@llm_timeout(timeout_seconds=15)
async def search_knowledge(
    query: str,
    subreddit: str | None = None,
    time_filter: Literal["all", "day", "week", "month", "year"] = "all",
    limit: Annotated[int, Field(ge=1, le=100)] = 10,
) -> PaginatedPostResponse:
    """
    STEP 1: FOUNDATION SEARCH. Use this to find factual threads or technical explanations.
    This uses a broad web-search (DuckDuckGo) to find Reddit threads that Reddit's own search might miss.
    Note: Pagination is not supported for this specific tool.
    """
    logger.info(f"search_knowledge: query='{query}'")
    client = DependencyContainer.get_reddit_client()
    posts = []
    data_source = None
    message = None

    try:
        posts, _ = await client.search(
            query=query, subreddit=subreddit, time_filter=time_filter, limit=limit
        )
    except RedditClientError as e:
        logger.warning(
            f"Reddit API failed or credentials missing ({e}); "
            "falling back to DDG + Arctic Shift for search_knowledge."
        )
        search_provider = DependencyContainer.get_search_provider()
        arctic_client = DependencyContainer.get_arctic_shift_client()

        try:
            search_results = await search_provider.search(
                query=query, subreddit=subreddit, time_filter=time_filter, limit=limit
            )
            post_ids = [res.post_id for res in search_results if res.post_id]
            if post_ids:
                posts = await arctic_client.get_posts_by_ids(post_ids)
                data_source = "arctic_shift"
                message = ARCHIVE_LAG_MESSAGE
        except (SearchProviderError, ArcticShiftError) as e:
            logger.warning(f"Fallback providers failed for search_knowledge: {e}")
            return PaginatedPostResponse(
                meta_context=build_meta_context(),
                data=[],
                next_page_token=None,
                status="degraded",
                message=DEGRADED_MESSAGE,
            )

    # Filter: Ensure we don't send posts with empty titles or very low quality
    valid_posts = [p for p in posts if len(p.title) > 5]

    return PaginatedPostResponse(
        meta_context=build_meta_context(),
        data=valid_posts,
        next_page_token=None,
        data_source=data_source,
        message=message,
    )


@llm_timeout(timeout_seconds=15)
async def explore_reddit_discussions(
    keyword: str,
    subreddit: str | None = None,
    sort: Literal["relevance", "hot", "top", "new", "comments"] = "relevance",
    time_filter: Literal["all", "day", "week", "month", "year"] = "year",
    limit: Annotated[int, Field(ge=1, le=100)] = 10,
    page_token: str | None = None,
) -> PaginatedPostResponse:
    """
    STEP 2: SENTIMENT EXPLORATION. Use this to gauge public opinion and market acceptance.
    Always check `upvote_ratio`: >0.8 = Positive, ~0.5 = Controversial.
    Check `age_in_days` to ensure relevance. Use `next_page_token` to see more results.
    """
    logger.info(f"explore_reddit_discussions: keyword='{keyword}'")
    client = DependencyContainer.get_reddit_client()
    posts = []
    next_token = None
    data_source = None
    message = None

    try:
        posts, next_token = await client.native_reddit_search(
            query=keyword,
            subreddit=subreddit,
            sort=sort,
            time_filter=time_filter,
            limit=limit,
            after=page_token,
        )
    except RedditClientError as e:
        logger.warning(
            f"Reddit API failed or credentials missing ({e}); "
            "falling back to DDG + Arctic Shift for explore_reddit_discussions."
        )
        search_provider = DependencyContainer.get_search_provider()
        arctic_client = DependencyContainer.get_arctic_shift_client()

        try:
            search_results = await search_provider.search(
                query=keyword, subreddit=subreddit, time_filter=time_filter, limit=limit
            )
            post_ids = [res.post_id for res in search_results if res.post_id]
            if post_ids:
                posts = await arctic_client.get_posts_by_ids(post_ids)
                data_source = "arctic_shift"
                message = ARCHIVE_LAG_MESSAGE
        except (SearchProviderError, ArcticShiftError) as e:
            logger.warning(
                f"Fallback providers failed for explore_reddit_discussions: {e}"
            )
            return PaginatedPostResponse(
                meta_context=build_meta_context(),
                data=[],
                next_page_token=None,
                status="degraded",
                message=DEGRADED_MESSAGE,
            )

    return PaginatedPostResponse(
        meta_context=build_meta_context(),
        data=posts,
        next_page_token=next_token,
        data_source=data_source,
        message=message,
    )


@llm_timeout(timeout_seconds=20)
async def extract_public_opinion(
    post_url: str, max_comments: Annotated[int, Field(ge=1, le=100)] = 30
) -> PaginatedCommentResponse:
    """
    DEEP DIVE TOOL: Use this ONLY after finding a relevant post via search tools.
    This tool extracts PURE human opinions, filtering out noise, bots, and low-effort content.
    Citations: You MUST use the `comment_url` for each specific quote in your final report.
    """
    logger.info(f"extract_public_opinion: url='{post_url}'")
    client = DependencyContainer.get_reddit_client()
    data_source = None
    message = None

    # Fetch thread (The client already maps basic data)
    try:
        thread = await client.get_post_thread(
            post_url=post_url, max_comments=max_comments
        )
    except RedditClientError as e:
        logger.warning(
            f"Reddit API failed or credentials missing ({e}); "
            "falling back to Arctic Shift for extract_public_opinion."
        )
        arctic_client = DependencyContainer.get_arctic_shift_client()
        try:
            thread = await arctic_client.get_post_thread(
                post_url_or_id=post_url, max_comments=max_comments
            )
        except ArcticShiftError as e:
            logger.warning(f"Fallback providers failed for extract_public_opinion: {e}")
            return PaginatedCommentResponse(
                meta_context=build_meta_context(),
                data=[],
                status="degraded",
                message=DEGRADED_MESSAGE,
            )
        data_source = "arctic_shift"
        message = ARCHIVE_LAG_MESSAGE

    # Application Layer Filtering: Drop low quality before responding
    # This saves tokens and ensures the LLM only sees valuable input.
    refined_comments = [
        c
        for c in thread.comments
        if is_high_quality_comment(
            author=c.author,
            body=c.body,
            score=c.score,
            thread_age_in_days=thread.post.age_in_days,
        )
    ]

    return PaginatedCommentResponse(
        meta_context=build_meta_context(),
        data=refined_comments,
        data_source=data_source,
        message=message,
    )


@llm_timeout(timeout_seconds=15)
async def analyze_niche_trends(
    subreddit_name: str,
    trend_type: Literal["hot", "new", "top", "rising"] = "rising",
    limit: Annotated[int, Field(ge=1, le=100)] = 10,
    page_token: str | None = None,
) -> PaginatedPostResponse:
    """
    Use this tool when asked to suggest ideas, find pain points, or discover opportunities in a specific niche (e.g., 'SaaS', 'Entrepreneur').
    By looking at 'rising' or 'hot' posts, you can identify what problems users are actively struggling with RIGHT NOW.
    Always compare the post's `created_at` with the `current_server_date` provided in `meta_context`.
    """
    logger.info(f"analyze_niche_trends: subreddit='{subreddit_name}'")
    client = DependencyContainer.get_reddit_client()

    try:
        posts, next_token = await client.get_subreddit_trends(
            subreddit=subreddit_name, category=trend_type, limit=limit, after=page_token
        )
        return PaginatedPostResponse(
            meta_context=build_meta_context(), data=posts, next_page_token=next_token
        )
    except RedditClientError:
        logger.warning("Reddit API failed or credentials missing. Cannot fetch trends.")
        return PaginatedPostResponse(
            meta_context=build_meta_context(),
            data=[],
            next_page_token=None,
            status="warning",
            message=(
                "Trending data is unavailable (OAuth credentials missing or Reddit API "
                "unreachable) due to archive lag. Please use search tools instead."
            ),
        )
