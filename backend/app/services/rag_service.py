import pandas as pd
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings 
from langchain_community.vectorstores import Chroma
from app.core.config import settings

class RAGService:
    @staticmethod
    def load_files(file_paths: list):
        docs = []
        dataframes = []
        
        for path in file_paths:
            if path.endswith(".pdf"):
                docs.extend(PyPDFLoader(path).load())
            elif path.endswith(".txt"):
                try:
                    docs.extend(TextLoader(path, encoding='utf-8').load())
                except UnicodeDecodeError:
                    docs.extend(TextLoader(path, encoding='latin-1').load())
            elif path.endswith(".csv"):
                try:
                    df = pd.read_csv(path, encoding='utf-8')
                except UnicodeDecodeError:
                    df = pd.read_csv(path, encoding='latin-1')
                dataframes.append(df)
            elif path.endswith(".xlsx"):
                dataframes.append(pd.read_excel(path))
                
        return docs, dataframes

    @staticmethod
    def create_vector_store(docs):
        if not docs: return None
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = splitter.split_documents(docs)
        return Chroma.from_documents(
            documents=splits,
            embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
            persist_directory=settings.CHROMA_PERSIST_DIR
        )