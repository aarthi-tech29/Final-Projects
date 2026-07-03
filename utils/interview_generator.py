from utils.resume_parser import ResumeParser


class InterviewQuestionGenerator:

    def __init__(self):

        self.parser = ResumeParser()

    def generate_questions(self, resume_text):

        data = self.parser.parse(resume_text)

        questions = []

        # Skill-based questions
        for skill in data["Skills"]:

            questions.append(
                f"Explain your experience with {skill}."
            )

            questions.append(
                f"What projects have you completed using {skill}?"
            )

        # Education
        for education in data["Education"]:

            questions.append(
                f"How has your {education} helped prepare you for this role?"
            )

        # Experience
        if data["Experience"] != "Not Found":

            questions.append(
                f"You have {data['Experience']} of experience. What was your most challenging project?"
            )

            questions.append(
                "Describe a technical problem you solved recently."
            )

        # General HR questions
        questions.extend([
            "Tell me about yourself.",
            "Why do you want to join our company?",
            "Describe a challenging situation and how you handled it.",
            "Where do you see yourself in the next five years?",
            "What are your strengths and weaknesses?"
        ])

        return questions