import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt
import fitz  # PyMuPDF for PDF reading

def run():
    st.title("📄 Resume Skill Matcher")

    @st.cache_data
    def load_data():
        return pd.read_csv('job_skills.csv')

    def extract_job_title(url):
        # Extract readable job title from URL
        parts = url.split('/view/')
        if len(parts) > 1:
            title_part = parts[1]
            title_part = re.sub(r'-\d+.*$', '', title_part)  # Remove trailing numbers and chars
            title = title_part.replace('-', ' ').title()
            return title
        return "Unknown Job"

    df_jobs = load_data()
    df_jobs['job_title'] = df_jobs['job_link'].apply(extract_job_title)

    # Limit to top 100 unique job titles for performance & UX
    job_titles = df_jobs['job_title'].unique()[:100]

    selected_job_title = st.selectbox("Select a job:", job_titles)

    # Get job link and skills for selected job
    selected_job_row = df_jobs[df_jobs['job_title'] == selected_job_title].iloc[0]
    selected_job_link = selected_job_row['job_link']
    skills_str = selected_job_row['job_skills']
    skills_list = [skill.strip().lower() for skill in skills_str.split(',') if skill.strip()]

    st.markdown(f"### Skills required for **{selected_job_title}**")
    st.write(", ".join(skills_list))

    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

    if uploaded_file:
        try:
            # Read PDF content from uploaded file
            pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            resume_text = ""
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                resume_text += page.get_text()

            resume_text = resume_text.lower()

            with st.expander("Preview extracted resume text"):
                st.text(resume_text[:3000] + ("..." if len(resume_text) > 3000 else ""))  # Limit preview to 3k chars

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
            st.error(f"Failed to read PDF file. Please upload a valid PDF. Error: {e}")

