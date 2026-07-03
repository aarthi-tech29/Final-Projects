from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_huggingface import HuggingFacePipeline

from transformers import pipeline

from utils.embeddings import EmbeddingManager


class DocumentQA:

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
You are an AI assistant.

Answer ONLY using the given context.

If the answer is not found, reply:

"I couldn't find the answer in the uploaded documents."

Context:
{context}

Question:
{question}

Answer:
"""
        )

        self.chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(self, question):

        docs = self.embedding_manager.similarity_search(
            question,
            k=3
        )

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        answer = self.chain.invoke(
            {
                "context": context,
                "question": question
            }
        )

        return answer