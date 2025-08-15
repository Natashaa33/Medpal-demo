import streamlit as st
from datetime import datetime
from openai import OpenAI

# Initialize OpenAI client (reads key from Streamlit secrets)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        answer = response.choices[0].message.content
        st.info(answer)
    except Exception as e:
        st.error(f"Error: {e}")
