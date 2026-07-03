from utils.embeddings import EmbeddingManager

def main():

    manager = EmbeddingManager()

    # Build the vector database
    manager.build_vector_database()

    print("\nVector Database Created Successfully!\n")

    print("Testing Similarity Search...\n")

    results = manager.similarity_search(
        "AI policy",
        k=3
    )

    for i, doc in enumerate(results, start=1):

        print("=" * 70)
        print(f"Result {i}")
        print("Source :", doc.metadata["source"])
        print()
        print(doc.page_content[:400])
        print()

if __name__ == "__main__":
    main()