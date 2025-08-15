
import streamlit as st
from datetime import datetime
import requests

st.set_page_config(page_title="MedPal", page_icon="💊")
st.title("MedPal - AI Health Companion")

# ---------------- Hugging Face API setup ----------------
HF_API_KEY = st.secrets.get("HF_API_KEY", "")
API_URL = "https://api-inference.huggingface.co/models/gpt2"  # Free model
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

def query_hf(prompt):
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            return data[0].get('generated_text', "No response text found.")
        elif isinstance(data, dict) and 'error' in data:
            return f"Model error: {data['error']}"
        else:
            return str(data)
    else:
        return f"Error: {response.status_code} - {response.text}"

# ---------------- Session State Initialization ----------------
if "med_logs" not in st.session_state:
    st.session_state.med_logs = []

if "symptom_logs" not in st.session_state:
    st.session_state.symptom_logs = []

# ---------------- Medication Logging ----------------
st.subheader("Log your Medication")
med = st.text_input("Medication Name", key="med_name")
dose = st.text_input("Dose", key="med_dose")

if st.button("Save Medication"):
    if med and dose:
        st.session_state.med_logs.append(f"{med} ({dose}) at {datetime.now().strftime('%H:%M')}")
        st.success("Medication saved!")
    else:
        st.error("Please enter both medication name and dose.")

if st.session_state.med_logs:
    st.write("**Medication History:**")
    for log in st.session_state.med_logs:
        st.write(log)

# ---------------- Symptom / Vitals Logging ----------------
st.subheader("Log your Symptoms / Vitals")
symptom = st.text_input("Symptom / Vitals", key="symptom_input")

if st.button("Log Symptom"):
    if symptom:
        st.session_state.symptom_logs.append(f"{symptom} at {datetime.now().strftime('%H:%M')}")
        st.success("Symptom logged!")
    else:
        st.error("Please enter a symptom or vital.")

if st.session_state.symptom_logs:
    st.write("**Symptom / Vitals History:**")
    for log in st.session_state.symptom_logs:
        st.write(log)

# ---------------- AI Chatbot ----------------
st.subheader("Ask MedPal")
question = st.text_input("Type your health question", key="question_input")

if st.button("Ask"):
    if not HF_API_KEY:
        st.error("No Hugging Face API key found. Please add it to Streamlit Secrets.")
    elif not question:
        st.error("Please type a question to ask MedPal.")
    else:
        with st.spinner("MedPal is thinking..."):
            answer = query_hf(question)
            st.info(answer)
