import streamlit as st
import pandas as pd
import os
import altair as alt

# --- Page Config ---
st.set_page_config(page_title="Analytics Dashboard", page_icon="📊", layout="wide")
st.title("📊 Chatbot Analytics Dashboard")
st.caption("Internship Project - Data Analyst: Sayali Pramod More")

# --- Load Data ---
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.abspath(os.path.join(current_dir, "..", "shared-data", "chat_logs_raw.csv"))

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
    # Ensure feedback columns exist
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

    # --- Feedback Breakdown & Actionable Insights ---
    chart_col, table_col = st.columns([1, 1])
    
    with chart_col:
        st.subheader("Feedback Breakdown")
        feedback_counts = df['feedback'].value_counts().reset_index()
        feedback_counts.columns = ['Feedback Type', 'Count']
        feedback_counts = feedback_counts[feedback_counts['Feedback Type'].isin(['positive', 'negative'])]
        
        if not feedback_counts.empty:
            chart = alt.Chart(feedback_counts).mark_bar().encode(
                x='Feedback Type',
                y='Count',
                color=alt.Color('Feedback Type', scale=alt.Scale(domain=['positive', 'negative'], range=['#4CAF50', '#F44336']))
            ).properties(height=250)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No feedback ratings submitted yet.")

    with table_col:
        st.subheader("Actionable Insights")
        st.caption("Top 5 recent negative feedback comments")
        # Filter for negative feedback with comments
        neg_df = df[(df['feedback'] == 'negative') & (df['optional_comment'] != "")]
        
        if not neg_df.empty:
            st.dataframe(
                neg_df.tail(5)[['timestamp', 'bot_response', 'optional_comment']],
                column_config={
                    "timestamp": "Time",
                    "bot_response": "Bot Said",
                    "optional_comment": "User Comment"
                },
                hide_index=True,
                height=250
            )
        else:
            st.success("No negative feedback comments yet! Great job.")

    st.divider()

    # --- Deep Dive: Top Issues & Recommendations ---
    st.subheader("Deep Dive: Negative Feedback Analysis")
    
    # Categorization Logic
    def categorize_issue(comment):
        if not isinstance(comment, str) or comment.strip() == "":
            return "Other"
        c = comment.lower()
        if any(w in c for w in ["generic", "not helpful"]):
            return "Generic Response"
        elif any(w in c for w in ["pricing", "doesn't answer", "not answering"]):
            return "Missing Specific Answer"
        elif any(w in c for w in ["confusing", "don't understand"]):
            return "Unclear Response"
        return "Other"

    if not neg_df.empty:
        neg_df = neg_df.copy()
        neg_df['issue_type'] = neg_df['optional_comment'].apply(categorize_issue)
        
        issue_col, action_col = st.columns([1, 1])
        
        with issue_col:
            st.write("**Top Issues Identified**")
            issue_counts = neg_df['issue_type'].value_counts().reset_index()
            issue_counts.columns = ['Issue Category', 'Count']
            
            issue_chart = alt.Chart(issue_counts).mark_bar(color='#FFA726').encode(
                x=alt.X('Count', axis=alt.Axis(tickMinStep=1)), # Ensure integers
                y=alt.Y('Issue Category', sort='-x')
            ).properties(height=200)
            st.altair_chart(issue_chart, use_container_width=True)
            
        with action_col:
            st.write("**Recommended Actions**")
            st.markdown("""
            * **Generic Response** → Improve prompt specificity
            * **Missing Specific Answer** → Add domain-specific responses (like pricing, features)
            * **Unclear Response** → Simplify language and structure
            * **Other** → Review manually
            """)
    else:
        st.info("Not enough negative feedback to generate deep-dive analytics.")

    st.divider()

    # --- Raw Data Expander ---
    with st.expander("View Raw Data Logs"):
        st.dataframe(df, use_container_width=True)
        
    # Auto-refresh button
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
