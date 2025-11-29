# app.py — Minimal Azure OpenAI + Streamlit chat example
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Azure OpenAI Chat (minimal)")
st.title("Azure OpenAI — Minimal Chat")

# --- Credentials: prefer st.secrets (Streamlit Cloud) but allow manual entry ---
col1, col2 = st.columns(2)
with col1:
    AZURE_OPENAI_ENDPOINT = st.text_input(
        "Azure OpenAI Endpoint (base URL)",
        placeholder="https://<your-resource>.openai.azure.com"
    )
with col2:
    AZURE_OPENAI_KEY = st.text_input("Azure OpenAI Key", type="password")

AZURE_OPENAI_DEPLOYMENT = st.text_input("Deployment name (model)", placeholder="gpt-4o-deploy")

# helper: create client
def make_client(key: str, base: str):
    return OpenAI(
        api_key=key,
        api_base=base,
        api_type="azure",
        api_version="2025-01-01-preview"  # or the API version your resource requires
    )

def generate_response(prompt: str) -> str:
    client = make_client(AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT)
    resp = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=512,
    )
    # use .content attribute — DO NOT index the message as a dict
    return resp.choices[0].message.content

# ---- UI ----
prompt = st.text_area("Prompt", "What are three quick tips to learn programming?")
if st.button("Send"):
    if not (AZURE_OPENAI_KEY and AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT):
        st.error("Please fill in endpoint, key and deployment name.")
    else:
        try:
            with st.spinner("Thinking..."):
                answer = generate_response(prompt)
            st.markdown("**Assistant:**")
            st.write(answer)
        except Exception as e:
            st.error(f"API call failed: {e}")