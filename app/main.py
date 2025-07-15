import PyPDF2
import streamlit as st
from agent import ResumeAgent
from dotenv import load_dotenv

load_dotenv()

st.title("CandidateAgent")

def pdf_to_text(file) -> str:
    """Extract text from an uploaded PDF file."""
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

with st.expander("Candidate Details", expanded=True):
    with st.form(key="input_form"):
        resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
        website = st.text_input("Website URL")
        github = st.text_input("GitHub Link")
        story = st.text_area("Personal Story")
        prompts = st.text_area("Helpful Prompts for the Recruiter")
        submitted = st.form_submit_button("Submit")

if submitted:
    resume_text = ""
    if resume_file is not None:
        resume_text = pdf_to_text(resume_file)
    combined = "\n\n".join(filter(None, [resume_text, website, github, story, prompts]))

    st.session_state['inputs'] = {
        'website': website,
        'github': github,
        'story': story,
        'prompts': prompts,
        'resume_text': resume_text,
    }
    st.session_state['agent'] = ResumeAgent(resume_text=combined)
    st.success("ResumeAgent created.")

if 'agent' in st.session_state:
    user_input = st.text_input("Ask about the candidate:")
    if st.button('Ask') and user_input:
        response = st.session_state['agent'].ask(user_input)
        st.write(response)
