import streamlit as st
from openai import AzureOpenAI
import datetime
import re

# ====== Azure OpenAI credentials ======
openai_key      = "F8cvPQQ5iKHG8NUJY0GbhH4Zxhll5BJQUMOapCLVoDQ6xX9V70tYJQQJ99BFACHYHv6XJ3w3AAAAACOGaJVI"
openai_endpoint = "https://sanvi-mbf58gtv-eastus2.cognitiveservices.azure.com/"
deployment      = "gpt-4.1"                       # your deployed model name
api_version     = "2024-12-01-preview"

client = AzureOpenAI(
    api_key=openai_key,
    azure_endpoint=openai_endpoint,
    api_version=api_version,
)

# ---------- GPT wrappers ----------
def generate_questions(interview_type: str) -> list[str]:
    """Ask GPT for five interview questions of the selected type."""
    prompt = f"""
You are an HR professional. Generate **exactly five** {interview_type.lower()} interview questions suitable for a final-year engineering student.
Return them as a plain numbered list.

Examples:
1. ...
2. ...
"""
    resp = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a professional interviewer."},
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=300,
        temperature=0.8,
    )
    q_text = resp.choices[0].message.content.strip()

    # extract numbered lines (1., 2., …)
    return [re.sub(r"^\d+\.\s*", "", line).strip()
            for line in q_text.splitlines()
            if line.strip()]

def get_feedback(questions: list[str], answers: list[str]) -> str:
    """Send Q&A pairs to GPT and receive constructive feedback."""
    qa_blocks = "\n\n".join(
        f"Q{idx+1}: {q}\nA{idx+1}: {a}" for idx, (q, a) in enumerate(zip(questions, answers))
    )
    prompt = f"""
You are an expert technical interviewer. Review the following question-answer pairs and give **constructive, specific feedback** for each answer (strengths, areas to improve, and a brief rating out of 10).

{qa_blocks}

Return feedback in this exact format:

Question 1 Feedback (rating x/10): …
Question 2 Feedback (rating x/10): …
...
"""
    resp = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a seasoned interviewer providing actionable feedback."},
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=800,
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()

# ---------- Streamlit page ----------
def run():
    st.title("🎤 Mock Interview Prep")
    st.markdown(
        "Practice common interview questions, type your answers, and receive AI-powered feedback."
    )

    # Select interview type
    interview_type = st.radio("Choose interview focus:",
                              ["Technical", "Behavioral"], horizontal=True)

    # Generate questions button
    if st.button("Generate Questions", type="primary"):
        st.session_state.questions  = generate_questions(interview_type)
        st.session_state.start_time = datetime.datetime.now()
        st.session_state.feedback   = None

    # If questions already generated, show them with answer inputs
    if "questions" in st.session_state:
        st.subheader("📋 Your Questions")
        answers = []
        for i, q in enumerate(st.session_state.questions, start=1):
            st.write(f"**{i}. {q}**")
            answer = st.text_area("Your answer:", key=f"ans_{i}", height=120)
            answers.append(answer)

        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Submit Answers & Get Feedback"):
                st.session_state.feedback = get_feedback(
                    st.session_state.questions, answers
                )
        with col2:
            if "start_time" in st.session_state:
                elapsed = datetime.datetime.now() - st.session_state.start_time
                st.info(f"⏱️ Time since questions generated: {elapsed.seconds//60} min {elapsed.seconds%60} s")

        # Show feedback once available
        if st.session_state.get("feedback"):
            st.markdown("### 📝 Feedback")
            st.write(st.session_state.feedback)

