from utils.extractor import DocumentExtractor
from utils.summarizer import DocumentSummarizer

file_path = "datasets/documents/ai_policy.pdf"

text = DocumentExtractor.extract(file_path)

summarizer = DocumentSummarizer()

summary = summarizer.summarize(text)

print("\nOriginal Text\n")
print(text)

print("\n" + "="*80)

print("\nSummary\n")
print(summary)