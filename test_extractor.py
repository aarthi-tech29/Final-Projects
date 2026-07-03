from utils.extractor import DocumentExtractor
import os

folder = "datasets/documents"

for file in os.listdir(folder):

    path = os.path.join(folder, file)

    print("=" * 60)
    print(file)
    print("=" * 60)

    text = DocumentExtractor.extract(path)

    print(text[:500])
    print()