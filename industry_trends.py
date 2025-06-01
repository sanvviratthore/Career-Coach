import streamlit as st

def run():
    st.title("💡 Industry Trends")
    st.markdown("Stay updated with the latest trends and insights across various tech domains.")

    selected_domain = st.selectbox(
        "Select a domain to explore trends:",
        ["AI", "Web Development", "Cybersecurity", "Data Analytics"]
    )

    if selected_domain:
        st.subheader(f"🔎 Latest Trends in {selected_domain}")
        
        trends = {
            "AI": [
                "Generative AI is reshaping content creation.",
                "AI-driven automation is increasing efficiency.",
                "Ethical AI and bias mitigation are gaining focus."
            ],
            "Web Development": [
                "Web3 and blockchain integrations are rising.",
                "Progressive Web Apps (PWAs) are becoming mainstream.",
                "Jamstack architecture improves performance and security."
            ],
            "Cybersecurity": [
                "Focus on zero-trust security models.",
                "Rise in AI-powered threat detection.",
                "Increased emphasis on privacy and data protection."
            ],
            "Data Analytics": [
                "Real-time dashboards and data visualization are in demand.",
                "Adoption of augmented analytics tools.",
                "Growing use of predictive analytics for business decisions."
            ]
        }

        for point in trends.get(selected_domain, []):
            st.markdown(f"- {point}")
