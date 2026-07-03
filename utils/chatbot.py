from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_huggingface import HuggingFacePipeline

from transformers import pipeline

from utils.embeddings import EmbeddingManager


class HRChatbot:

    def __init__(self):

        self.embedding_manager = EmbeddingManager()

        self.embedding_manager.load_vector_database()

        pipe = pipeline(
            task="text2text-generation",
            model="google/flan-t5-base",
            max_new_tokens=256,
            do_sample=False
        )

        self.llm = HuggingFacePipeline(
            pipeline=pipe
        )

        self.prompt = ChatPromptTemplate.from_template(
"""
You are an HR Assistant.

Answer only from the company documents.

If the answer is unavailable, reply:

I couldn't find that information in the uploaded HR documents.

Context:
{context}

Employee Question:
{question}

Answer:
"""
        )

        self.chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )

    def chat(self, question):

        docs = self.embedding_manager.similarity_search(
            question,
            k=4
        )

        context = "\n\n".join(
            doc.page_content for doc in docs
        )

        return self.chain.invoke(
            {
                "context": context,
                "question": question
            }
        )