import streamlit as st
import os
import shutil
import pandas as pd

from utils.extractor import DocumentExtractor
from utils.summarizer import DocumentSummarizer
from utils.semantic_search import SemanticSearch
from utils.qa import DocumentQA
from utils.resume_matcher import ResumeMatcher
from utils.ranking import CandidateRanking
from utils.interview_generator import InterviewQuestionGenerator
from utils.chatbot import HRChatbot
from utils.report_generator import ReportGenerator
from utils.classifier import DocumentClassifier
from utils.duplicate_detector import DuplicateDetector
from utils.logger import AILogger


st.set_page_config(
    page_title="Enterprise AI Document Intelligence",
    page_icon="📄",
    layout="wide"
)

logger = AILogger()

st.title("📄 Enterprise AI Document Intelligence & Resume Screening Platform")

st.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Upload Documents",
        "AI Summarizer",
        "Semantic Search",
        "Question Answering",
        "Resume Screening",
        "Candidate Ranking",
        "Interview Questions",
        "HR Chatbot",
        "Business Reports",
        "Document Classification",
        "Duplicate Documents",
        "AI Logs"
    ]
)
if menu == "Dashboard":

    st.header("Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    documents = len(os.listdir("datasets/documents"))
    resumes = len(os.listdir("datasets/resumes"))

    col1.metric("Documents", documents)
    col2.metric("Resumes", resumes)
    col3.metric("Job Descriptions", len(os.listdir("datasets/job_descriptions")))

    try:
        logs = pd.read_csv("logs/ai_logs.csv")
        col4.metric("AI Logs", len(logs))
    except:
        col4.metric("AI Logs", 0)

    st.markdown("---")

    st.subheader("Project Features")

    st.success("✔ AI Document Processing")
    st.success("✔ Resume Screening")
    st.success("✔ Semantic Search")
    st.success("✔ Question Answering")
    st.success("✔ HR Chatbot")
    st.success("✔ Business Reports")
    st.success("✔ Duplicate Detection")
    
elif menu == "Upload Documents":

    st.header("Upload Documents")

    uploaded = st.file_uploader(
        "Upload PDF, DOCX or TXT",
        type=["pdf", "docx", "txt"]
    )

    if uploaded:

        os.makedirs("uploads", exist_ok=True)

        path = os.path.join(
            "uploads",
            uploaded.name
        )

        with open(path, "wb") as f:

            f.write(uploaded.getbuffer())

        st.success("Document Uploaded Successfully")

        text = DocumentExtractor.extract(path)

        st.subheader("Extracted Text")

        st.text_area(
            "",
            text,
            height=300
        )

        logger.log(
            "Upload",
            uploaded.name,
            "Uploaded Successfully"
        )
elif menu == "AI Summarizer":

    st.header("AI Document Summarizer")

    files = os.listdir("datasets/documents")

    selected = st.selectbox(
        "Select Document",
        files
    )

    if st.button("Generate Summary"):

        path = os.path.join(
            "datasets/documents",
            selected
        )

        text = DocumentExtractor.extract(path)

        summarizer = DocumentSummarizer()

        with st.spinner("Generating Summary..."):

            summary = summarizer.summarize(text)

        st.subheader("Summary")

        st.success(summary)

        logger.log(
            "Summarizer",
            selected,
            summary
        )
elif menu == "Semantic Search":

    st.header("Semantic Search")

    query = st.text_input(
        "Enter Search Query"
    )

    if st.button("Search"):

        search = SemanticSearch()

        results = search.search(query)

        logger.log(
            "Semantic Search",
            query,
            "Completed"
        )

        for i, doc in enumerate(results):

            st.subheader(f"Result {i+1}")

            if hasattr(doc, "metadata"):
                st.write("Source:", doc.metadata.get("source", "Unknown"))

            if hasattr(doc, "page_content"):
                st.write(doc.page_content)
            else:
                st.write(doc)
elif menu == "Question Answering":

    st.header("Ask Questions")

    question = st.text_input(
        "Enter your question"
    )

    if st.button("Get Answer"):

        qa = DocumentQA()

        with st.spinner("Thinking..."):

            answer = qa.ask(question)

        st.success(answer)

        logger.log(
            "Question Answering",
            question,
            answer
        )
elif menu == "Resume Screening":

    st.header("Resume Screening")

    resumes = os.listdir("datasets/resumes")

    resume = st.selectbox(
        "Select Resume",
        resumes
    )

    jobs = os.listdir("datasets/job_descriptions")

    job = st.selectbox(
        "Select Job Description",
        jobs
    )

    if st.button("Screen Resume"):

        resume_text = DocumentExtractor.extract(
            os.path.join(
                "datasets/resumes",
                resume
            )
        )

        with open(
            os.path.join(
                "datasets/job_descriptions",
                job
            ),
            "r",
            encoding="utf-8"
        ) as f:

            jd = f.read()

        matcher = ResumeMatcher()

        result = matcher.calculate_score(
            resume_text,
            jd
        )

        st.metric(
            "Matching Score",
            f"{result['Score']}%"
        )

        st.subheader("Matched Skills")

        st.success(result["Matched Skills"])

        st.subheader("Missing Skills")

        st.error(result["Missing Skills"])

        logger.log(
            "Resume Screening",
            resume,
            result["Score"]
        )
elif menu == "Candidate Ranking":

    st.header("Candidate Ranking")

    jobs = os.listdir("datasets/job_descriptions")

    job = st.selectbox(
        "Job Description",
        jobs
    )

    if st.button("Rank Candidates"):

        with open(
            os.path.join(
                "datasets/job_descriptions",
                job
            ),
            "r",
            encoding="utf-8"
        ) as f:

            jd = f.read()

        ranking = CandidateRanking()

        results = ranking.rank_candidates(
            "datasets/resumes",
            jd
        )

        st.dataframe(
            pd.DataFrame(results)
        )

        logger.log(
            "Candidate Ranking",
            job,
            "Completed"
        )
elif menu == "Interview Questions":

    st.header("Interview Question Generator")

    resumes = os.listdir("datasets/resumes")

    resume = st.selectbox(
        "Select Resume",
        resumes
    )

    if st.button("Generate Questions"):

        text = DocumentExtractor.extract(
            os.path.join(
                "datasets/resumes",
                resume
            )
        )

        generator = InterviewQuestionGenerator()

        questions = generator.generate_questions(text)

        for i, q in enumerate(questions, 1):

            st.write(f"{i}. {q}")

        logger.log(
            "Interview Questions",
            resume,
            len(questions)
        )
elif menu == "HR Chatbot":

    st.header("🤖 Enterprise HR Chatbot")

    question = st.text_input(
        "Ask an HR Question"
    )

    if st.button("Ask HR"):

        bot = HRChatbot()

        with st.spinner("Thinking..."):

            answer = bot.chat(question)

        st.success(answer)

        logger.log(
            "HR Chatbot",
            question,
            answer
        )
elif menu == "Business Reports":

    st.header("📊 AI Business Report Generator")

    documents = os.listdir(
        "datasets/documents"
    )

    selected = st.selectbox(
        "Select Document",
        documents
    )

    if st.button("Generate Business Report"):

        path = os.path.join(
            "datasets/documents",
            selected
        )

        text = DocumentExtractor.extract(path)

        summary = DocumentSummarizer().summarize(text)

        report = ReportGenerator()

        file = report.generate_report(
            title=selected,
            summary=summary
        )

        st.success("Report Generated Successfully!")

        with open(file, "rb") as f:

            st.download_button(
                "📄 Download Report",
                f,
                file_name=os.path.basename(file),
                mime="application/pdf"
            )

        logger.log(
            "Business Report",
            selected,
            file
        )
elif menu == "Document Classification":

    st.header("📂 Document Classification")

    classifier = DocumentClassifier()

    if st.button("Classify Documents"):

        results = classifier.classify_folder(
            "datasets/documents"
        )

        df = pd.DataFrame(
            list(results.items()),
            columns=[
                "Document",
                "Category"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        logger.log(
            "Document Classification",
            "All Documents",
            "Completed"
        )
elif menu == "Duplicate Documents":

    st.header("📑 Duplicate Document Detection")

    if st.button("Find Duplicate Documents"):

        detector = DuplicateDetector()

        duplicates = detector.detect_duplicates(
            "datasets/documents"
        )

        if len(duplicates) == 0:

            st.success("No Duplicate Documents Found")

        else:

            df = pd.DataFrame(duplicates)

            st.dataframe(
                df,
                use_container_width=True
            )

        logger.log(
            "Duplicate Detection",
            "All Documents",
            "Completed"
        )
elif menu == "AI Logs":

    st.header("📜 AI Interaction Logs")

    try:

        logs = pd.read_csv(
            "logs/ai_logs.csv"
        )

        st.dataframe(
            logs,
            use_container_width=True
        )

        csv = logs.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇ Download Logs",
            csv,
            file_name="ai_logs.csv",
            mime="text/csv"
        )

    except:

        st.warning("No Logs Available")
if menu == "Dashboard":

    st.title("Enterprise AI Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Documents",
        len(os.listdir("datasets/documents"))
    )

    c2.metric(
        "Resumes",
        len(os.listdir("datasets/resumes"))
    )

    c3.metric(
        "Job Descriptions",
        len(os.listdir("datasets/job_descriptions"))
    )

    try:

        logs = pd.read_csv(
            "logs/ai_logs.csv"
        )

        c4.metric(
            "AI Interactions",
            len(logs)
        )

    except:

        c4.metric(
            "AI Interactions",
            0
        )

    st.markdown("---")

    st.subheader("Project Status")

    data = pd.DataFrame({

        "Requirement":[
            "AI Processing",
            "Summarization",
            "Semantic Search",
            "Question Answering",
            "Resume Screening",
            "Candidate Ranking",
            "HR Chatbot",
            "Business Reports",
            "Classification",
            "Duplicate Detection"
        ],

        "Completed":[
            100,
            100,
            100,
            100,
            100,
            100,
            100,
            100,
            100,
            100
        ]
    })

    st.bar_chart(
        data.set_index("Requirement")
    )

    st.success("✅ All Project Requirements Implemented")
