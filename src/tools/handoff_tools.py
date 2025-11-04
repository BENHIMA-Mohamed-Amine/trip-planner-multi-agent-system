from langgraph_supervisor import create_handoff_tool

# Handoff tool for transferring TO the calendar agent
calendar_handoff_tool = create_handoff_tool(
    agent_name="calendar_agent",  # Must match the node name in your graph
    name="transfer_to_calendar_agent",  # Explicit tool name (optional, but good for clarity)
    description="Transfer control to the calendar agent when the user needs help with scheduling, viewing calendar events, managing appointments, setting reminders, or any calendar-related tasks. Use this when flight searches are complete and the user wants to add travel dates to their calendar.",
    add_handoff_messages=True,  # Keep handoff messages in history for context continuity
)

# Handoff tool for transferring TO the flight search agent
flight_handoff_tool = create_handoff_tool(
    agent_name="flight_search_agent",  # Must match the node name in your graph
    name="transfer_to_flight_search_agent",  # Explicit tool name (optional, but good for clarity)
    description="Transfer control to the flight search agent when the user needs to search for flights, check flight availability, compare flight options, get flight prices, or handle any flight booking related queries. Use this when calendar tasks involve travel and need flight information.",
    add_handoff_messages=True,  # Keep handoff messages in history for context continuity
)
