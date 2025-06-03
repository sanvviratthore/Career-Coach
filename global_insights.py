import streamlit as st
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Azure Document Intelligence setup
AZURE_FORM_RECOGNIZER_ENDPOINT = "https://careercoach-formrecognizer.cognitiveservices.azure.com/"
AZURE_FORM_RECOGNIZER_KEY = "ElgiMCrTNyuLEyrikbAIjuQHUD9lzVrLT242zHAxdD4iTQewXj7aJQQJ99BFACYeBjFXJ3w3AAALACOGtUSC"  # Replace securely in production

client = DocumentAnalysisClient(
    endpoint=AZURE_FORM_RECOGNIZER_ENDPOINT,
    credential=AzureKeyCredential(AZURE_FORM_RECOGNIZER_KEY)
)

def extract_text(uploaded_file):
    try:
        poller = client.begin_analyze_document("prebuilt-document", document=uploaded_file)
        result = poller.result()
        full_text = ""
        for page in result.pages:
            for line in page.lines:
                full_text += line.content + " "
        return full_text.lower()
    except Exception as e:
        st.error(f"Failed to extract document content. Error: {e}")
        return ""

def run():
    st.title("🌍 Global Insights")

    st.markdown("""
    Welcome to the **Global Insights** section, where we'll help you understand:

    - Industry trends and job market analytics powered by **Azure OpenAI** and **Azure Machine Learning**.
    - Geospatial insights and location-based visualizations using **Azure Maps**.
    - Document intelligence to extract career-relevant insights with **Azure Document Intelligence**.
    """)

    st.markdown("---")
    st.subheader("📈 Job Market Trends")
    st.info("Job market trend graphs will appear here once integrated.")

    st.markdown("---")
    st.subheader("🗺️ Geospatial Job Data")
    st.info("Azure Maps visualizations will be displayed here.")

    st.markdown("---")
    st.subheader("📄 Document Intelligence Insights")

    uploaded_file = st.file_uploader("Upload a resume, cover letter, or job description (PDF)", type=["pdf"])
    if uploaded_file:
        with st.spinner("Analyzing document..."):
            extracted_text = extract_text(uploaded_file)

        if extracted_text:
            st.success("Text successfully extracted! Here's a preview:")
            st.text_area("📄 Extracted Content Preview", extracted_text[:1000], height=200)

            # Optional: Simple keyword check
            keywords = ["python", "machine learning", "communication", "team", "intern", "developer"]
            found_keywords = [kw for kw in keywords if kw in extracted_text]

            if found_keywords:
                st.markdown("### 🔍 Keywords Detected:")
                for kw in found_keywords:
                    st.markdown(f"- {kw.title()}")
            else:
                st.info("No predefined keywords found.")
        else:
            st.warning("No text extracted from document.")

    st.markdown("---")
    st.caption("Stay tuned as we build out these features with live data and interactive charts!")

