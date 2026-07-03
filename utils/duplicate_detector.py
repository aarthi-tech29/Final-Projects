import os

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from utils.extractor import DocumentExtractor


class DuplicateDetector:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def detect_duplicates(
        self,
        folder,
        threshold=0.80
    ):

        files = []

        texts = []

        for file in os.listdir(folder):

            path = os.path.join(folder, file)

            try:

                text = DocumentExtractor.extract(path)

                files.append(file)

                texts.append(text)

            except:

                pass

        embeddings = self.model.encode(texts)

        similarity = cosine_similarity(
            embeddings
        )

        duplicates = []

        n = len(files)

        for i in range(n):

            for j in range(i + 1, n):

                score = similarity[i][j]

                if score >= threshold:

                    duplicates.append({

                        "Document 1": files[i],

                        "Document 2": files[j],

                        "Similarity": round(
                            float(score),
                            2
                        )

                    })

        return duplicates