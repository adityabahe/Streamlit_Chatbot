import streamlit as st
from openai import AzureOpenAI

st.title("🤖 Azure OpenAI Chatbot (Streamlit)")

# Sidebar: Azure settings
azure_endpoint = st.sidebar.text_input(
    "Azure OpenAI Endpoint",
    placeholder="https://openai-genesis-poc-swedencentral.openai.azure.com/"
)
azure_api_key = st.sidebar.text_input("Azure OpenAI Key", type="password")
azure_deployment = st.sidebar.text_input("Deployment Name", placeholder="test-gpt4o-mini")

def generate_response(user_input: str):
    client = AzureOpenAI(
        api_key=azure_api_key,
        azure_endpoint=azure_endpoint,
        api_version="2025-01-01-preview",
    )

    response = client.chat.completions.create(
        model=azure_deployment,     # your Azure deployment name
        messages=[{"role": "user", "content": user_input}],
        temperature=0.7,
    )

    st.info(response.choices[0].message["content"])


with st.form("input_form"):
    user_text = st.text_area("Enter your question:", value="Tell me a fun fact!")
    submitted = st.form_submit_button("Send")

    if submitted:
        if not azure_api_key or not azure_endpoint or not azure_deployment:
            st.warning("Please fill all Azure OpenAI fields!", icon="⚠")
        else:
            generate_response(user_text)