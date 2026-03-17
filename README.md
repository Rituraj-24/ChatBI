# 📊 ChatBI — AI Powered Business Intelligence Dashboard

ChatBI is an AI-powered Business Intelligence tool that allows users to upload datasets and generate interactive dashboards using natural language queries.

Instead of writing SQL or manually creating charts, users can simply ask questions about their data and ChatBI automatically generates the appropriate visualizations.

## 🚀 Live Demo

Try the deployed application here:

👉 https://chatbi-ai.streamlit.app/

## ✨ Features

- 📁 Upload any CSV dataset
- 💬 Ask questions about your data in natural language
- 📊 Automatic chart generation (Bar, Pie, Line)
- 🤖 AI-powered data interpretation using Gemini LLM
- 📈 Trend analysis
- 🔎 Sidebar filters for dataset exploration
- 🧠 AI insights panel explaining chart patterns
- ⚡ Interactive dashboard powered by Streamlit

## 🧠 How It Works

1. User uploads a dataset
2. User asks a question about the data
3. AI interprets the question
4. The system identifies:
   - grouping column
   - value column
   - chart type
5. Chart is automatically generated
6. AI generates insights explaining the chart

## 🛠 Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- Gemini API (Google Generative AI)

## 📂 Project Structure
ChatBI
│
├── app.py # Main Streamlit dashboard
├── requirements.txt # Project dependencies
│
├── dataset
│ └── sales.csv # Example dataset
│
├── utils
│ └── llm_query.py # AI query interpretation
│
└── .streamlit
└── secrets.toml # API key (not uploaded to GitHub)

---

## ⚙ Installation (Run Locally)

Clone the repository:

```bash
git clone https://github.com/yourusername/chatbi.git

