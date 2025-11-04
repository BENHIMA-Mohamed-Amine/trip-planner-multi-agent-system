from src.agents.graph_builder import graph_builder

from langchain.messages import AIMessage

def main():
    graph = graph_builder()
    config = {"configurable": {"thread_id": "12345"}}
    while True:
        user_input = input("User: ")
        if user_input.lower() in {"exit", "quit", "q", " "}:
            break
        
        user_input = {"chat_history": [{"role": "user", "content": user_input}]}
        response = graph.invoke(user_input, config=config)
        if isinstance(response.get("chat_history", [])[-1], AIMessage):
            ai_response = response.get("chat_history", [])[-1].content
            print(f"Agent: {ai_response}")


if __name__ == "__main__":
    main()
