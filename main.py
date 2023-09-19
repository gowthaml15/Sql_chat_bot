import streamlit as st
import psycopg2
import sqlite3
import openai
import os
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# App title
st.set_page_config(page_title="🤖 Chat with GPT-3")

# User-provided OpenAI API key
openai_api_key = st.text_input("Enter your OpenAI API key:", type="password")

# Function for generating GPT-3 response
def generate_response(prompt_input, api_key):
    if not api_key:
        st.error("Please enter your OpenAI API key.")
        return
    db = SQLDatabase.from_uri(f'postgresql+psycopg2://aija:Adm!nAj!a@aija-rds-postgres.cyh5e1oowekp.us-east-1.rds.amazonaws.com/aija')
    # openai.api_key = api_key
    os.environ['OPENAI_API_KEY'] = api_key
    llm = OpenAI(temperature=0, verbose=True)
    toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0))
    agent_executor = create_sql_agent(
        llm=OpenAI(temperature=0),
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )
    
    return agent_executor(prompt_input)

# Initialize conversation history
conversation_history = []

# User-provided prompt
prompt = st.text_area("You:", "Hi, GPT-3!")

# Chatbot response and conversation history
if st.button("Send"):
    if prompt:
        conversation_history.append(("User", prompt))
        with st.spinner("Thinking..."):
            response = generate_response(prompt, openai_api_key)
        conversation_history.append(("GPT-3", response))
        st.text_area("Conversation:", value="\n".join([f"{role}: {message}" for role, message in conversation_history]), height=300)

# Example or instructions
st.markdown("💡 **Tip:** You can start the conversation with a greeting or question.")
st.markdown("📖 Learn more about how to create the OpenAI GPT-3 API Key [here](https://www.awesomescreenshot.com/blog/knowledge/chat-gpt-api).")
