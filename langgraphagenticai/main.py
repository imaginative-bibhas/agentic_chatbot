import streamlit as st
from langgraphagenticai.src.ui.streamlitui.loadui import LoadStreamLitUI
from langgraphagenticai.src.llms.openai_llm import OpenAILLM
from langgraphagenticai.src.graph.graph_builder import GraphBuilder
from langgraphagenticai.src.ui.streamlitui.display_result import DisplayResultStreamlit

def load_langgraph_agenticai_app():
    """
    Loads and Runs the LangGraph AgenticAI application with StreamLit UI.
    This function indicates the UI, handles your input, configures the LLM Model, sets up
    the graph based on the selected usecase, and displays the output while implementing
    exception handling for robusteness.
    """
    #Load UI
    ui = LoadStreamLitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error. failed to load user input AI")
        return

    user_message = st.chat_input("Enter your message:")

    if st.session_state.IsFetchButtonClicked == True:
        user_message = st.session_state.timeframe

    if user_message:
        #Configure LLM
        try:
            obj_llm_config = OpenAILLM(user_control_input=user_input)
            model = obj_llm_config.get_llm_model()
            if not model:
                st.error("Error: LLM Model could not be initialized")
                return

            #Initialize and set up Graph based on use-case
            print("--Invoking selected_usecase--")
            usecase=user_input.get("selected_usecase")
            if not usecase:
                st.error("Error: No UseCase selected")

            #Graph Builder
            print("--Invoking GraphBuilder--")
            graph_builder=GraphBuilder(model)
            try:
                print("--Invoking setup_graph--")
                graph=graph_builder.setup_graph(usecase)
                print(f"graph {graph}")
                DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()

            except Exception as e:
                st.error(f"Error: Graph setup failed {e}")
                return

            print("Usecase:", usecase)
            print("Graph:", graph)
            print("Graph type:", type(graph))
        except Exception as e:
            st.error(f"Error: {e}")
            return
