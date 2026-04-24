import streamlit as st
import time

# --- Page Config ---
st.set_page_config(page_title="RaiTalk Chatbot Simulator", page_icon="💬", layout="centered")

st.title("💬 RaiTalk Chatbot (Simulated)")
st.caption("Internship Project - AI Engineer: Dipak Appasaheb Khandagale")

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am the RaiTalk assistant. How can I help you today?"}
    ]

# --- Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- AI Response Logic (Rule-based for Demo) ---
def get_ai_response(user_input):
    user_input = user_input.lower()
    if "pricing" in user_input or "cost" in user_input:
        return "Our pricing plans start at $10/month for the Basic tier. We also have Pro and Enterprise options."
    elif "password" in user_input or "reset" in user_input:
        return "To reset your password, please go to your Account Settings and click 'Reset Password'."
    elif "trial" in user_input or "free" in user_input:
        return "Yes! We offer a 14-day free trial on all of our paid plans. Would you like a link to sign up?"
    elif "hello" in user_input or "hi" in user_input:
        return "Hi there! How can I assist you with RaiTalk today?"
    else:
        return "I'm still learning! Could you please provide more details or ask about our pricing, free trial, or password resets?"

# --- Chat Input ---
if prompt := st.chat_input("Ask me a question..."):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Simulate typing delay
        response_text = get_ai_response(prompt)
        for chunk in response_text.split(" "):
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
            
        message_placeholder.markdown(full_response)
        
    # Add assistant response to state
    st.session_state.messages.append({"role": "assistant", "content": full_response})
