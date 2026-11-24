#from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode, tools_condition

def get_tools():
    """
    Returns list of tools to be used in chatbot
    """
    tools=[TavilySearch(max_results=2)]
    return tools

def create_tool_node(tools):
    """
    Create and returns a tool node for the graph
    """
    return ToolNode(tools=tools)