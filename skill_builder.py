import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from openai import AzureOpenAI
import json
from streamlit_lottie import st_lottie

doc_key = st.secrets["azure_form_recognizer_key"]
doc_endpoint = st.secrets["azure_form_recognizer_endpoint"]

# Updated Azure OpenAI secrets
openai_key = st.secrets["azure_openai_api_key"]
openai_endpoint = st.secrets["azure_openai_endpoint"]
deployment = st.secrets["azure_openai_deployment"]
api_version = st.secrets["azure_openai_api_version"]

doc_client = DocumentAnalysisClient(
    endpoint=doc_endpoint,
    credential=AzureKeyCredential(doc_key)
)

openai_client = AzureOpenAI(
    api_key=openai_key,
    azure_endpoint=openai_endpoint,
    api_version=api_version,
)

def parse_resume(uploaded_file):
    poller = doc_client.begin_analyze_document("prebuilt-read", document=uploaded_file)
    result = poller.result()
    full_text = " ".join([line.content for page in result.pages for line in page.lines])
    return full_text

def analyze_resume_content(resume_text):
    prompt = f"""
You are a career guidance expert. Analyze the following resume content:

\"\"\"{resume_text}\"\"\"

Provide:
1. Key strengths based on skills and experience
2. Gaps or weaknesses to improve
3. A learning roadmap to address these gaps

Respond clearly in a structured format.
"""
    response = openai_client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a helpful and insightful career coach."},
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=1000,
        temperature=0.7
    )
    return response.choices[0].message.content

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_resume = load_lottiefile("animations/Animation - 1749285315567.json") 

def run():
    st.title("🛠️ Skill Builder via Resume")
    st.markdown("Upload your resume to receive personalized feedback on your strengths, weaknesses, and a learning roadmap.")

    st.markdown(
        """
        <style>
        .container {
            display: flex;
            justify-content: center;
            align-items: flex-start;
            gap: 3rem;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        .input-area {
            max-width: 450px;
            flex: 1 1 450px;
        }
        .animation-area {
            max-width: 300px;
            flex: 1 1 300px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="container">', unsafe_allow_html=True)

    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])
    analyze_clicked = st.button("Analyze Resume")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="animation-area">', unsafe_allow_html=True)
    st_lottie(lottie_resume, height=280, key="resume_lottie")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file and analyze_clicked:
        with st.spinner("Reading and analyzing your resume..."):
            try:
                resume_text = parse_resume(uploaded_file)
                analysis = analyze_resume_content(resume_text)

                st.markdown("### ✅ Career Analysis Result")
                st.markdown(analysis)

            except Exception as e:
                st.error(f"Something went wrong: {e}")

if __name__ == "__main__":
    run()
