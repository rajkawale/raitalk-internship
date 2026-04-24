import streamlit as st
import pandas as pd
import os
import altair as alt

# --- Page Config ---
st.set_page_config(page_title="Analytics Dashboard", page_icon="📊", layout="wide")
st.title("📊 Chatbot Analytics Dashboard")
st.caption("Internship Project - Data Analyst: Sayali Pramod More")

# --- Load Data ---
data_path = os.path.join("..", "shared-data", "chat_logs_raw.csv")

@st.cache_data(ttl=5) # Refresh every 5 seconds to capture live logs
def load_data():
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    else:
        return pd.DataFrame()

df = load_data()

# --- Dashboard UI ---
if df.empty:
    st.info("No data available yet. Start chatting with the bot to generate logs!")
else:
    # Ensure feedback columns exist (backward compatibility)
    if 'feedback' not in df.columns:
        df['feedback'] = "unrated"
        df['optional_comment'] = ""
        
    df['feedback'] = df['feedback'].fillna("unrated")
    df['optional_comment'] = df['optional_comment'].fillna("")

    # --- KPIs ---
    total_interactions = len(df)
    positive_count = len(df[df['feedback'] == 'positive'])
    negative_count = len(df[df['feedback'] == 'negative'])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Interactions", total_interactions)
    col2.metric("👍 Positive Feedback", positive_count)
    col3.metric("👎 Negative Feedback", negative_count)
    
    st.divider()

    # --- Charts & Tables Layout ---
    chart_col, table_col = st.columns([1, 1])
    
    with chart_col:
        st.subheader("Feedback Breakdown")
        
        # Prepare data for chart
        feedback_counts = df['feedback'].value_counts().reset_index()
        feedback_counts.columns = ['Feedback Type', 'Count']
        
        # Filter out 'unrated' for cleaner chart if preferred, or keep it
        feedback_counts = feedback_counts[feedback_counts['Feedback Type'].isin(['positive', 'negative'])]
        
        if not feedback_counts.empty:
            chart = alt.Chart(feedback_counts).mark_bar().encode(
                x='Feedback Type',
                y='Count',
                color=alt.Color('Feedback Type', scale=alt.Scale(domain=['positive', 'negative'], range=['#4CAF50', '#F44336']))
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No feedback ratings submitted yet.")

    with table_col:
        st.subheader("Actionable Insights (Negative Feedback)")
        
        # Filter for negative feedback with comments
        neg_df = df[(df['feedback'] == 'negative') & (df['optional_comment'] != "")]
        
        if not neg_df.empty:
            st.dataframe(
                neg_df[['timestamp', 'bot_response', 'optional_comment']],
                column_config={
                    "timestamp": "Time",
                    "bot_response": "Bot Said",
                    "optional_comment": "User Comment"
                },
                hide_index=True,
                height=300
            )
        else:
            st.success("No negative feedback comments yet! Great job.")

    # --- Raw Data Expander ---
    with st.expander("View Raw Data Logs"):
        st.dataframe(df, use_container_width=True)
        
    # Auto-refresh button
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
