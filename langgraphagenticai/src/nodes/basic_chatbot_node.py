 
from langgraphagenticai.src.state.state import State
class BasicChatbotNode:
    """
    Basic Chatbot login implementation
    """
    def __init__(self,model):
        self.llm=model

    def process(self,state:State)->dict:
        """
        Process the input state and generates a chatbot response.
        """
        print("--BasicChatbotNode.process--")
        response = self.llm.invoke(state["messages"])
        #return {"messages":self.llm.invoke(state['messages'])}
        return {
            "messages": [response]
        }
