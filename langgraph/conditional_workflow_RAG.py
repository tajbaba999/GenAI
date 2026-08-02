import os
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")

def build_retriver(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    document = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size = 800, chunk_overlap = 100)

    chunks = splitter.split_documents(document)

    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore.as_retriever(search_kwargs= {"k" : 4})


academic_retriver = build_retriver("academics_handbook.pdf")
fee_retriver = build_retriver("fee_structure.pdf")

llm = ChatGroq("llama-3.3-70b-versatile", temperature=0.4)