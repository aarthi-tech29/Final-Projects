import os
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate


class ReportGenerator:

    def __init__(self):

        self.styles = getSampleStyleSheet()

    def generate_report(
        self,
        title,
        summary,
        output_file="reports/business_report.pdf"
    ):

        # Automatically create folder
        os.makedirs(
            os.path.dirname(output_file),
            exist_ok=True
        )

        doc = SimpleDocTemplate(output_file)

        story = []

        story.append(
            Paragraph(title, self.styles["Heading1"])
        )

        story.append(
            Paragraph(
                f"<b>Generated:</b> {datetime.now()}",
                self.styles["Normal"]
            )
        )

        story.append(
            Paragraph("<br/><br/>", self.styles["Normal"])
        )

        story.append(
            Paragraph(summary, self.styles["BodyText"])
        )

        doc.build(story)

        return output_file