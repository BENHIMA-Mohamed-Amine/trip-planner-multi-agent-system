from langchain.messages import SystemMessage

from src.core.workflow_state import WorkflowState
from src.core.models import model
from src.prompts.flight_prompt import FLIGHT_SEARCH_AGENT_PROMPT
from src.tools.flight_tool import flight_tools
from src.tools.handoff_tools import calendar_handoff_tool

def flight_search_agent(state: WorkflowState) -> None:
    """Flight search agent using Amadeus tools."""

    system_message = SystemMessage(content=FLIGHT_SEARCH_AGENT_PROMPT)
    chat_history = state.get("chat_history", [])
    prompt = [system_message] + chat_history

    tools = flight_tools + [calendar_handoff_tool]

    flight_model = model.bind_tools(tools)

    response = flight_model.invoke(prompt)

    return {"chat_history": response}
