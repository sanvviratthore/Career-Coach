import streamlit as st
from azure_openai_api import ask_azure_openai

API_KEY = "2MTbbBLRpmpNv7sP6UJYF3kM3CuUhbVUL1Dad0mYzUoeVPuBvL8GJQQJ99BFAC77bzfXJ3w3AAABACOGUO8O"
ENDPOINT = "https://careercoach-openai.openai.azure.com"
DEPLOYMENT_NAME = "gpt-35-turbo"  # your deployment/model name

def run():
    st.title("🧪 Mock Interview Prep")
    st.markdown("Practice typical interview questions to boost your confidence.")

    question_type = st.radio("Select question type:", ["Behavioral", "Technical"])

    if question_type == "Behavioral":
        prompt = "Give me a behavioral interview question and tips for answering it."
    else:
        prompt = "Give me a technical interview question and tips for answering it."

    if st.button("Get Question"):
        answer = ask_azure_openai(prompt, DEPLOYMENT_NAME, API_KEY, ENDPOINT)
        st.markdown(f"**AI Generated Question & Tips:**\n\n{answer}")


