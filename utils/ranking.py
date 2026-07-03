import os

from utils.extractor import DocumentExtractor
from utils.resume_matcher import ResumeMatcher


class CandidateRanking:

    def __init__(self):

        self.matcher = ResumeMatcher()

    def rank_candidates(self, resume_folder, job_description):

        rankings = []

        for file in os.listdir(resume_folder):

            if not file.lower().endswith((".pdf", ".docx", ".txt")):
                continue

            path = os.path.join(resume_folder, file)

            resume_text = DocumentExtractor.extract(path)

            result = self.matcher.calculate_score(
                resume_text,
                job_description
            )

            rankings.append({

                "Resume": file,

                "Score": result["Score"],

                "Matched Skills": result["Matched Skills"],

                "Missing Skills": result["Missing Skills"]

            })

        rankings = sorted(
            rankings,
            key=lambda x: x["Score"],
            reverse=True
        )

        return rankings