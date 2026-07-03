from utils.duplicate_detector import DuplicateDetector

detector = DuplicateDetector()

duplicates = detector.detect_duplicates(
    "datasets/documents"
)

print("=" * 80)
print("Duplicate Document Detection")
print("=" * 80)

if len(duplicates) == 0:

    print("\nNo duplicate documents found.")

else:

    for item in duplicates:

        print()

        print("Document 1 :", item["Document 1"])

        print("Document 2 :", item["Document 2"])

        print("Similarity :", item["Similarity"])

        print("-" * 70)