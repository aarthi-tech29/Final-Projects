import os

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from utils.extractor import DocumentExtractor


class EmbeddingManager:

    def __init__(self):

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vector_db = None

    def build_vector_database(self, folder="datasets/documents"):

        docs = []

        for file in os.listdir(folder):

            path = os.path.join(folder, file)

            text = DocumentExtractor.extract(path)

            docs.append(
                Document(
                    page_content=text,
                    metadata={"source": file}
                )
            )

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        split_docs = splitter.split_documents(docs)

        self.vector_db = FAISS.from_documents(
            split_docs,
            self.embedding_model
        )

        self.vector_db.save_local("vector_db")

        print("Vector Database Created Successfully!")

    def load_vector_database(self):

        self.vector_db = FAISS.load_local(
            "vector_db",
            self.embedding_model,
            allow_dangerous_deserialization=True
        )

    def similarity_search(self, query, k=3):

        if self.vector_db is None:
            self.load_vector_database()

        return self.vector_db.similarity_search(query, k=k)