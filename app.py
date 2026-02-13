import streamlit as st
import google.generativeai as genai
import json
import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="BuildWise AI Planner", layout="wide")
st.title("🏗 BuildWise — AI Construction Planner")

# ---------- API KEY INPUT ----------
api_key = st.text_input("Enter Google AI Studio API Key", type="password")

# Only configure model if API key entered
model = None
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
    except Exception as e:
        st.error(f"Error configuring API key: {e}")

# ---------- SIDEBAR INPUT ----------
st.sidebar.header("Project Details")
project_name = st.sidebar.text_input("Project Name")
project_type = st.sidebar.selectbox("Project Type", ["House", "Apartment", "Bridge", "Road", "Mall", "Office"])
budget = st.sidebar.number_input("Budget (₹)", min_value=10000)
duration = st.sidebar.number_input("Duration (Days)", min_value=1)
workers = st.sidebar.slider("Workers", 1, 500, 20)
materials = st.sidebar.text_area("Materials Required")
location = st.sidebar.text_input("Location")
generate = st.sidebar.button("Generate Plan")

# ---------- AI FUNCTION ----------
def ask_ai(prompt):
    if not api_key or model is None:
        return "⚠ Please enter a valid API key first."

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"ERROR: {e}"

# ---------- GENERATE PLAN ----------
if generate:
    st.success("Generating AI Plan...")
    base_prompt = f"""
You are a professional construction planning AI.

Project Name: {project_name}
Type: {project_type}
Budget: {budget}
Duration: {duration} days
Workers: {workers}
Materials: {materials}
Location: {location}

Generate:
1. Cost breakdown
2. Schedule timeline
3. Resource allocation
4. Risk analysis
5. Optimization suggestions

Format clearly with headings.
"""
    result = ask_ai(base_prompt)
    st.markdown(result)

# ---------- TABS ----------
tab1, tab2, tab3, tab4 = st.tabs(["Cost Estimator","Scheduler","Resources","AI Assistant"])

# ---------- COST ESTIMATOR ----------
with tab1:
    if st.button("Estimate Cost"):
        prompt = f"Estimate detailed construction cost breakdown for a {project_type} with budget {budget}"
        st.write(ask_ai(prompt))

# ---------- SCHEDULER ----------
with tab2:
    if st.button("Generate Schedule"):
        prompt = f"Create construction timeline schedule for {project_type} lasting {duration} days"
        st.write(ask_ai(prompt))

# ---------- RESOURCES ----------
with tab3:
    if st.button("Plan Resources"):
        prompt = f"Plan resource allocation for {workers} workers building a {project_type}"
        st.write(ask_ai(prompt))

# ---------- CHATBOT ----------
with tab4:
    user_q = st.text_input("Ask construction question")
    if st.button("Ask"):
        if user_q:
            reply = ask_ai(user_q)
            st.write(reply)

# ---------- FOOTER ----------
st.markdown("---")
st.caption("AI Construction Planner • Powered by Gemini + Streamlit")