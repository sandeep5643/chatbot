from langchain_community.vectorstores import FAISS
from services.embedding_service import embedding

def build_vector_db(docs):
    return FAISS.from_documents(docs, embedding)
