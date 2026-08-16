# pyrefly: ignore [missing-import]
from fastmcp import FastMCP
import logging

from reddit_mcp.application.tools import (
    search_knowledge,
    explore_reddit_discussions,
    extract_public_opinion,
    analyze_niche_trends
)

logger = logging.getLogger(__name__)

def create_server() -> FastMCP:
    """
    Creates and configures the FastMCP server instance.
    
    This server handles the Model Context Protocol (MCP) JSON-RPC messages.
    It sits in the interface layer and will route requests to the application layer.
    
    Returns:
        A configured FastMCP instance ready to be run.
    """
    logger.info("Initializing Reddit MCP Server (AI-Native Edition)")
    
    # Initialize the FastMCP server with dependencies
    mcp = FastMCP(
        name="Reddit MCP Server"
    )
    
    # Register tools from the application layer
    mcp.tool()(search_knowledge)
    mcp.tool()(explore_reddit_discussions)
    mcp.tool()(extract_public_opinion)
    mcp.tool()(analyze_niche_trends)
    logger.debug("FastMCP server initialized with AI-Native tools.")
    
    return mcp
