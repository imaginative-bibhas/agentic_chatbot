from langgraph.graph import StateGraph
from langgraphagenticai.src.state.state import State
from langgraph.graph import START, END

from langgraphagenticai.src.nodes.basic_chatbot_node import BasicChatbotNode
from langgraphagenticai.src.nodes.chatbot_with_tool_node import ChatBotToolNode
from langgraphagenticai.src.nodes.ai_news_node import AINewsNode
from langgraphagenticai.src.tools.search_tool import get_tools,create_tool_node,tools_condition
from langgraph.prebuilt import tools_condition,ToolNode

class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)

        self.basic_chatbot_node=BasicChatbotNode(self.llm)

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using LangGraph. This method initializes a chatbot node using the
        'BasicChatbotNode' class and integrates it into the graph. The chatbot is set as both the
        entry and exit point of the Graph.        
        """
        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot",END)

        graph = self.graph_builder.compile()
        return graph

    def chatbot_with_tools_build_graph(self):
        """
        Builds an advanced chatbot graph with tool integration.
        This method creates a chatbot graph that includes both a chatbot node
        and a tool node. It defines tools, initializes the chatbot with tool
        capabilities, and sets up conditional and direct edges between nodes.
        The chatbot node is set as the entry point.
        """
        ## Define the tool and tools
        tools=get_tools()
        tool_node=create_tool_node(tools)

        ## Define LLM
        llm=self.llm

        ## Define the chatbot node
        obj_chatbot_with_node=ChatBotToolNode(llm)
        chatbot_node=obj_chatbot_with_node.create_chatbot(tools)

        ## Add nodes
        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)
        ## Define conditional and direct edges
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools","chatbot")
        #self.graph_builder.add_edge("chatbot",END) #May not need to write

        graph = self.graph_builder.compile()
        return graph

    def ai_news_builder_graph(self):
        #AI News
        print("--ai_news_builder_graph--")
        ai_news_node = AINewsNode(self.llm)

        self.graph_builder.add_node("fetch_news",ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news",ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result",ai_news_node.save_result)

        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news","summarize_news")
        self.graph_builder.add_edge("summarize_news","save_result")
        self.graph_builder.add_edge("save_result",END)

        graph = self.graph_builder.compile()
        return graph

                

    def setup_graph(self, usecase: str):
        """
        Sets up the Graph for selected usecase
        """
        print(f"usecase '{usecase}'")
        if usecase == "Basic Chatbot":
            graph=self.basic_chatbot_build_graph()
            return graph

        if usecase == "Chatbot with Web":
            graph=self.chatbot_with_tools_build_graph()
            return graph

        if usecase == "AI News":
            graph = self.ai_news_builder_graph()
            return graph

        return self.graph_builder.compile()
