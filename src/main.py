import asyncio
from src.agents.graph_builder import graph_builder, stream_response

from langchain.messages import AIMessage


async def main():
    graph = graph_builder()
    config = {"configurable": {"thread_id": "12345"}, "recursion_limit": 15}

    while True:
        user_input = input("User: ")
        if user_input.lower() in {"exit", "quit", "q", " "}:
            break

        user_input = {"chat_history": [{"role": "user", "content": user_input}]}
        print("Agent:", end=" ", flush=True)
        async for chunk in stream_response(graph, user_input, config):
            for node_name in chunk.keys():
                message = chunk[node_name]["chat_history"]
                # print(message.content, end=" ", flush=True)
                if isinstance(message, list):
                    for msg in message:
                        print(f"called tool: {msg.name}")

                if isinstance(message, AIMessage):
                    if message.content:
                        print(message.content, end=" ", flush=True)
        print()


if __name__ == "__main__":
    asyncio.run(main())
