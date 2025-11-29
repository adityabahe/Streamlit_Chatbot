import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Azure OpenAI Chatbot")
st.title("🤖 Azure OpenAI (minimal)")

# --- Sidebar: put your Azure details here ---
azure_endpoint = st.sidebar.text_input(
    "Azure OpenAI Endpoint",
    placeholder="https://<your-resource-name>.openai.azure.com"
)
azure_api_key = st.sidebar.text_input("Azure OpenAI Key", type="password")
deployment = st.sidebar.text_input("Deployment name (model)", placeholder="gpt-4o")

# Simple input area
user_text = st.text_area("Ask something:", "Tell me a short joke about cats.")
if st.button("Send"):
    if not (azure_endpoint and azure_api_key and deployment):
        st.error("Fill the endpoint, key and deployment name in the sidebar.")
    else:
        try:
            # create the client configured for Azure
            client = OpenAI(
                api_key=azure_api_key,
                api_base=azure_endpoint,    # e.g. "https://my-openai-resource.openai.azure.com"
                api_type="azure",
                api_version="2024-12-01"    # use the API version your Azure resource supports
            )

            # call chat completions on the deployment name
            resp = client.chat.completions.create(
                model=deployment,
                messages=[{"role": "user", "content": user_text}],
                temperature=0.7,
                max_tokens=512
            )

            # message content (new SDK: message object with .content)
            reply = resp.choices[0].message.content
            st.success(reply)

        except Exception as e:
            st.error(f"API error: {e}")
