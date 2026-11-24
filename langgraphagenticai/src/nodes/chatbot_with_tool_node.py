from langgraphagenticai.src.state.state import State


class ChatBotToolNode:
    """
    Chatbot logic enhanced with tool integration.
    """

    def __init__(self, model):
        self.llm = model

    def create_chatbot(self, tools):
        """
        Creates a chatbot node with tool capabilities.
        """

        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State):
            """
            Processes messages and generates an AI response.
            The AI may respond normally or request a tool call.
            """

            print("--ChatBotToolNode.chatbot_node--")

            response = llm_with_tools.invoke(state["messages"])

            return {
                "messages": [response]
            }

        return chatbot_node