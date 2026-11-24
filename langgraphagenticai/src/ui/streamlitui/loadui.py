import streamlit as st
import os

from langgraphagenticai.src.ui.uiconfig import Config

class LoadStreamLitUI:
    def __init__(self):
        self.config = Config()
        self.user_control = {}

    def load_streamlit_ui(self):
        st.set_page_config(page_title="🧠 " + self.config.get_page_title(),layout="wide")
        st.header("🧠 " + self.config.get_page_title())
        st.session_state.IsFetchButtonClicked =False
        st.session_state.timeframe =''

        with st.sidebar:
            # Get Options from Config file
            llm_options = self.config.get_llm_options()
            use_case_options = self.config.get_usecase_options()

            #LLM Options
            self.user_control["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_control["selected_llm"] == "Groq":
                # Model Selections
                model_options = self.config.get_model_options()
                self.user_control["selected_model"] = st.selectbox("Select Model", model_options)
                self.user_control["API_KEY"] = st.session_state["API_KEY"] = st.text_input("API_KEY", type="password")

                #Validate API Key
                if not self.user_control["API_KEY"]:
                    st.warning("Please enter your API Key to proceed")
            elif self.user_control["selected_llm"] == "ChatGPT":
                # Model Selections
                model_options = self.config.get_model_options()
                self.user_control["selected_model"] = st.selectbox("Select Model", model_options)
                self.user_control["API_KEY"] = st.session_state["API_KEY"] = st.text_input("API_KEY", type="password")
            
                #Validate API Key
                if not self.user_control["API_KEY"]:
                    st.warning("Please enter your API Key to proceed")

            #Usecase Selection
            self.user_control["selected_usecase"] = st.selectbox("Select Usecases", use_case_options)

            if self.user_control["selected_usecase"] == 'Chatbot with Web' or self.user_control["selected_usecase"] == 'AI News':
                self.user_control["TAVILY_API_KEY"]=st.session_state['TAVILY_API_KEY']=st.text_input("TAVILY_API_KEY",type="password")

                #Validate API Key
                if not self.user_control["TAVILY_API_KEY"]:
                    st.warning("Please enter your TAVILY API Key to proceed")
                else:
                    os.environ["TAVILY_API_KEY"] = self.user_control["TAVILY_API_KEY"]

            if self.user_control["selected_usecase"] == 'AI News':
                st.subheader("\U0001F50D AI News Explorer")
                with st.sidebar:
                    time_frame = st.selectbox(
                        "📅select time frame",
                        ["Daily","Weekly","Monthly"],
                        index=0
                    )

                if st.button("\U0001F50D Fetch latest AI News", use_container_width=True):
                    st.session_state.timeframe=time_frame
                    st.session_state.IsFetchButtonClicked = True

        return self.user_control
