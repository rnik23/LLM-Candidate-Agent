import streamlit as st
from agent import ResumeAgent

st.title("CandidateAgent")

# Initialize agent
if 'agent' not in st.session_state:
    st.session_state['agent'] = ResumeAgent()

user_input = st.text_input("Ask about Nikhil Racha's experience:")
if st.button('Submit') and user_input:
    response = st.session_state['agent'].ask(user_input)
    st.write(response)
