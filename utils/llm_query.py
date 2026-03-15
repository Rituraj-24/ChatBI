import google.generativeai as genai

genai.configure(api_key="AIzaSyD8tVM2ZMQ1tJ7demEh9dOr75HwT27hgyY")

def generate_analysis(question, columns):

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
You are a data analyst.

User question: {question}

Dataset columns: {columns}

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
