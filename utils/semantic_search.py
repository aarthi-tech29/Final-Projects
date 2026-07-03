from utils.embeddings import EmbeddingManager


class SemanticSearch:

    def __init__(self):

        self.embedding_manager = EmbeddingManager()

        self.embedding_manager.load_vector_database()

    def search(self, query, top_k=3):

        return self.embedding_manager.similarity_search(
            query=query,
            k=top_k
        )