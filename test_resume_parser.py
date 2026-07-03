from utils.extractor import DocumentExtractor
from utils.resume_parser import ResumeParser

file_path = "datasets/resumes/resume1.pdf"

text = DocumentExtractor.extract(file_path)

parser = ResumeParser()

result = parser.parse(text)

print("=" * 80)

for key, value in result.items():

    print(f"{key} : {value}")