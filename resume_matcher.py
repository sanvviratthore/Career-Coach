import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Your existing imports and code ...

# Azure Document Intelligence config
AZURE_FORM_RECOGNIZER_ENDPOINT = "https://careercoach-formrecognizer.cognitiveservices.azure.com/"
AZURE_FORM_RECOGNIZER_KEY = "ElgiMCrTNyuLEyrikbAIjuQHUD9lzVrLT242zHAxdD4iTQewXj7aJQQJ99BFACYeBjFXJ3w3AAALACOGtUSC"

client = DocumentAnalysisClient(
    endpoint=AZURE_FORM_RECOGNIZER_ENDPOINT,
    credential=AzureKeyCredential(AZURE_FORM_RECOGNIZER_KEY)
)

def analyze_resume_with_azure(pdf_bytes):
    poller = client.begin_analyze_document(
        "prebuilt-document",
        document=pdf_bytes
    )
    result = poller.result()

    full_text = ""
    for page in result.pages:
        # page.lines is a list of line objects; extract their content strings
        page_text = " ".join([line.content for line in page.lines])
        full_text += page_text + " "

    # Convert entire text to lowercase once all pages are processed
    return full_text.lower()


def run():
    st.title("📄 Resume Skill Matcher")

    @st.cache_data
    def load_data():
        return pd.read_csv('job_skills.csv')

    # Existing job title extraction and UI code ...
    df_jobs = load_data()
    df_jobs['job_title'] = df_jobs['job_link'].apply(
        lambda url: re.sub(r'-\d+.*$', '', url.split('/view/')[1]).replace('-', ' ').title() if '/view/' in url else "Unknown Job"
    )

    job_titles = df_jobs['job_title'].unique()[:100]
    selected_job_title = st.selectbox("Select a job:", job_titles)

    selected_job_row = df_jobs[df_jobs['job_title'] == selected_job_title].iloc[0]
    skills_list = [skill.strip().lower() for skill in selected_job_row['job_skills'].split(',') if skill.strip()]

    st.markdown(f"### Skills required for **{selected_job_title}**")
    st.write(", ".join(skills_list))

    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

    if uploaded_file:
        try:
            pdf_bytes = uploaded_file.read()
            resume_text = analyze_resume_with_azure(pdf_bytes)

            with st.expander("Preview extracted resume text (first 3000 chars)"):
                st.text(resume_text[:3000] + ("..." if len(resume_text) > 3000 else ""))

            matched = [skill for skill in skills_list if skill in resume_text]
            missing = [skill for skill in skills_list if skill not in resume_text]

            st.markdown(f"**Matched Skills ({len(matched)}):** {', '.join(matched) if matched else 'None'}")
            st.markdown(f"**Skills to Improve ({len(missing)}):** {', '.join(missing) if missing else 'None'}")

            def show_skill_gap_chart(matched, missing):
                labels = ['Matched Skills', 'Missing Skills']
                sizes = [len(matched), len(missing)]
                colors = ['#4CAF50', '#FF5722']

                fig, ax = plt.subplots()
                wedges, texts, autotexts = ax.pie(
                    sizes,
                    labels=labels,
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=colors,
                    textprops={'color':"w"}
                )
                ax.axis('equal')
                plt.setp(autotexts, size=14, weight="bold")
                st.pyplot(fig)

            show_skill_gap_chart(matched, missing)

        except Exception as e:
            st.error(f"Failed to analyze resume. Error: {e}")


