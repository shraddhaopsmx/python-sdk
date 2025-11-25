"""MCP Snippets.

This package contains simple examples of MCP server features.
Each server demonstrates a single feature and can be run as a standalone server.

To run a server, use the command:
    uv run server basic_tool sse
"""

import importlib
import sys
from typing import Literal, cast


def run_server():
    """Run a server by name with optional transport.

    Usage: server <server-name> [transport]
    Example: server basic_tool sse
    """
    if len(sys.argv) < 2:
        print("Usage: server <server-name> [transport]")
        print("Available servers: basic_tool, basic_resource, basic_prompt, tool_progress,")
        print("                   sampling, elicitation, completion, notifications")
        print("Available transports: stdio (default), sse, streamable-http")
        sys.exit(1)

    server_name = sys.argv[1]
    transport = sys.argv[2] if len(sys.argv) > 2 else "stdio"

    # Whitelist of allowed server names
    allowed_servers = {
        "basic_tool",
        "basic_resource", 
        "basic_prompt",
        "tool_progress",
        "sampling",
        "elicitation",
        "completion",
        "notifications"
    }
    
    if server_name not in allowed_servers:
        print(f"Error: Server '{server_name}' not found")
        print("Available servers: basic_tool, basic_resource, basic_prompt, tool_progress,")
        print("                   sampling, elicitation, completion, notifications")
        sys.exit(1)

    try:
        # Use explicit conditional imports with string literals to satisfy static analysis
        if server_name == "basic_tool":
            module = importlib.import_module("examples.snippets.servers.basic_tool")
        elif server_name == "basic_resource":
            module = importlib.import_module("examples.snippets.servers.basic_resource")
        elif server_name == "basic_prompt":
            module = importlib.import_module("examples.snippets.servers.basic_prompt")
        elif server_name == "tool_progress":
            module = importlib.import_module("examples.snippets.servers.tool_progress")
        elif server_name == "sampling":
            module = importlib.import_module("examples.snippets.servers.sampling")
        elif server_name == "elicitation":
            module = importlib.import_module("examples.snippets.servers.elicitation")
        elif server_name == "completion":
            module = importlib.import_module("examples.snippets.servers.completion")
        elif server_name == "notifications":
            module = importlib.import_module("examples.snippets.servers.notifications")
        else:
            # This should never be reached due to the whitelist check above
            raise ImportError(f"Server '{server_name}' not found")
            
        module.mcp.run(cast(Literal["stdio", "sse", "streamable-http"], transport))
    except ImportError:
        print(f"Error: Server '{server_name}' not found")
        sys.exit(1)
