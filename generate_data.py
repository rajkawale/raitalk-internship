import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

def get_path(folder, filename):
    return os.path.join(base_dir, folder, filename)

# 1. Generate shared-data
print("Generating shared-data...")
num_logs = 50
log_ids = [f"LOG_{str(i).zfill(3)}" for i in range(1, num_logs + 1)]
user_ids = [f"USR_{random.randint(10, 30)}" for _ in range(num_logs)]
base_time = datetime(2026, 4, 20, 10, 0, 0)
timestamps = [base_time + timedelta(minutes=random.randint(1, 1000)) for _ in range(num_logs)]
messages = ["Hi, I need help with my account.", "What are your pricing plans?", "How do I reset my password?", "Is there a free trial?", "Thank you!", "I'm having trouble logging in."]
senders = ['user', 'bot'] * (num_logs // 2)

chat_logs_raw = pd.DataFrame({
    'log_id': log_ids,
    'timestamp': sorted(timestamps),
    'user_id': user_ids,
    'message': [random.choice(messages) for _ in range(num_logs)],
    'sender': [random.choice(['user', 'bot']) for _ in range(num_logs)]
})
chat_logs_raw.to_csv(get_path('shared-data', 'chat_logs_raw.csv'), index=False)

processed_data = chat_logs_raw.copy()
processed_data['message_length'] = processed_data['message'].apply(len)
processed_data['sentiment_score'] = [round(random.uniform(-1, 1), 2) for _ in range(num_logs)]
processed_data.to_csv(get_path('shared-data', 'processed_data.csv'), index=False)

# 2. Generate ai-engineer-dipak logs
print("Generating ai-engineer-dipak data...")
eval_logs = pd.DataFrame({
    'timestamp': [base_time + timedelta(hours=i) for i in range(10)],
    'prompt_version': ['v1', 'v1', 'v1', 'v1', 'v1', 'v2', 'v2', 'v2', 'v2', 'v2'],
    'user_input': ["Hello", "Reset password", "Pricing", "Free trial", "Help", "Hello", "Reset password", "Pricing", "Free trial", "Help"],
    'bot_response': ["Hi there!", "Go to settings.", "It's $10/mo.", "Yes, 14 days.", "How can I assist?", "Hello! How can I help you today?", "You can reset it in settings.", "Our plans start at $10/month.", "Yes, we offer a 14-day free trial.", "I am here to help!"],
    'rating': [3, 2, 4, 5, 3, 5, 4, 5, 5, 5]
})
eval_logs.to_csv(get_path('ai-engineer-dipak', 'evaluation_logs.csv'), index=False)

# 3. Generate data-analyst-sayali logs
print("Generating data-analyst-sayali data...")
session_ids = [f"SESS_{str(i).zfill(3)}" for i in range(1, 21)]
unique_users = list(set(user_ids))
sessions = pd.DataFrame({
    'session_id': session_ids,
    'user_id': [random.choice(unique_users) for _ in range(20)],
    'start_time': [base_time + timedelta(minutes=i*45) for i in range(20)],
    'end_time': [base_time + timedelta(minutes=i*45 + random.randint(2, 30)) for i in range(20)],
    'total_messages': [random.randint(2, 15) for _ in range(20)],
    'drop_off': [random.choice([True, False, False, False]) for _ in range(20)]
})
sessions.to_csv(get_path('data-analyst-sayali', 'user_sessions.csv'), index=False)

# 4. Generate data-analyst-priya logs
print("Generating data-analyst-priya data...")
priya_eval = pd.DataFrame({
    'interaction_id': log_ids[:20],
    'expected_intent': ['greeting', 'password_reset', 'pricing', 'trial', 'support'] * 4,
    'actual_intent': ['greeting', 'password_reset', 'pricing', 'trial', 'support'] * 3 + ['unknown', 'support', 'pricing', 'greeting', 'unknown'],
    'accuracy_score': [random.choice([0.8, 0.9, 1.0]) for _ in range(15)] + [0.1, 0.4, 0.8, 0.2, 0.1],
    'helpfulness_score': [random.randint(3, 5) for _ in range(20)]
})
priya_eval.to_csv(get_path('data-analyst-priya', 'evaluation_dataset.csv'), index=False)

# Excel for Priya
try:
    with pd.ExcelWriter(get_path('data-analyst-priya', 'analysis.xlsx')) as writer:
        priya_eval.to_excel(writer, sheet_name='Raw Data', index=False)
        
        # Summary pivot
        summary = priya_eval.groupby('expected_intent').agg(
            avg_accuracy=('accuracy_score', 'mean'),
            avg_helpfulness=('helpfulness_score', 'mean'),
            count=('interaction_id', 'count')
        ).reset_index()
        summary.to_excel(writer, sheet_name='Intent Summary', index=False)
    print("Excel file generated successfully.")
except ImportError:
    print("openpyxl not installed, skipping Excel generation.")

print("All datasets generated successfully!")
