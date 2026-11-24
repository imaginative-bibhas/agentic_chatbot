import os
import streamlit as st
from langchain_openai import ChatOpenAI

class OpenAILLM:
    def __init__(self,user_control_input):
        self.user_control_input=user_control_input

    
    def get_llm_model(self):
        try:
            print("--get_llm_model--")
            api_key=self.user_control_input["API_KEY"]
            selected_model=self.user_control_input["selected_model"]

            os.environ["OPENAI_API_KEY"] = api_key
            if api_key=='' and os.environ['API_KEY']=='':
                st.error('No API Key provided')

            print("--Invoking ChatOpenAI--")
            llm=ChatOpenAI(model=selected_model,temperature=0)
        except Exception as e:
            raise ValueError(f"Exception occrred: {e}")

        return llm