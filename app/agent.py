from pathlib import Path
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


from langchain.docstore.document import Document
from resume_loader import load_resume

class ResumeAgent:
    def __init__(self, resume_path: str = "data/My_Resume_Nikhil_Racha_K.pdf", prompt_path: str = "app/prompt_template.txt", resume_text: str | None = None):
        self.db = self._build_vector_store(resume_path, resume_text)
        self.chain = self._build_chain(prompt_path)

    def _build_vector_store(self, resume_path: str, resume_text: str | None = None):
        if resume_text is not None:
            documents = [Document(page_content=resume_text)]
        else:
            documents = load_resume(Path(resume_path))
        embeddings = OpenAIEmbeddings()
        return FAISS.from_documents(documents, embeddings)

    def _build_chain(self, prompt_path: str):
        llm = ChatOpenAI(temperature=0)
        retriever = self.db.as_retriever()

        with open(prompt_path, 'r') as f:
            system_prompt = f.read()

        prompt = PromptTemplate(
            input_variables=["context", "question"],  # Most RetrievalQA chains use these
            template=system_prompt
        )

        return RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": prompt},
        )

    def ask(self, question: str) -> str:
        result = self.chain.run(question)
        return result
