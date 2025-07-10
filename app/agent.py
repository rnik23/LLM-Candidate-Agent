from pathlib import Path
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

from resume_loader import load_resume

class ResumeAgent:
    def __init__(self, resume_path: str = "data/resume.pdf", prompt_path: str = "app/prompt_template.txt"):
        self.db = self._build_vector_store(resume_path)
        self.chain = self._build_chain(prompt_path)

    def _build_vector_store(self, resume_path: str):
        documents = load_resume(Path(resume_path))
        embeddings = OpenAIEmbeddings()
        return FAISS.from_documents(documents, embeddings)

    def _build_chain(self, prompt_path: str):
        llm = ChatOpenAI(temperature=0)
        retriever = self.db.as_retriever()
        with open(prompt_path, 'r') as f:
            system_prompt = f.read()
        return RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": system_prompt},
        )

    def ask(self, question: str) -> str:
        result = self.chain.run(question)
        return result
