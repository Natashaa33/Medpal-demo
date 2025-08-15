import streamlit as st
from datetime import datetime
import requests
import os

# Hugging Face API setup
HF_API_KEY = st.secrets.get("HF_API_KEY", "")  # Store key in Streamlit secrets for safety
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

def query_hf(prompt):
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    if response.status_code == 200:
        return response.json()[0]['generated_text']
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit UI
st.set_page_config(page_title="MedPal", page_icon="💊")
st.title("MedPal - AI Health Companion")

# Medication logging
st.subheader("Log your Medication")
med = st.text_input("Medication Name")
dose = st.text_input("Dose")
if st.button("Save Medication"):
    st.success(f"Saved: {med} ({dose}) at {datetime.now().strftime('%H:%M')}")

# Health log
st.subheader("Log your Symptoms / Vitals")
symptom = st.text_input("Symptom / Vitals")
if st.button("Log Symptom"):
    st.success(f"Logged: {symptom} at {datetime.now().strftime('%H:%M')}")

# AI Chatbot
st.subheader("Ask MedPal")
question = st.text_input("Type your health question")
if st.button("Ask"):
    if not HF_API_KEY:
        st.error("No Hugging Face API key found. Please add it to Streamlit Secrets.")
    else:
        answer = query_hf(question)
        st.info(answer)
