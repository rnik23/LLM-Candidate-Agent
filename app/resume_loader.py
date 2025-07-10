from pathlib import Path
from typing import List
from langchain.docstore.document import Document
import PyPDF2


def load_resume(path: Path) -> List[Document]:
    """Load resume PDF and return list of Documents."""
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return [Document(page_content=text)]
