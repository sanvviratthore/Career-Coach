import streamlit as st
from datetime import date, timedelta

def run():
    st.title("📚 Course Recommendations")

    st.markdown("### Build your personalized study plan")

    skill_input = st.text_input(
        "Enter skills you want to learn or improve (comma separated):",
        placeholder="e.g., Python, Data Analysis, Machine Learning"
    )

    skills = []
    if skill_input:
        skills = [s.strip() for s in skill_input.split(",") if s.strip()]
        if skills:
            st.write(f"Planning study schedule for: **{', '.join(skills)}**")

            start_date = st.date_input("Select Start Date", value=date.today())

            plan_length = st.slider(
                "Select the number of weeks for your study plan:",
                min_value=1,
                max_value=12,
                value=min(len(skills), 4),
                help="Adjust duration based on your availability"
            )

            if st.button("Generate Study Plan"):
                st.markdown("### Your Study Plan:")
                for i in range(plan_length):
                    week_start = start_date + timedelta(weeks=i)
                    # Cycle through skills if plan_length > number of skills
                    skill = skills[i % len(skills)]
                    st.write(f"**Week {i + 1} ({week_start.strftime('%b %d, %Y')}):** Focus on learning **{skill}**")
        else:
            st.warning("Please enter at least one skill to create a study plan.")
        st.markdown("---")

    st.subheader("🎯 Recommended Courses for You")

    sample_courses = {
        "Python": ["Python for Everybody - Coursera", "Automate the Boring Stuff with Python"],
        "Data Analysis": ["Data Analysis with Pandas - DataCamp", "Excel to MySQL: Analytic Techniques - Coursera"],
        "Machine Learning": ["Machine Learning by Andrew Ng - Coursera", "Intro to Machine Learning - Udacity"],
    }

    if skills:
        for skill in skills:
            courses = sample_courses.get(skill, ["No course data yet"])
            st.markdown(f"**{skill}:**")
            for c in courses:
                st.write(f"- {c}")
    else:
        st.info("Start by typing the skills you'd like to learn or improve.")

