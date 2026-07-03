import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

UPLOAD_FOLDER = "uploads"
TEXT_FOLDER = "extracted_text"
SUMMARY_FOLDER = "summaries"
EXPORT_FOLDER = "exports"
VECTOR_FOLDER = "vector_db"
LOG_FOLDER = "logs"

for folder in [
    UPLOAD_FOLDER,
    TEXT_FOLDER,
    SUMMARY_FOLDER,
    EXPORT_FOLDER,
    VECTOR_FOLDER,
    LOG_FOLDER,
]:
    os.makedirs(folder, exist_ok=True)