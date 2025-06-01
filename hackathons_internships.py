import streamlit as st

def run():
    st.title("📅 Hackathons & Internships")
    st.markdown("Discover upcoming tech events and internship opportunities to boost your experience.")

    st.markdown("### 🚀 Upcoming Hackathons")
    hackathons = [
        {"name": "Smart India Hackathon", "date": "July 2025"},
        {"name": "Hack the Mountains", "date": "August 2025"},
    ]
    for h in hackathons:
        st.markdown(f"- **{h['name']}** – {h['date']}")

    st.markdown("### 🧑‍💻 Internship Listings")
    internships = [
        {"role": "Intern at Microsoft", "deadline": "Apply by June 10"},
        {"role": "Research Intern at ISRO", "deadline": "Apply by June 15"},
    ]
    for i in internships:
        st.markdown(f"- **{i['role']}** – {i['deadline']}")
