import streamlit as st

def run():
    st.title("📊 Career Path Explorer")
    st.markdown("Explore career paths, salary trends, essential skills, and growth opportunities.")

    careers = {
        "Data Scientist": {
            "salary": "₹12–30 LPA",
            "skills": ["Python", "Statistics", "Machine Learning", "SQL", "Data Visualization"],
            "growth": "🚀 High demand across industries",
            "courses": {
                "Coursera": "https://www.coursera.org/specializations/data-science-python",
                "LinkedIn Learning": "https://www.linkedin.com/learning/topics/data-science",
                "Udemy": "https://www.udemy.com/topic/data-science/"
            }
        },
        "Software Engineer": {
            "salary": "₹8–25 LPA",
            "skills": ["Programming (Java, Python)", "Data Structures", "Algorithms", "System Design"],
            "growth": "📈 Steady growth with tech evolution",
            "courses": {
                "Coursera": "https://www.coursera.org/specializations/java-programming",
                "LinkedIn Learning": "https://www.linkedin.com/learning/software-development",
                "Udemy": "https://www.udemy.com/topic/software-engineering/"
            }
        },
        "Cybersecurity Analyst": {
            "salary": "₹7–20 LPA",
            "skills": ["Network Security", "Ethical Hacking", "Risk Management", "Compliance"],
            "growth": "🚀 Growing importance due to cyber threats",
            "courses": {
                "Coursera": "https://www.coursera.org/specializations/cyber-security",
                "LinkedIn Learning": "https://www.linkedin.com/learning/topics/cybersecurity",
                "Udemy": "https://www.udemy.com/topic/cyber-security/"
            }
        },
        "UX Designer": {
            "salary": "₹5–15 LPA",
            "skills": ["User Research", "Wireframing", "Prototyping", "Design Tools (Figma, Adobe XD)"],
            "growth": "📈 Increasing focus on user experience",
            "courses": {
                "Coursera": "https://www.coursera.org/specializations/ui-ux-design",
                "LinkedIn Learning": "https://www.linkedin.com/learning/ux-design",
                "Udemy": "https://www.udemy.com/topic/ux-design/"
            }
        },
        "Mechanical Engineer": {
            "salary": "₹4–12 LPA",
            "skills": ["CAD", "Thermodynamics", "Manufacturing Processes", "Material Science"],
            "growth": "📉 Moderate, varies by industry",
            "courses": {
                "Coursera": "https://www.coursera.org/courses?query=mechanical%20engineering",
                "LinkedIn Learning": "https://www.linkedin.com/learning/topics/mechanical-engineering",
                "Udemy": "https://www.udemy.com/topic/mechanical-engineering/"
            }
        }
    }

    choice = st.selectbox("Choose a career path to explore:", list(careers.keys()))

    if choice:
        career = careers[choice]
        st.subheader(f"🔍 Details for {choice}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Average Salary:** {career['salary']}")
            st.markdown("**Growth Outlook:**")
            st.markdown(f"> {career['growth']}")

        with col2:
            st.markdown("**Top Skills:**")
            for skill in career['skills']:
                st.markdown(f"- {skill}")

        st.markdown("**Suggested Courses:**")
        for platform, url in career['courses'].items():
            st.markdown(f"- [{platform}]({url})")

