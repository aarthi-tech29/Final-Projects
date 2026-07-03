from utils.classifier import DocumentClassifier

classifier = DocumentClassifier()

results = classifier.classify_folder(
    "datasets/documents"
)

print("=" * 80)

for file, category in results.items():

    print(file)

    print("Category :", category)

    print("-" * 60)