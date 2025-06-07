import streamlit as st
from openai import AzureOpenAI

endpoint = st.secrets["openai_endpoint"]
deployment = st.secrets["deployment"] 
subscription_key = st.secrets["openai_key"]
api_version = st.secrets.get("azure_openai_api_version", "2024-12-01-preview")  

client = AzureOpenAI(
    api_key=subscription_key,
    azure_endpoint=endpoint,
    api_version=api_version,
)

def ask_azure_openai(messages):
    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=messages,
            max_tokens=500,
            temperature=1.0,
            top_p=1.0,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"
    