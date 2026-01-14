from langgraph.graph import StateGraph, START, END
from langgraph.pregel import Pregel
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode

from src.core.workflow_state import WorkflowState
from .flight_search_agent import flight_search_agent
from .calendar_agent import calendar_agent
from src.tools.calendar_tool import calendar_tools
from src.tools.flight_tool import flight_tools


def should_continue(state: WorkflowState) -> str:
    last_message = state.get("chat_history", [])[-1]
    # print("Last message:", last_message)
    if last_message.tool_calls:
        for tool_call in last_message.tool_calls:
            if tool_call["name"] == "transfer_to_calendar_agent":
                return "calendar_agent"
            if tool_call["name"] == "transfer_to_flight_search_agent":
                return "flight_search_agent"

        return "tools"
    else:
        return "end"


def intial_routing_condition(state: WorkflowState) -> str:
    last_node = state.get("last_node", None)
    if last_node == "calendar_agent":
        return "calendar_agent"
    else:
        return "flight_search_agent"


def graph_builder() -> Pregel:
    """Graph builder to construct knowledge graph from user inputs."""

    checkpointer = InMemorySaver()
    graph = StateGraph(WorkflowState)

    graph.add_node(flight_search_agent)
    graph.add_node(calendar_agent)
    graph.add_node(
        ToolNode(
            tools=calendar_tools,
            name="calendar_tools",
            messages_key="chat_history",
            handle_tool_errors=False,
        )
    )
    graph.add_node(
        ToolNode(
            tools=flight_tools,
            name="flight_tools",
            messages_key="chat_history",
            handle_tool_errors=False,
        )
    )

    graph.add_conditional_edges(
        START,
        intial_routing_condition,
        {
            "flight_search_agent": "flight_search_agent",
            "calendar_agent": "calendar_agent",
        }
    )
    graph.add_conditional_edges(
        "flight_search_agent",
        should_continue,
        {
            "tools": "flight_tools",
            "calendar_agent": "calendar_agent",
            "end": END,
        },
    )
    graph.add_edge("flight_tools", "flight_search_agent")

    graph.add_conditional_edges(
        "calendar_agent",
        should_continue,
        {
            "tools": "calendar_tools",
            "flight_search_agent": "flight_search_agent",
            "end": END,
        },
    )
    graph.add_edge("calendar_tools", "calendar_agent")
    graph = graph.compile(checkpointer=checkpointer)

    return graph


async def stream_response(graph: Pregel, state: dict, config: dict):
    """Stream response from the graph based on user input."""

    async for mode, chunck in graph.astream(
        input=state, config=config, stream_mode=["updates", "custom"]
    ):
        if mode == "updates":
            yield chunck
