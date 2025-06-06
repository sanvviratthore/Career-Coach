import streamlit as st
import os
from openai import AzureOpenAI

# Azure OpenAI settings
endpoint = "https://sanvi-mbf58gtv-eastus2.cognitiveservices.azure.com/"
deployment = "gpt-4.1"  # Deployed model name in Azure OpenAI Studio
api_version = "2024-12-01-preview"
subscription_key = "F8cvPQQ5iKHG8NUJY0GbhH4Zxhll5BJQUMOapCLVoDQ6xX9V70tYJQQJ99BFACHYHv6XJ3w3AAAAACOGaJVI"  # Replace with your actual key

# Initialize AzureOpenAI client
client = AzureOpenAI(
    api_key=subscription_key,
    api_version=api_version,
    azure_endpoint=endpoint
)

def run():
    st.title("🎯 Course Recommendations")

    topics = st.text_input(
        "Enter one or more topics (comma separated, e.g. Flutter, Data Engineering):", 
        placeholder="e.g. Python, Cloud Computing"
    )

    if st.button("Get Recommendations") and topics.strip() != "":
        with st.spinner("Fetching course recommendations..."):
            prompt = f"""
            Suggest top 10 high-quality online courses for the following topics: {topics}.
            For each course, include:
            - Platform name (Coursera, Udemy, edX, etc.)
            - Course title as clickable Markdown link (format: [Course Title](url))
            - A brief reason why the course is recommended.
            Provide the list as bullet points in Markdown format.
            """

            try:
                response = client.chat.completions.create(
                    model=deployment,
                    messages=[
                        {"role": "system", "content": "You are a helpful course recommendation assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=800,
                    temperature=1.0,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )

                recommendations = response.choices[0].message.content
                st.markdown("### 📚 Recommended Courses")
                st.markdown(recommendations)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
