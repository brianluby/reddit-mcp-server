import logging
import sys

def setup_logging(level: int = logging.INFO) -> None:
    """
    Configures the root logger to output strictly to stderr.
    
    This is a critical requirement for MCP servers using standard I/O transport.
    If logs are written to stdout, they will corrupt the JSON-RPC communication
    between the MCP server and the client.
    
    Args:
        level: The logging level to set (e.g., logging.INFO, logging.DEBUG)
    """
    # Create a handler that writes exclusively to stderr
    handler = logging.StreamHandler(sys.stderr)
    
    # Define a clear format for the logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Get the root logger
    root_logger = logging.getLogger()
    
    # Remove any existing handlers to prevent duplicate logs or stdout leakage
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
        
    root_logger.addHandler(handler)
    root_logger.setLevel(level)
    
    # Ensure our own package logger is also explicitly set
    logger = logging.getLogger("reddit_mcp")
    logger.setLevel(level)
    
    logger.debug("Logging initialized (stderr only).")
