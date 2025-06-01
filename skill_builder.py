import streamlit as st

def run():
    st.title("🧠 Skill Builder")
    st.markdown("Find skill-building resources tailored to your interests or resume gaps.")

    skills_resources = {
        "Python": [
            ("Beginner Course on Coursera", "https://www.coursera.org/specializations/python"),
            ("Intermediate Practice on HackerRank", "https://www.hackerrank.com/domains/tutorials/10-days-of-python"),
            ("Build 2 Projects using this skill", None),
            ("Add to Resume and LinkedIn", None),
        ],
        "Communication": [
            ("Effective Communication Course on Coursera", "https://www.coursera.org/learn/effective-communication"),
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
        "DSA": [
            ("Data Structures and Algorithms Specialization on Coursera", "https://www.coursera.org/specializations/data-structures-algorithms"),
            ("Solve problems on HackerRank", "https://www.hackerrank.com/domains/tutorials/10-days-of-javascript"),
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

    selected_skill = st.selectbox("Choose a skill to improve:", list(skills_resources.keys()))

    if selected_skill:
        st.subheader(f"📘 Learning Path for {selected_skill}")
        for item in skills_resources[selected_skill]:
            if item[1]:
                st.markdown(f"- [{item[0]}]({item[1]})")
            else:
                st.markdown(f"- {item[0]}")
