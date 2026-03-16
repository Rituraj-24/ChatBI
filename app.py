import streamlit as st
import pandas as pd
import plotly.express as px
from utils.llm_query import generate_analysis, generate_insight
import streamlit as st

st.set_page_config(
    page_title="ChatBI Dashboard",
    page_icon="📊",
    layout="wide",
)


st.markdown("""
# 📊 ChatBI — AI Powered Business Intelligence
Ask questions about your data and generate dashboards instantly.

Upload a dataset and start chatting with your data.
""")
if st.button("Clear Conversation"):
    st.session_state.chat_history = []

# Chat memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader("Upload your CSV dataset", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)
    # KPI Cards
    st.subheader("📊 Dataset Overview")
    
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    
    # show total sales if column exists
    if "Sales" in df.columns:
        col3.metric("Total Sales", int(df["Sales"].sum()))
    else:
        col3.metric("Numeric Columns", len(df.select_dtypes(include="number").columns))

    st.subheader("Dataset Preview")
    st.dataframe(df)

    question = st.text_input("Ask a question about the data")

    if question:

        # Save question to chat history
        st.session_state.chat_history.append(question)

        st.subheader("Conversation History")

        for q in st.session_state.chat_history:
            st.write("User:", q)

        columns = list(df.columns)

        # Combine chat history for context
        analysis = generate_analysis(question, columns)

        try:
            group_column, value_column, chart_type = analysis.split(",")

            group_column = group_column.strip()
            value_column = value_column.strip()
            chart_type = chart_type.strip().lower()

        except:
            st.error("AI returned an unexpected format. Please try another question.")
            st.write("AI Output:", analysis)
            st.stop()

        try:
            result = df.groupby(group_column)[value_column].sum().reset_index()
        except:
            st.error("Could not process the dataset with AI suggestion.")
            st.stop()

        # Generate chart
        if chart_type == "bar":
            fig = px.bar(result, x=group_column, y=value_column)

        elif chart_type == "pie":
            fig = px.pie(result, names=group_column, values=value_column)

        elif chart_type == "line":
            fig = px.line(result, x=group_column, y=value_column)

        else:
            st.error("Unsupported chart type returned by AI.")
            st.stop()

        st.subheader("AI Generated Dashboard")

        col1, col2 = st.columns(2)

        # Bar chart
        with col1:
            fig_bar = px.bar(result, x=group_column, y=value_column, title="Comparison Chart")
            st.plotly_chart(fig_bar, use_container_width=True)

        # Pie chart
        with col2:
            fig_pie = px.pie(result, names=group_column, values=value_column, title="Distribution Chart")
            st.plotly_chart(fig_pie, use_container_width=True)

        # Trend chart (if Date column exists)
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"])
            trend = df.groupby("Date")[value_column].sum().reset_index()

            fig_line = px.line(trend, x="Date", y=value_column, title="Trend Chart")

            st.plotly_chart(fig_line, use_container_width=True)

        # AI Insights
        # st.subheader("AI Insights")

        # summary = result.head(10).to_string()

        # insight = generate_insight(summary)

        # st.write(insight)
