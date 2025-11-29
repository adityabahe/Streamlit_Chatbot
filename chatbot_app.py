# chatbot_app.py
import streamlit as st
from langchain_openai import AzureChatOpenAI   # LangChain Azure wrapper
from dotenv import load_dotenv
import os

load_dotenv()  # optional if you use a .env

st.set_page_config(page_title="Azure OpenAI Chatbot")
st.title("🦜🔗 Azure OpenAI Quickstart")

# collect Azure credentials (sidebar)
azure_endpoint = st.sidebar.text_input(
    "Azure OpenAI Endpoint",
    placeholder="https://<your-resource>.openai.azure.com/",
    value=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
)
azure_key = st.sidebar.text_input(
    "Azure OpenAI Key",
    type="password",
    value=os.getenv("AZURE_OPENAI_KEY", ""),
)
deployment = st.sidebar.text_input(
    "Deployment Name",
    placeholder="your-deployment-name",
    value=os.getenv("AZURE_OPENAI_DEPLOYMENT", ""),
)
api_version = st.sidebar.text_input(
    "API Version (optional)",
    value=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-01")
)

# simple helper
def generate_response(input_text: str) -> str:
    # validate
    if not (azure_endpoint and azure_key and deployment):
        raise ValueError("Fill Azure endpoint, key and deployment name in the sidebar.")

    model = AzureChatOpenAI(
        deployment_name=deployment,
        openai_api_base=azure_endpoint,
        openai_api_key=azure_key,
        openai_api_version=api_version,
        temperature=0.7,
    )
    # .invoke returns a string (LangChain wrapper)
    return model.invoke(input_text)

# chat form
with st.form("my_form"):
    user_text = st.text_area(
        "Enter text:",
        "What are the three key pieces of advice for learning how to code?",
    )
    submitted = st.form_submit_button("Submit")

if submitted:
    if not azure_key:
        st.warning("Please enter your Azure OpenAI Key in the sidebar.", icon="⚠")
    else:
        try:
            reply = generate_response(user_text)
            st.success(reply)
        except Exception as e:
            st.error(f"Error: {e}")s