import os
import fitz  # PyMuPDF
from docx import Document


class DocumentExtractor:

    @staticmethod
    def extract_pdf(file_path):
        text = ""

        pdf = fitz.open(file_path)

        for page in pdf:
            text += page.get_text()

        pdf.close()

        return text


    @staticmethod
    def extract_docx(file_path):

        doc = Document(file_path)

        text = []

        for para in doc.paragraphs:
            text.append(para.text)

        return "\n".join(text)


    @staticmethod
    def extract_txt(file_path):

        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()


    @staticmethod
    def extract(file_path):

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            return DocumentExtractor.extract_pdf(file_path)

        elif extension == ".docx":
            return DocumentExtractor.extract_docx(file_path)

        elif extension == ".txt":
            return DocumentExtractor.extract_txt(file_path)

        else:
            raise ValueError(f"Unsupported file type: {extension}")


    @staticmethod
    def save_text(text, output_path):

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)