# CandidateAgent

CandidateAgent is a prototype LLM-powered resume assistant. Recruiters can chat with the agent to learn more about Nikhil Racha's experience and technical background. The app uses OpenAI's GPT models with LangChain to answer questions based on an embedded copy of the candidate's resume.

## Architecture
- **Streamlit UI** – simple chat interface
- **LangChain** – loads and queries resume data
- **Vector Store** – FAISS for similarity search
- **Prompt Template** – customize the assistant's tone
- **Dockerized** – ready for container deployment

## Setup
1. Install Python 3.10+
2. `pip install -r requirements.txt`
3. Create a `.env` file in the project root and add your API key (this file is already listed in `.gitignore`):
   ```
   OPENAI_API_KEY=sk-...
   ```
   Alternatively export the variable in your shell with `export OPENAI_API_KEY=sk-...`.
4. `streamlit run app/main.py`

## Docker
Build and run the app in Docker:
```bash
docker build -t candidate-agent .
docker run -p 8501:8501 -e OPENAI_API_KEY=sk-... candidate-agent
```

## Next Steps
- Add authentication for recruiter sessions
- Support multiple resumes/candidates
- Switch vector store to Chroma
- Deploy to a cloud service for easier access
