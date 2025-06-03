import streamlit as st
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Azure Document Intelligence setup
AZURE_FORM_RECOGNIZER_ENDPOINT = "https://careercoach-formrecognizer.cognitiveservices.azure.com/"
AZURE_FORM_RECOGNIZER_KEY = "ElgiMCrTNyuLEyrikbAIjuQHUD9lzVrLT242zHAxdD4iTQewXj7aJQQJ99BFACYeBjFXJ3w3AAALACOGtUSC"  # Replace with your key

client = DocumentAnalysisClient(
    endpoint=AZURE_FORM_RECOGNIZER_ENDPOINT,
    credential=AzureKeyCredential(AZURE_FORM_RECOGNIZER_KEY)
)

def extract_text_from_doc(uploaded_file):
    try:
        poller = client.begin_analyze_document("prebuilt-document", document=uploaded_file)
        result = poller.result()
        full_text = ""
        for page in result.pages:
            for line in page.lines:
                full_text += line.content + " "
        return full_text.lower()
    except Exception as e:
        st.error(f"Failed to extract skills. Error: {e}")
        return ""

def run():
    st.title("🧠 Skill Builder")
    st.markdown("Find skill-building resources tailored to your interests or resume gaps.")

    # Upload document for skill detection
    uploaded_file = st.file_uploader("📄 Upload certificate, transcript or training doc (PDF)", type=["pdf"])
    
    extracted_skills = []
    if uploaded_file:
        with st.spinner("Analyzing document..."):
            text = extract_text_from_doc(uploaded_file)
            if text:
                skill_keywords = ["python", "sql", "communication", "data structures", "machine learning"]
                extracted_skills = [skill for skill in skill_keywords if skill in text]
                
                if extracted_skills:
                    st.success(f"Extracted Skills: {', '.join(extracted_skills)}")
                else:
                    st.warning("No known skills were extracted from this document.")

    skills_resources = {
        "Python": [
            ("Beginner Course on Coursera", "https://www.coursera.org/specializations/python"),
            ("Intermediate Practice on HackerRank", "https://www.hackerrank.com/domains/python"),
            ("Build 2 Projects using this skill", None),
            ("Add to Resume and LinkedIn", None),
        ],
        "Communication": [
            ("Effective Communication Course on Coursera", "https://www.coursera.org/learn/active-listening-enhancing-communication-skills"),
            ("Practice public speaking on Toastmasters", "https://www.toastmasters.org/find-a-club"),
            ("Record yourself and review", None),
            ("Add to Resume and LinkedIn", None),
        ],
        "SQL": [
            ("SQL for Data Science on Coursera", "https://www.coursera.org/learn/sql-for-data-science"),
            ("Practice SQL on LeetCode", "https://leetcode.com/problemset/database/"),
            ("Build a small database project", None),
            ("Add to Resume and LinkedIn", None),
        ],
        "Data Structures": [
            ("Data Structures and Algorithms Specialization on Coursera", "https://www.coursera.org/specializations/data-structures-algorithms"),
            ("Solve problems on GFG", "https://www.geeksforgeeks.org/explore?page=1&sprint=ca8ae412173dbd8346c26a0295d098fd&sortBy=submissions&sprint_name=Beginner%27s%20DSA%20Sheet&utm_source=geeksforgeeks&utm_medium=main_header&utm_campaign=practice_header"),
            ("Implement 2 algorithms in projects", None),
            ("Add to Resume and LinkedIn", None),
        ],
        "Machine Learning": [
            ("Machine Learning by Andrew Ng on Coursera", "https://www.coursera.org/learn/machine-learning"),
            ("Kaggle Competitions and Practice", "https://www.kaggle.com/competitions"),
            ("Build ML projects and portfolio", None),
            ("Add to Resume and LinkedIn", None),
        ],
    }

    # Let user choose skill or view suggestions
    st.divider()
    if extracted_skills:
     st.markdown("### 📌 Skill-building suggestions from your document:")

    for skill in extracted_skills:
        # Safely try to match skill regardless of case
        resource_key = next((k for k in skills_resources if k.lower() == skill.lower()), None)

        if not resource_key:
            st.warning(f"No learning path found for extracted skill: {skill}")
            continue

        st.subheader(f"📘 Learning Path for {resource_key}")
        for item in skills_resources[resource_key]:
            if item[1]:
                st.markdown(f"- [{item[0]}]({item[1]})")
            else:
                st.markdown(f"- {item[0]}")




    else:
        selected_skill = st.selectbox("Or choose a skill to improve:", list(skills_resources.keys()))
        if selected_skill:
            st.subheader(f"📘 Learning Path for {selected_skill}")
            for item in skills_resources[selected_skill]:
                if item[1]:
                    st.markdown(f"- [{item[0]}]({item[1]})")
                else:
                    st.markdown(f"- {item[0]}")

