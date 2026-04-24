import streamlit as st
import pandas as pd
import os
import altair as alt

# --- Page Config ---
st.set_page_config(page_title="Model Evaluation Dashboard", page_icon="🎯", layout="wide")
st.title("🎯 Model Evaluation Dashboard")
st.caption("Internship Project - Data Analyst: Priya Raju Marmat")

# --- Load Data ---
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.abspath(os.path.join(current_dir, "..", "shared-data", "chat_logs_raw.csv"))

@st.cache_data(ttl=5)
def load_data():
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    else:
        return pd.DataFrame()

raw_df = load_data()

# --- Evaluation Logic (Simulating Manual Scoring) ---
def evaluate_interaction(row):
    prompt = str(row.get('user_input', '')).lower()
    bot_response = str(row.get('bot_response', '')).lower()
    
    # Defaults
    expected = "General helpful response"
    relevance = 1
    helpfulness = 3
    
    # Rule 1: Emotional/Mental distress
    if any(w in prompt for w in ["stress", "anxious", "sad", "bad", "not good"]):
        expected = "Empathetic and calming tone"
        if any(w in bot_response for w in ["sorry", "tough", "hear you", "okay", "listen"]):
            relevance = 1
            helpfulness = 5
        else:
            relevance = 0
            helpfulness = 1
            
    # Rule 2: Specific queries (e.g. pricing, product details)
    elif "pricing" in prompt or "cost" in prompt:
        expected = "Direct answer with pricing details or link"
        if "pricing" in bot_response or "cost" in bot_response:
            relevance = 1
            helpfulness = 5
        else:
            relevance = 0
            helpfulness = 1 # Failed to provide specific details
            
    # Rule 3: Support queries
    elif "help" in prompt or "work" in prompt:
        expected = "Clear instructions or clarification request"
        if "how can i help" in bot_response or "tell me" in bot_response or "what's on your mind" in bot_response:
            relevance = 1
            helpfulness = 4
        else:
            relevance = 0
            helpfulness = 2

    return pd.Series([expected, relevance, helpfulness])

# --- Dashboard UI ---
if raw_df.empty:
    st.info("No data available yet. Generate logs via the chatbot first!")
else:
    # Apply evaluation scoring
    eval_df = raw_df.copy()
    eval_df[['expected_response', 'relevance', 'helpfulness']] = eval_df.apply(evaluate_interaction, axis=1)

    # --- Top KPIs ---
    avg_relevance = eval_df['relevance'].mean() * 100
    avg_helpfulness = eval_df['helpfulness'].mean()
    
    st.subheader("System Performance Metrics")
    col1, col2 = st.columns(2)
    col1.metric("Target Relevance Score", f"{avg_relevance:.1f}%")
    col2.metric("Average Helpfulness (1-5)", f"{avg_helpfulness:.1f} / 5.0")
    
    st.divider()

    # --- Response Quality Breakdown ---
    st.subheader("Response Quality Breakdown")
    
    good_responses = eval_df[eval_df['helpfulness'] >= 4]
    poor_responses = eval_df[eval_df['helpfulness'] <= 3]
    
    tab1, tab2 = st.tabs(["✅ High Quality Responses", "⚠️ Poor Responses (Needs Improvement)"])
    
    with tab1:
        st.write("Responses that successfully matched the user intent and provided high value.")
        if not good_responses.empty:
            st.dataframe(
                good_responses[['user_input', 'bot_response', 'expected_response', 'helpfulness']],
                column_config={"user_input": "User Prompt", "bot_response": "Bot Response", "expected_response": "Expected", "helpfulness": "Score"},
                hide_index=True, use_container_width=True
            )
        else:
            st.info("No high quality responses logged yet.")
            
    with tab2:
        st.write("Responses that failed to meet the expected criteria.")
        if not poor_responses.empty:
            st.dataframe(
                poor_responses[['user_input', 'bot_response', 'expected_response', 'relevance', 'helpfulness']],
                column_config={"user_input": "User Prompt", "bot_response": "Bot Response", "expected_response": "Expected", "relevance": "Matched Intent?", "helpfulness": "Score"},
                hide_index=True, use_container_width=True
            )
        else:
            st.success("No poor responses found! Excellent.")

    st.divider()

    # --- Improvement Opportunities ---
    st.subheader("Improvement Opportunities")
    st.markdown("""
    Based on the manual evaluation of the raw chat logs, the following systemic issues have been identified:
    
    * **Generic Fallbacks on Specific Queries**: The model scores low on `relevance` when users ask for specific facts (like pricing or features) because it relies on generic conversational fallbacks. 
    * **Intent Mismatch**: Missing specific intent mapping causes a drop in the `Helpfulness Score` from a 5 to a 1.
    * **Recommendation for AI Engineer (Dipak)**: Update `app.py` prompt logic to include specific `if/elif` branches for domain queries (e.g., pricing, login help) rather than routing them to the general response pool.
    """)
    
    st.divider()
    
    with st.expander("View Full Evaluation Dataset"):
        st.dataframe(eval_df[['timestamp', 'user_input', 'bot_response', 'expected_response', 'relevance', 'helpfulness']], use_container_width=True)
