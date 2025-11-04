from amadeus import Client
from langchain_community.agent_toolkits.amadeus.toolkit import AmadeusToolkit
from langchain_community.tools.amadeus.closest_airport import AmadeusClosestAirport
from langchain_community.tools.amadeus.flight_search import AmadeusFlightSearch

from src.core.config import AMADEUS_CLIENT_ID, AMADEUS_CLIENT_SECRET
from src.core.models import model


def create_flight_tools():
    """Initialize and return Amadeus flight tools."""

    # Create namespace with Client class
    namespace = {"Client": Client}

    # Rebuild all Amadeus tool classes with the namespace
    AmadeusToolkit.model_rebuild(_types_namespace=namespace)
    AmadeusClosestAirport.model_rebuild(_types_namespace=namespace)
    AmadeusFlightSearch.model_rebuild(_types_namespace=namespace)

    # Create the client
    client = Client(client_id=AMADEUS_CLIENT_ID, client_secret=AMADEUS_CLIENT_SECRET, hostname="test")

    # Create toolkit
    toolkit = AmadeusToolkit(llm=model, client=client)
    tools = toolkit.get_tools()

    # for tool in tools:
    #     print(f"\nTool Name: {tool.name}")
    #     print(f"Description: {tool.description}")
    #     print(f"Arguments Schema: {tool.args}")
    #     # You can also access:
    #     # print(f"Args Schema Type: {tool.args_schema}")
    #     print("-" * 50)

    # response = client.shopping.flight_offers_search.get(
    #     originLocationCode="NYC",
    #     destinationLocationCode="LAX",
    #     departureDate="2025-12-01",
    #     adults=1,
    # )

    # print(f"Found {len(response.data)} flight offers")

    return tools

flight_tools = create_flight_tools()
