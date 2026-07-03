from utils.extractor import DocumentExtractor
from utils.interview_generator import InterviewQuestionGenerator

resume = DocumentExtractor.extract(
    "datasets/resumes/resume1.pdf"
)

generator = InterviewQuestionGenerator()

questions = generator.generate_questions(resume)

print("=" * 80)
print("Interview Questions")
print("=" * 80)

for i, question in enumerate(questions, start=1):

    print(f"{i}. {question}")