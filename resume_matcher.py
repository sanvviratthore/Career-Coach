import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt
import fitz  # PyMuPDF for PDF reading

def run():
    st.title("📄 Resume Skill Matcher")

    @st.cache_data
    def load_data():
        df = pd.read_csv('job_skills.csv')
        return df

    def extract_job_title(url):
        parts = url.split('/view/')
        if len(parts) > 1:
            title_part = parts[1]
            title_part = re.sub(r'-\d+.*$', '', title_part)
            title = title_part.replace('-', ' ').title()
            return title
        return "Unknown Job"

    df_jobs = load_data()
    df_jobs['job_title'] = df_jobs['job_link'].apply(extract_job_title)
    job_titles = df_jobs['job_title'].unique()[:100]

    selected_job_title = st.selectbox("Select a job:", job_titles)
    selected_job_link = df_jobs[df_jobs['job_title'] == selected_job_title]['job_link'].values[0]

    skills_str = df_jobs[df_jobs['job_link'] == selected_job_link]['job_skills'].values[0]
    skills_list = [skill.strip().lower() for skill in skills_str.split(',')]

    st.write(f"### Skills required for this job:")
    st.write(", ".join(skills_list))

    uploaded_file = st.file_uploader("Upload your resume (.pdf)", type=["pdf"])

    if uploaded_file is not None:
        # Read PDF content from uploaded file
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        resume_text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            resume_text += page.get_text()

        resume_text = resume_text.lower()
        st.write("### Text Extracted from Resume:")
        st.write(resume_text)

        matched = [skill for skill in skills_list if skill in resume_text]
        missing = [skill for skill in skills_list if skill not in resume_text]

        st.write(f"**Matched Skills ({len(matched)}):** {', '.join(matched) if matched else 'None'}")
        st.write(f"**Skills to Improve ({len(missing)}):** {', '.join(missing) if missing else 'None'}")

        def show_skill_gap_chart(matched, missing):
            labels = ['Matched Skills', 'Missing Skills']
            sizes = [len(matched), len(missing)]
            colors = ['#4CAF50', '#FF5722']

            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
            ax.axis('equal')
            st.pyplot(fig)

        show_skill_gap_chart(matched, missing)

