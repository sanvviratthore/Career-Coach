import streamlit as st
from azure_openai_api import ask_azure_openai

def run():
    st.title("🧪 Mock Interview Prep")
    st.markdown("Practice typical interview questions to boost your confidence.")

    question_type = st.radio("Select question type:", ["Behavioral", "Technical"])

    if question_type == "Behavioral":
        prompt = "Give me a behavioral interview question and tips for answering it."
    else:
        prompt = "Give me a technical interview question and tips for answering it."

    if st.button("Get Question"):
        with st.spinner("Fetching question from Azure OpenAI..."):
            # Prepare the messages list
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
            answer = ask_azure_openai(messages)
            st.markdown(f"**AI Generated Question & Tips:**\n\n{answer}")

if __name__ == "__main__":
    run()
