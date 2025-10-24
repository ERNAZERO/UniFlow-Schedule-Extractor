from langchain_ollama import ChatOllama
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from typing import List
from langchain_core.documents import Document


from app.core.config import settings

PROMPT = ChatPromptTemplate.from_messages([
("system", "Du bist Assistent. Antworte nur auf der Grundlage des Kontexts. Wenn es keine Antwort gibt, sag es einfach."),
("human", "Frage: {input}\nKontext:\n{context}")])


class LCPipeline:
    def __init__(self):
        self.llm = ChatOllama(
        base_url=settings.OLLAMA_BASE_URL,
        model=settings.OLLAMA_MODEL,
        temperature=settings.OLLAMA_TEMPERATURE,
        num_ctx=settings.OLLAMA_NUM_CTX,
        num_batch=settings.OLLAMA_NUM_BATCH,
        num_thread=settings.OLLAMA_NUM_THREAD,
        keep_alive="30m",)

        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=settings.BGE_MODEL_NAME,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    def extract_docs(self, file_path: str) -> List[Document]:
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
        docs = splitter.split_documents(pages)
        return docs

    def build_vectorstore(self, docs: List[Document]):
        vs = FAISS.from_documents(docs, self.embeddings)
        return vs

    def make_qa_chain(self, vectorstore):
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})
        doc_chain = create_stuff_documents_chain(self.llm, PROMPT)
        qa_chain = create_retrieval_chain(retriever, doc_chain)
        return qa_chain