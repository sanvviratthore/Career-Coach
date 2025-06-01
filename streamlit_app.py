import streamlit as st
from streamlit_lottie import st_lottie
import json
import career_path_explorer
import course_recommendations
import global_insights
import hackathons_internships
import industry_trends
import mock_interview
import resume_matcher
import skill_builder

# Load local lottie animation JSON
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Path to your local animation JSON
lottie_career = load_lottiefile("animations/Animation - 1748757720975.json")

# Set up Streamlit layout
st.set_page_config(page_title="Career Coach for Students", layout="wide")

# Sidebar navigation
PAGES = {
    "🏠 Home": None,
    "📄 Resume Matcher": resume_matcher,
    "🌍 Global Insights": global_insights,
    "📚 Course Recommendations": course_recommendations,
    "📊 Career Path Explorer": career_path_explorer,
    "🧠 Skill Builder": skill_builder,
    "🧪 Mock Interview Prep": mock_interview,
    "📅 Hackathons & Internships": hackathons_internships,
    "💡 Industry Trends": industry_trends,
}

st.sidebar.title("🎓 Career Coach Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# Main display logic
if selection == "🏠 Home":
    col1, col2 = st.columns(2)
    
    with col1:
        st.title("🎓 Career Coach for Students")
        st.markdown(
            """
            <div style='font-size:18px;'>
            Welcome! This AI-powered tool is designed to help students like you bridge the gap between university education and industry expectations.
            <br><br>
            🚀 Start your journey towards a successful career by exploring:
            <ul>
                <li>📄 Resume Matcher</li>
                <li>🌍 Global Insights</li>
                <li>📚 Course Recommendations</li>
                <li>📊 Career Path Explorer</li>
                <li>🧠 Skill Builder</li>
                <li>🧪 Mock Interview Prep</li>
                <li>📅 Hackathons & Internships</li>
                <li>💡 Industry Trends</li>
            </ul>
            </div>
            """, unsafe_allow_html=True
        )
    
    with col2:
        st_lottie(lottie_career, height=350, key="career")
else:
    page = PAGES[selection]
    if hasattr(page, "run") and callable(page.run):
        page.run()
    else:
        st.error(f"The page '{selection}' doesn't have a `run()` function.")


