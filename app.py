import streamlit as st
import pandas as pd
import plotly.express as px
from utils.llm_query import generate_analysis, generate_insight


# Page configuration
st.set_page_config(
    page_title="ChatBI Dashboard",
    page_icon="📊",
    layout="wide",
)

# Hero section
st.markdown("""
# 📊 ChatBI — AI Powered Business Intelligence

Ask questions about your data and generate dashboards instantly.

Upload a dataset and start chatting with your data.
""")

# Chat memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar controls
st.sidebar.header("⚙ Dashboard Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV Dataset",
    type=["csv"]
)

if st.sidebar.button("Clear Conversation"):
    st.session_state.chat_history = []


# Main app logic
if uploaded_file:

    try:
        df = pd.read_csv(uploaded_file, encoding="utf-8")
    except:
        try:
            df = pd.read_csv(uploaded_file, encoding="latin-1")
        except:
            df = pd.read_csv(uploaded_file, encoding="ISO-8859-1")

    # -----------------------------
    # Sidebar Filters
    # -----------------------------
    st.sidebar.subheader("🔎 Filters")

    categorical_cols = df.select_dtypes(exclude="number").columns
    selected_filters = {}

    for col in categorical_cols:

        unique_values = df[col].unique()

        selected_values = st.sidebar.multiselect(
            f"Filter {col}",
            unique_values,
            default=unique_values
        )

        selected_filters[col] = selected_values

    # Apply filters
    for col, values in selected_filters.items():
        df = df[df[col].isin(values)]


    # -----------------------------
    # Dataset Overview (KPI Cards)
    # -----------------------------
    st.subheader("📊 Dataset Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])

    numeric_cols = df.select_dtypes(include="number").columns

    if "Sales" in df.columns:
        col3.metric("Total Sales", int(df["Sales"].sum()))
    else:
        col3.metric("Numeric Columns", len(numeric_cols))


    # -----------------------------
    # Dataset Preview
    # -----------------------------
    st.divider()

    st.subheader("📄 Dataset Preview")

    st.dataframe(df)


    # -----------------------------
    # Sample Prompts
    # -----------------------------
    st.divider()

    st.subheader("💡 Try asking:")

    st.markdown("""
    • Show sales by region  
    • Show product distribution  
    • Show sales trend  
    • Compare sales across regions  
    """)


    # -----------------------------
    # User Question
    # -----------------------------
    question = st.text_input(
        "💬 Ask a question about the data",
        placeholder="Example: Show sales by region"
    )


    if question:

        st.session_state.chat_history.append(question)

        # Show chat history
        st.subheader("🗨 Conversation History")

        for q in st.session_state.chat_history:
            st.write("User:", q)


        columns = list(df.columns)

        # AI analysis
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


        # Group data
        try:
            result = df.groupby(group_column)[value_column].sum().reset_index()
        except:
            st.error("Could not process dataset with AI suggestion.")
            st.stop()


        # -----------------------------
        # Dashboard Charts
        # -----------------------------
        st.subheader("📊 AI Generated Dashboard")

        col1, col2 = st.columns(2)

        # Bar Chart
        with col1:
            fig_bar = px.bar(
                result,
                x=group_column,
                y=value_column,
                title="Comparison Chart"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            st.divider()

            st.subheader("🤖 AI Insights")

            try:
                summary = result.head(10).to_string()

                insight = generate_insight(summary)

                st.info(insight)

            except:
                st.warning("Could not generate AI insights.")

        # Pie Chart
        with col2:
            fig_pie = px.pie(
                result,
                names=group_column,
                values=value_column,
                title="Distribution Chart"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            st.divider()

            st.subheader("🤖 AI Insights")

            try:
                summary = result.head(10).to_string()

                insight = generate_insight(summary)

                st.info(insight)

            except:
                st.warning("Could not generate AI insights.")


        # Trend chart if Date column exists
    if "Date" in df.columns:

        try:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

            trend = df.groupby("Date")[value_column].sum().reset_index()

            fig_line = px.line(trend, x="Date", y=value_column, title="Trend Chart")

            st.plotly_chart(fig_line, use_container_width=True)
            st.divider()

            st.subheader("🤖 AI Insights")

            try:
                summary = result.head(10).to_string()

                insight = generate_insight(summary)

                st.info(insight)

            except:
                st.warning("Could not generate AI insights.")

        except:
            st.warning("Could not generate trend chart from Date column.")


        # -----------------------------
        # AI Insights (Optional)
        # -----------------------------
        st.subheader("🤖 AI Insights")

        summary = result.head(10).to_string()

        insight = generate_insight(summary)

        st.write(insight)

