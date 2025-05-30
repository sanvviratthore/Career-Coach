import streamlit as st
from datetime import date, timedelta

def run():
    st.title("📚 Course Recommendations")

    st.markdown("### Build your personalized study plan")

    # Let user enter skills to improve separated by commas
    skill_input = st.text_input("Enter skills you want to learn or improve (comma separated):")

    if skill_input:
        skills = [s.strip() for s in skill_input.split(",") if s.strip()]
        st.write(f"Planning study schedule for: {', '.join(skills)}")

        start_date = st.date_input("Start Date", value=date.today())

        plan_length = st.slider("Number of weeks for the study plan:", 1, 12, 4)

        if st.button("Generate Study Plan"):
            st.markdown("### Your Study Plan:")
            for i, skill in enumerate(skills, 1):
                week = start_date + timedelta(weeks=i-1)
                st.write(f"**Week {i} ({week.strftime('%b %d, %Y')}):** Focus on learning **{skill}**")

