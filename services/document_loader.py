import os
from langchain_community.document_loaders import PyPDFLoader

def load_documents():
    docs = []
    for file in os.listdir("data/nvidia_docs"):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(f"data/nvidia_docs/{file}")
            docs.extend(loader.load())
    return docs
