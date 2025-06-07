import streamlit as st
from openai import AzureOpenAI
import datetime, re, json
from streamlit_lottie import st_lottie

client = AzureOpenAI(
    api_key=st.secrets["azure_openai_api_key"],
    azure_endpoint=st.secrets["azure_openai_endpoint"],
    api_version=st.secrets["azure_openai_api_version"],
)

DEPLOYMENT = st.secrets["azure_openai_deployment"]

def generate_questions(interview_type: str) -> list[str]:
    prompt = f"""You are an HR professional. Generate **exactly ten** {interview_type.lower()} interview questions suitable for a pre-final and
final-year computer-science/IT engineering student. Return them as a plain numbered list.
Also make sure you try to give different questions every time they ask for generating questions.
Also make sure to give 0/10 if the user doesn't input anything and just submits their answer."""
    resp = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[
            {"role": "system", "content": "You are a professional interviewer."},
            {"role": "user", "content": prompt}],
        max_tokens=300, temperature=0.8)
    q_text = resp.choices[0].message.content.strip()
    return [re.sub(r"^\d+\.\s*", "", ln).strip()
            for ln in q_text.splitlines() if ln.strip()]

def get_feedback(questions, answers) -> str:
    qa = "\n\n".join(f"Q{i+1}: {q}\nA{i+1}: {a}"
                     for i, (q, a) in enumerate(zip(questions, answers)))
    prompt = f"""You are an expert technical interviewer. Review the Q&A and give strengths, areas to improve,
and a rating out of 10 for each answer.

{qa}

Return exactly:
Question 1 Feedback (rating x/10): ...
Question 2 Feedback (rating x/10): ...
"""
    resp = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[
            {"role": "system", "content": "You are a seasoned interviewer providing actionable feedback."},
            {"role": "user", "content": prompt}],
        max_tokens=800, temperature=0.7)
    return resp.choices[0].message.content.strip()

def load_lottie(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

lottie_json = load_lottie("animations/Animation - 1749286005992.json")      

def run():
    st.title("🎤 Mock Interview Prep")
    st.markdown(
        "Practice common interview questions, type your answers, and receive AI-powered feedback."
    )

    st.markdown("""
    <style>
    .container {display:flex;align-items:center;justify-content:center;gap:2rem;flex-wrap:wrap;margin-bottom:1.5rem;}
    .input-box {max-width:380px;flex:1 1 380px;}
    .lottie-box{max-width:260px;flex:1 1 260px;}
    .stButton>button{width:100%}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="container">', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="input-box">', unsafe_allow_html=True)
        interview_type = st.radio("Choose interview focus:", ["Technical", "Behavioral"], horizontal=True)
        if st.button("Generate Questions", type="primary"):
            st.session_state.questions = generate_questions(interview_type)
            st.session_state.start_time = datetime.datetime.now()
            st.session_state.feedback = None
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="lottie-box">', unsafe_allow_html=True)
    st_lottie(lottie_json, height=220, key="interview_lottie")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) 

    if "questions" in st.session_state:
        st.subheader("📋 Your Questions")
        answers = []
        for i, q in enumerate(st.session_state.questions, 1):
            st.write(f"**{i}. {q}**")
            answers.append(st.text_area("Your answer:", key=f"ans_{i}", height=120))

        colA, colB = st.columns([1, 3])
        with colA:
            if st.button("Submit Answers & Get Feedback"):
                st.session_state.feedback = get_feedback(st.session_state.questions, answers)
        with colB:
            if "start_time" in st.session_state:
                elapsed = datetime.datetime.now() - st.session_state.start_time
                st.info(f"⏱️ Time since questions generated: {elapsed.seconds//60} min {elapsed.seconds%60} s")

        if st.session_state.get("feedback"):
            st.markdown("### 📝 Feedback")
            st.write(st.session_state.feedback)

if __name__ == "__main__":
    run()
