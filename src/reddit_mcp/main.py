import asyncio
import logging
import sys

from reddit_mcp.application.tools import DependencyContainer
from reddit_mcp.infrastructure.logging import setup_logging
from reddit_mcp.interface.server import create_server


def main():
    """
    Main entry point for the Reddit MCP Server.

    This script initializes the strict stderr logging configuration to prevent
    JSON-RPC stream corruption, sets up the server, and starts the STDIO transport.
    """
    # 1. Initialize strictly to stderr
    setup_logging(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting Reddit MCP Server...")

        # 2. Create the FastMCP server instance
        mcp = create_server()

        # 3. Start the standard IO (STDIO) transport loop.
        # FastMCP's run() uses STDIO by default in production.
        logger.info("Starting STDIO transport loop. Listening for JSON-RPC messages.")
        mcp.run()

    except KeyboardInterrupt:
        logger.info("Server stopped by user.")
    except Exception:
        logger.exception("Fatal error encountered")
        sys.exit(1)
    finally:
        logger.info("Cleaning up resources...")
        try:
            client = DependencyContainer.get_reddit_client()
            asyncio.run(client.close())
        except Exception as cleanup_error:  # noqa: BLE001
            logger.error(f"Error during cleanup: {cleanup_error}")


if __name__ == "__main__":
    main()
