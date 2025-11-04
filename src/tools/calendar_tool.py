from langchain_google_community import CalendarToolkit

def create_calendar_tools():
    toolkit = CalendarToolkit()
    tools = toolkit.get_tools()
    # print("calender toolkit tools")
    # for tool in tools:
    #     print(tool.get_name())
    #     print(tool.args)
    #     print(10 * "-")
    return tools


calendar_tools = create_calendar_tools()