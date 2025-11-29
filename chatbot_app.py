import streamlit as st
from openai import OpenAI

st.title("🤖 Azure OpenAI Chatbot")

# Sidebar Inputs
azure_endpoint = st.sidebar.text_input("Azure OpenAI Endpoint")
azure_api_key = st.sidebar.text_input("Azure OpenAI Key", type="password")
deployment = st.sidebar.text_input("Deployment Name")  # e.g., gpt-4o

def generate_response(prompt):
    client = OpenAI(
        api_key=azure_api_key,
        base_url=f"{azure_endpoint}/openai/deployments/{deployment}"
    )

    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

user_input = st.text_area("Ask something", "Hello!")

if st.button("Submit"):
    if not azure_api_key or not azure_endpoint or not deployment:
        st.error("Please enter all Azure OpenAI details in the sidebar.")
    else:
        try:
            reply = generate_response(user_input)
            st.success(reply)
        except Exception as e:
            st.error(f"Error: {e}")