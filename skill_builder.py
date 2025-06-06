import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from openai import AzureOpenAI

# === Azure Credentials ===
# Azure Document Intelligence
doc_key = "ElgiMCrTNyuLEyrikbAIjuQHUD9lzVrLT242zHAxdD4iTQewXj7aJQQJ99BFACYeBjFXJ3w3AAALACOGtUSC"
doc_endpoint = "https://careercoach-formrecognizer.cognitiveservices.azure.com/"

# Azure OpenAI
openai_key = "F8cvPQQ5iKHG8NUJY0GbhH4Zxhll5BJQUMOapCLVoDQ6xX9V70tYJQQJ99BFACHYHv6XJ3w3AAAAACOGaJVI"
openai_endpoint = "https://sanvi-mbf58gtv-eastus2.cognitiveservices.azure.com/"
deployment = "gpt-4.1"

# === Setup Clients ===
doc_client = DocumentAnalysisClient(
    endpoint=doc_endpoint,
    credential=AzureKeyCredential(doc_key)
)

openai_client = AzureOpenAI(
    api_key=openai_key,
    azure_endpoint=openai_endpoint,
    api_version="2024-12-01-preview"
)

# === Helper Functions ===
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

# === Streamlit Page ===
def run():
    st.title("🛠️ Skill Builder via Resume")
    st.markdown("Upload your resume to receive personalized feedback on your strengths, weaknesses, and a learning roadmap.")

    uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

    if uploaded_file and st.button("Analyze Resume"):
        with st.spinner("Reading and analyzing your resume..."):
            try:
                resume_text = parse_resume(uploaded_file)
                analysis = analyze_resume_content(resume_text)

                st.markdown("### ✅ Career Analysis Result")
                st.write(analysis)

            except Exception as e:
                st.error(f"Something went wrong: {e}")
