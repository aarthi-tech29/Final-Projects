import re
import spacy

nlp = spacy.load("en_core_web_sm")


class ResumeParser:

    def __init__(self):

        self.skills = [
            "Python", "Java", "SQL", "Machine Learning",
            "Deep Learning", "NLP", "Power BI", "Tableau",
            "Spark", "AWS", "Azure", "Docker",
            "Kubernetes", "Git", "Linux",
            "TensorFlow", "PyTorch", "Pandas",
            "NumPy", "Scikit-learn", "LangChain",
            "FAISS", "OpenAI"
        ]

    def extract_text(self, text):

        return nlp(text)

    def extract_skills(self, text):

        found = []

        lower_text = text.lower()

        for skill in self.skills:

            if skill.lower() in lower_text:
                found.append(skill)

        return sorted(list(set(found)))

    def extract_email(self, text):

        emails = re.findall(
            r'[\w\.-]+@[\w\.-]+\.\w+',
            text
        )

        return emails[0] if emails else ""

    def extract_phone(self, text):

        phones = re.findall(
            r'\+?\d[\d\s\-]{8,15}',
            text
        )

        return phones[0] if phones else ""

    def extract_education(self, text):

        education = []

        keywords = [
            "B.Tech",
            "B.E",
            "M.Tech",
            "M.E",
            "MBA",
            "B.Sc",
            "M.Sc",
            "Bachelor",
            "Master",
            "PhD"
        ]

        for key in keywords:

            if key.lower() in text.lower():
                education.append(key)

        return education

    def extract_experience(self, text):

        exp = re.findall(
            r'(\d+)\+?\s+years?',
            text,
            re.IGNORECASE
        )

        if exp:
            return exp[0] + " Years"

        return "Not Found"

    def parse(self, text):

        return {

            "Email": self.extract_email(text),

            "Phone": self.extract_phone(text),

            "Skills": self.extract_skills(text),

            "Education": self.extract_education(text),

            "Experience": self.extract_experience(text)

        }