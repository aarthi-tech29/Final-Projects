from utils.extractor import DocumentExtractor
from utils.resume_parser import ResumeParser


class ResumeMatcher:

    def __init__(self):

        self.parser = ResumeParser()

    def calculate_score(self, resume_text, job_description):

        resume = self.parser.parse(resume_text)

        resume_skills = set(
            skill.lower() for skill in resume["Skills"]
        )

        jd_skills = set()

        common_skills = [
            "Python",
            "Java",
            "SQL",
            "Machine Learning",
            "Deep Learning",
            "NLP",
            "AWS",
            "Azure",
            "Spark",
            "Docker",
            "Kubernetes",
            "Git",
            "Linux",
            "Power BI",
            "Tableau",
            "LangChain",
            "FAISS",
            "OpenAI",
            "TensorFlow",
            "PyTorch"
        ]

        jd_lower = job_description.lower()

        for skill in common_skills:

            if skill.lower() in jd_lower:
                jd_skills.add(skill.lower())

        matched = resume_skills.intersection(jd_skills)

        if len(jd_skills) == 0:
            score = 0
        else:
            score = round(
                len(matched) / len(jd_skills) * 100,
                2
            )

        return {
            "Score": score,
            "Matched Skills": sorted(list(matched)),
            "Missing Skills": sorted(list(jd_skills - matched))
        }