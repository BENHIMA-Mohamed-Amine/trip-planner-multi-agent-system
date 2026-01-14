from src.tools.calendar_tool import calendar_tools
from src.tools.handoff_tools import flight_handoff_tool
from src.core.models import model
from src.core.workflow_state import WorkflowState
from src.prompts.calendar_prompt import CALENDAR_AGENT_PROMPT

from langchain.messages import SystemMessage


def calendar_agent(state: WorkflowState):
    system_message = SystemMessage(content=CALENDAR_AGENT_PROMPT)

    prompt = state.get("chat_history", []) + [system_message]

    tools = calendar_tools + [flight_handoff_tool]
    calendar_model = model.bind_tools(tools)

    response = calendar_model.invoke(prompt)

    return {"chat_history": response, "last_node": "calendar_agent"}
