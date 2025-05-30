import streamlit as st
import resume_matcher
import global_insights
import course_recommendations

st.set_page_config(page_title="Career Coach for Students", layout="wide")

PAGES = {
    "🏠 Home": None,
    "📄 Resume Matcher": resume_matcher,
    "🌍 Global Insights": global_insights,
    "📚 Course Recommendations": course_recommendations,
}

st.sidebar.title("🎓 Career Coach Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

if selection == "🏠 Home":
    st.title("🎓 Career Coach for Students")
    st.markdown(
        """
        Welcome! This tool helps students bridge the gap between university education and industry needs.
        \nUse the sidebar to navigate to different tools like:
        - **Resume Matcher**
        - **Global Insights**
        - **Course Recommendations**
        """
    )
else:
    page = PAGES[selection]
    page.run()
