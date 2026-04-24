import streamlit as st
import pandas as pd
from datetime import datetime
import os
import random

# Define the path for the CSV log
log_file_path = os.path.join("..", "shared-data", "chat_logs_raw.csv")

def save_to_csv(data_dict):
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    df = pd.DataFrame([data_dict])
    if os.path.exists(log_file_path):
        df.to_csv(log_file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(log_file_path, mode='w', header=True, index=False)

st.title("AI Chatbot Demo")

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_bot_response" not in st.session_state:
    st.session_state.last_bot_response = ""

# Response Variations
empathetic_responses = [
    "I'm really sorry you're dealing with this. I'm here for you.",
    "That sounds tough. Do you want to talk more about it?",
    "I hear you. It's totally okay to feel that way.",
    "I'm sorry things are hard right now. I'm listening."
]

general_responses = [
    "Got it. Tell me a bit more.",
    "I see. What's on your mind today?",
    "Thanks for sharing. How can I help you with that?",
    "Interesting. Could you elaborate on that?"
]

def get_response(user_input):
    user_input_lower = user_input.lower()
    
    if any(word in user_input_lower for word in ["not good", "bad", "sad", "stress", "anxious"]):
        pool = empathetic_responses
    else:
        pool = general_responses
        
    # Prevent exact repeat
    choices = [r for r in pool if r != st.session_state.last_bot_response]
    if not choices: 
        choices = pool
        
    selected = random.choice(choices)
    st.session_state.last_bot_response = selected
    return selected

# Render Chat History
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # Feedback UI for assistant messages
        if msg["role"] == "assistant":
            state = msg.get("feedback_state", "unrated")
            
            if state == "unrated":
                col1, col2, _ = st.columns([0.5, 0.5, 8])
                
                if col1.button("👍", key=f"up_{i}", type="tertiary"):
                    save_to_csv({
                        "timestamp": msg["timestamp"],
                        "user_input": st.session_state.messages[i-1]["content"],
                        "bot_response": msg["content"],
                        "response_length": len(msg["content"]),
                        "feedback": "positive",
                        "optional_comment": ""
                    })
                    st.session_state.messages[i]["feedback_state"] = "rated"
                    st.rerun()
                    
                if col2.button("👎", key=f"down_{i}", type="tertiary"):
                    st.session_state.messages[i]["feedback_state"] = "rating_negative"
                    st.rerun()
                    
                st.caption("Your feedback helps improve responses")
                
            elif state == "rating_negative":
                with st.form(key=f"neg_form_{i}"):
                    comment = st.text_input("What could be better?", key=f"comment_{i}")
                    if st.form_submit_button("Submit Feedback"):
                        save_to_csv({
                            "timestamp": msg["timestamp"],
                            "user_input": st.session_state.messages[i-1]["content"],
                            "bot_response": msg["content"],
                            "response_length": len(msg["content"]),
                            "feedback": "negative",
                            "optional_comment": comment
                        })
                        st.session_state.messages[i]["feedback_state"] = "rated"
                        st.rerun()
                st.caption("Your feedback helps improve responses")

# Chat Input Area
if user_input := st.chat_input("Type your message here..."):
    # Append User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Generate Bot Response
    bot_response = get_response(user_input)
    
    # Append Bot Message with metadata for feedback
    st.session_state.messages.append({
        "role": "assistant", 
        "content": bot_response,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "feedback_state": "unrated"
    })
    
    st.rerun()
