import streamlit as st
from src.pipelines.pipeline import run_research_pipeline

st.title("Multi Agent Research System using Langchain")

query = st.chat_input("Enter the topic you want a research report on!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

if query:
    st.chat_message("user").markdown(query)
    st.session_state.messages.append({"role" : "user", "content" : query})
    state = run_research_pipeline(query)
    final_response = f"{state['report']}\n{state['feedback']}"
    st.chat_message("agent").markdown(final_response)
    st.session_state.messages.append({"role" : "agent", "content" : final_response})


    