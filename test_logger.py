from utils.logger import AILogger

logger = AILogger()

logger.log(
    "Semantic Search",
    "AI Policy",
    "Found ai_policy.pdf"
)

logger.log(
    "Resume Screening",
    "resume1.pdf",
    "Score : 85%"
)

logger.log(
    "HR Chatbot",
    "What is leave policy?",
    "Employees receive 20 annual leaves."
)

print("=" * 70)
print("Logs Saved Successfully!")
print("=" * 70)