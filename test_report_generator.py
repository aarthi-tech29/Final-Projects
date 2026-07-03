from utils.report_generator import ReportGenerator
from utils.extractor import DocumentExtractor
from utils.summarizer import DocumentSummarizer

text = DocumentExtractor.extract(
    "datasets/documents/sales_report.pdf"
)

summary = DocumentSummarizer().summarize(text)

generator = ReportGenerator()

file = generator.generate_report(
    title="Sales Report Analysis",
    summary=summary
)

print("=" * 80)
print("Report Generated Successfully")
print(file)