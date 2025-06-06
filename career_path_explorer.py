import streamlit as st
from openai import AzureOpenAI
import requests

client = AzureOpenAI(
    api_key="F8cvPQQ5iKHG8NUJY0GbhH4Zxhll5BJQUMOapCLVoDQ6xX9V70tYJQQJ99BFACHYHv6XJ3w3AAAAACOGaJVI",
    azure_endpoint="https://sanvi-mbf58gtv-eastus2.cognitiveservices.azure.com/",
    api_version="2024-12-01-preview",
)
DEPLOYMENT = "gpt-4.1"

def get_career_paths_and_companies(domain):
    prompt = (
        f"You are a career counselor. For the industry/domain '{domain}', please provide:\n"
        f"1. Five career paths with relevant skills for each.\n"
        f"2. A list of top companies globally that hire for roles in this domain.\n"
        f"3. Add a line at the end that region-specific companies or information on startups and emerging organizations in that field, explore the Industry Trends feature of this app.\n"
        f"Format your answer clearly with headings."
    )
    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[
            {"role": "system", "content": "You are a helpful career counselor."},
            {"role": "user", "content": prompt},
        ],
        max_completion_tokens=700,
        temperature=0.7,
    )
    return response.choices[0].message.content

def run():
    st.title("🚀 Career Path Explorer")

    domain = st.text_input(
        "Enter an Industry/Domain (e.g., AI, Cloud, Cybersecurity):",
        key="domain_input"
    )

    if domain.strip():
        with st.spinner("Fetching career paths and top companies..."):
            try:
                career_info = get_career_paths_and_companies(domain.strip())
            except Exception as e:
                st.error(f"Error fetching career info: {e}")
                career_info = None

        if career_info:
            st.markdown("### Career Paths and Hiring Companies")
            st.write(career_info)

if __name__ == "__main__":
    run()