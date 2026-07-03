from utils.ranking import CandidateRanking

with open(
    "datasets/job_descriptions/data_scientist.txt",
    "r",
    encoding="utf-8"
) as f:

    jd = f.read()

ranking = CandidateRanking()

results = ranking.rank_candidates(
    "datasets/resumes",
    jd
)

print("=" * 100)
print("Candidate Ranking")
print("=" * 100)

for i, candidate in enumerate(results, start=1):

    print(f"\nRank {i}")

    print("Resume :", candidate["Resume"])

    print("Score :", candidate["Score"])

    print("Matched Skills :", candidate["Matched Skills"])

    print("Missing Skills :", candidate["Missing Skills"])

    print("-" * 100)