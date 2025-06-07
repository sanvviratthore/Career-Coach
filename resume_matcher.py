import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import json
from streamlit_lottie import st_lottie

AZURE_FORM_RECOGNIZER_ENDPOINT = "https://careercoach-formrecognizer.cognitiveservices.azure.com/"
AZURE_FORM_RECOGNIZER_KEY = "ElgiMCrTNyuLEyrikbAIjuQHUD9lzVrLT242zHAxdD4iTQewXj7aJQQJ99BFACYeBjFXJ3w3AAALACOGtUSC"

client = DocumentAnalysisClient(
    endpoint=AZURE_FORM_RECOGNIZER_ENDPOINT,
    credential=AzureKeyCredential(AZURE_FORM_RECOGNIZER_KEY)
)

def load_lottiefile(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

lottie_resume = load_lottiefile("animations/Animation - 1749283614215.json")  

@st.cache_data
def load_data():
    return pd.read_csv('job_skills.csv')

def analyze_resume_with_azure(pdf_bytes):
    poller = client.begin_analyze_document("prebuilt-document", document=pdf_bytes)
    result = poller.result()
    full_text = ""
    for page in result.pages:
        page_text = " ".join([line.content for line in page.lines])
        full_text += page_text + " "
    return full_text.lower()

def run():
    st.title("📄 Resume Skill Matcher")
    st.subheader("For students and working professionals")
    st.markdown("Upload your resume and see how well it aligns with the skills required for your desired job roles.")

    col1, col2 = st.columns([3, 2])
    with col2:
        st_lottie(lottie_resume, height=250, key="resume")

    with col1:
        df_jobs = load_data()

        df_jobs['job_title'] = df_jobs['job_link'].apply(
            lambda url: re.sub(r'-\d+.*$', '', url.split('/view/')[1]).replace('-', ' ').title()
            if '/view/' in url else "Unknown Job"
        )

        tech_keywords = ['engineer', 'developer', 'analyst', 'scientist', 'architect']
        job_filter = st.radio("🎯 Filter Jobs:", ["All Jobs", "Tech Only"])
        filtered_jobs = df_jobs[df_jobs['job_title'].str.lower().str.contains('|'.join(tech_keywords))] \
                        if job_filter == "Tech Only" else df_jobs

        job_titles = filtered_jobs['job_title'].unique()[:100]
        selected_job_title = st.selectbox("💼 Select a Job Title:", job_titles)

        selected_row = filtered_jobs[filtered_jobs['job_title'] == selected_job_title].iloc[0]
        skills_list = [skill.strip().lower() for skill in selected_row['job_skills'].split(',') if skill.strip()]

        st.markdown(f"### ✅ Skills Required for **{selected_job_title}**")
        st.write(", ".join(skills_list))

        uploaded_file = st.file_uploader("📎 Upload your Resume (PDF only)", type=["pdf"])

        if uploaded_file:
            try:
                pdf_bytes = uploaded_file.read()
                resume_text = analyze_resume_with_azure(pdf_bytes)

                with st.expander("🔍 Preview Extracted Resume Text (First 3000 characters)"):
                    st.text(resume_text[:3000] + ("..." if len(resume_text) > 3000 else ""))

                matched = [skill for skill in skills_list if skill in resume_text]
                missing = [skill for skill in skills_list if skill not in resume_text]

                st.success(f"✅ Matched Skills ({len(matched)}):")
                st.markdown(", ".join(matched) if matched else "None")

                st.error(f"📌 Skills to Improve ({len(missing)}):")
                st.markdown(", ".join(missing) if missing else "None")

                def show_skill_gap_chart(matched, missing):
                    labels = ['Matched Skills', 'Missing Skills']
                    sizes = [len(matched), len(missing)]
                    colors = ['#4CAF50', '#FF5722']

                    fig, ax = plt.subplots()
                    wedges, _, autotexts = ax.pie(
                        sizes,
                        labels=labels,
                        autopct='%1.1f%%',
                        startangle=90,
                        colors=colors,
                        textprops={'color': "w"}
                    )
                    ax.axis('equal')
                    plt.setp(autotexts, size=14, weight="bold")
                    st.pyplot(fig)

                show_skill_gap_chart(matched, missing)

            except Exception as e:
                st.error(f"❌ Failed to analyze resume. Error: {e}")
