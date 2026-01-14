import json
from langchain_google_community import CalendarToolkit
from langchain.tools import tool


def safe_response(result):
    """Normalize tool output to avoid empty or invalid content."""
    if isinstance(result, list) and len(result) == 0:
        return "No results found."
    if result is None:
        return "No results found."
    if isinstance(result, dict):
        return json.dumps(result)
    return result


def create_calendar_tools():
    toolkit = CalendarToolkit()
    raw_tools = toolkit.get_tools()
    safe_tools = []

    for t in raw_tools:
        # Wrap specific tools that need special handling
        if t.name in ["search_events", "get_current_datetime"]:
            # Using decorator with args_schema to preserve input schema
            # Use factory function to capture the current tool (avoid closure bug)
            def make_wrapper(base_tool):
                @tool(base_tool.name, description=base_tool.description, args_schema=base_tool.args_schema)
                def wrapped_tool(**kwargs):
                    # Fix calendar_id None issue for get_current_datetime
                    if base_tool.name == "get_current_datetime" and kwargs.get("calendar_id") is None:
                        kwargs["calendar_id"] = "primary"
                    result = base_tool.invoke(kwargs)
                    return safe_response(result)
                return wrapped_tool

            def make_async_wrapper(base_tool):
                @tool(base_tool.name, description=base_tool.description, args_schema=base_tool.args_schema)
                async def wrapped_tool_async(**kwargs):
                    # Fix calendar_id None issue for get_current_datetime
                    if base_tool.name == "get_current_datetime" and kwargs.get("calendar_id") is None:
                        kwargs["calendar_id"] = "primary"
                    result = await base_tool.ainvoke(kwargs)
                    return safe_response(result)
                return wrapped_tool_async

            # Check if the tool supports async
            if hasattr(t, "ainvoke"):
                safe_tools.append(make_async_wrapper(t))
            else:
                safe_tools.append(make_wrapper(t))
        else:
            # Keep all other tools as-is
            safe_tools.append(t)

    return safe_tools


# Build all calendar tools
calendar_tools = create_calendar_tools()
