import streamlit as st
from openai import AzureOpenAI
import json
from streamlit_lottie import st_lottie

client = AzureOpenAI(
    api_key=st.secrets["azure_openai_api_key"],
    azure_endpoint=st.secrets["azure_openai_endpoint"],
    api_version=st.secrets["azure_openai_api_version"]
)

DEPLOYMENT = st.secrets["azure_openai_deployment"]

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_career = load_lottiefile("animations/Animation - 1749285017326.json")

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

    st.markdown(
        """
        <style>
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 2rem;
            margin-top: 20px;
            margin-bottom: 40px;
            flex-wrap: wrap;
        }
        .input-area {
            max-width: 400px;
            flex: 1 1 400px;
        }
        .animation-area {
            max-width: 300px;
            flex: 1 1 300px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.form(key="domain_form"):
        st.markdown('<div class="container">', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="input-area">', unsafe_allow_html=True)
            domain = st.text_input(
                "Enter an Industry/Domain (e.g., AI, Cloud, Cybersecurity):",
                key="domain_input"
            )
            submit = st.form_submit_button("Explore Career Paths")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="animation-area">', unsafe_allow_html=True)
        st_lottie(lottie_career, height=250, key="career_lottie")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    if submit and domain.strip():
        with st.spinner("Fetching career paths and top companies..."):
            try:
                career_info = get_career_paths_and_companies(domain.strip())
            except Exception as e:
                st.error(f"Error fetching career info: {e}")
                career_info = None

        if career_info:
            st.markdown("### Career Paths and Hiring Companies")
            st.markdown(career_info) 

if __name__ == "__main__":
    run()
