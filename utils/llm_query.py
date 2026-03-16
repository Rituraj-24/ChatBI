import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def generate_analysis(question, columns):

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
You are a data analyst.

User question: {question}

Dataset information:
{columns}
Identify:
1. Which column should be used for grouping
2. Which column should be used as value
3. Suggest chart type (bar, pie, line)

Return ONLY in this format:
group_column,value_column,chart_type
"""

    response = model.generate_content(prompt)

    return response.text.strip()

def generate_insight(data_summary):

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
You are a business data analyst.

Analyze the following summarized data and provide 2–3 short insights.

Data:
{data_summary}

Respond in simple bullet points.
"""

    response = model.generate_content(prompt)

    return response.text.strip()