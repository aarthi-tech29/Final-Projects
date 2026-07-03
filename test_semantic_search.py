from utils.semantic_search import SemanticSearch

search = SemanticSearch()

query = input("Enter Search Query: ")

results = search.search(query)

print("\n")
print("=" * 80)
print("SEARCH RESULTS")
print("=" * 80)

for i, doc in enumerate(results, start=1):

    print(f"\nResult {i}")

    print("Source :", doc.metadata["source"])

    print()

    print(doc.page_content)

    print("-" * 80)