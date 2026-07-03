import os

from utils.extractor import DocumentExtractor


class DocumentClassifier:

    def __init__(self):

        self.categories = {

            "AI Policy": [
                "artificial intelligence",
                "ai",
                "machine learning",
                "governance"
            ],

            "Finance": [
                "finance",
                "revenue",
                "profit",
                "budget",
                "expenses"
            ],

            "Sales": [
                "sales",
                "customer",
                "market",
                "product"
            ],

            "HR": [
                "employee",
                "leave",
                "benefits",
                "handbook",
                "policy"
            ],

            "Resume": [
                "experience",
                "skills",
                "education",
                "projects",
                "resume"
            ]
        }

    def classify(self, text):

        text = text.lower()

        scores = {}

        for category, words in self.categories.items():

            scores[category] = 0

            for word in words:

                if word in text:
                    scores[category] += 1

        best = max(scores, key=scores.get)

        if scores[best] == 0:
            return "General"

        return best

    def classify_folder(self, folder):

        results = {}

        for file in os.listdir(folder):

            path = os.path.join(folder, file)

            try:

                text = DocumentExtractor.extract(path)

                results[file] = self.classify(text)

            except Exception:

                continue

        return results