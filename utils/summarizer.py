from transformers import pipeline


class DocumentSummarizer:

    def __init__(self):

        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn"
        )

    def summarize(self, text):

        text = text.strip()

        if len(text) == 0:
            return "No text found."

        # Hugging Face models accept limited input length
        if len(text) > 3000:
            text = text[:3000]

        summary = self.summarizer(
            text,
            max_length=150,
            min_length=50,
            do_sample=False
        )

        return summary[0]["summary_text"]