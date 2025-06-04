import streamlit as st
from openai import AzureOpenAI

# --- Azure OpenAI connection details (fill in your own) ---------------
API_VERSION   = "2024-12-01-preview"
AZURE_ENDPOINT = "https://careercoach-openai.openai.azure.com/"
DEPLOYMENT     = "gpt-35-turbo"        # your deployment name
API_KEY        = "2MTbbBLRpmpNv7sP6UJYF3kM3CuUhbVUL1Dad0mYzUoeVPuBvL8GJQQJ99BFAC77bzfXJ3w3AAABACOGUO8O" # keep visible per your request
# ---------------------------------------------------------------------

client = AzureOpenAI(
    api_version   = API_VERSION,
    azure_endpoint= AZURE_ENDPOINT,
    api_key       = API_KEY,
)

SYSTEM_PROMPT = (
    "You are a course-recommendation assistant. "
    "When given a tech topic, output **exactly 10** up-to-date online courses. "
    "For each course, return a Markdown bullet with: "
    "• **Course Title**  • Platform  • 1-line reason  • Link. "
    "Keep responses concise."
)

@st.cache_data(show_spinner=False, ttl=86400)
def recommend_courses(topic: str) -> str:
    """Call Azure OpenAI and return raw Markdown."""
    chat = client.chat.completions.create(
        model     = DEPLOYMENT,
        messages  = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": topic.strip()},
        ],
        temperature = 0.7,
        max_tokens  = 800,
    )
    return chat.choices[0].message.content

def run():
    st.title("🎯 Course Recommendations")
    topic = st.text_input("What do you want to learn? (e.g., ‘Flutter’, ‘Data Engineering’)")
    
    if topic:
        with st.spinner("Fetching top courses…"):
            md = recommend_courses(topic)
        st.markdown(md, unsafe_allow_html=True)

# Allow standalone execution
if __name__ == "__main__":
    run()

