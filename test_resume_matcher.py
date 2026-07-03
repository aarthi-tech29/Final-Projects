from utils.extractor import DocumentExtractor
from utils.resume_matcher import ResumeMatcher

resume = DocumentExtractor.extract(
    "datasets/resumes/resume1.pdf"
)

with open(
    "datasets/job_descriptions/data_scientist.txt",
    "r",
    encoding="utf-8"
) as f:

    jd = f.read()

matcher = ResumeMatcher()

result = matcher.calculate_score(
    resume,
    jd
)

print("=" * 80)

for key, value in result.items():

    print(f"{key}: {value}")