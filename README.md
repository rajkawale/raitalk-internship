# AI Conversational System with Feedback, Analytics, and Evaluation

## Overview
This project demonstrates a complete product loop:
`User interaction → AI response → Feedback → Data analysis → Model evaluation → Improvement`

## Team Roles
* **Dipak (AI Engineer)**: Builds chatbot, generates responses, captures feedback.
* **Sayali (Data Analyst)**: Analyzes feedback data, identifies patterns, suggests improvements.
* **Priya (Evaluation Analyst)**: Measures response quality using defined metrics.

## System Flow
`User → Chatbot → Feedback (👍 👎) → CSV logs → Sayali Dashboard (analysis) → Priya Dashboard (evaluation)`

## How the System Works

### 1. Response Generation
Rule-based logic selects responses based on user input.

### 2. Feedback Capture
User clicks 👍 or 👎. Stored in `shared-data/chat_logs_raw.csv`.

### 3. Analysis Logic
Negative feedback is categorized using keyword matching. Example:
* `"pricing"` → Missing Specific Answer
* `"generic"` → Generic Response

### 4. Evaluation Metrics
* **Relevance Score**: `(Number of relevant responses / Total responses) * 100`
* **Helpfulness Score**: `Sum of helpfulness scores / Total responses`

## How to Run Locally

**Step 1: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 2: Run chatbot**
```bash
python -m streamlit run ai-engineer-dipak/app.py
```

**Step 3: Generate some data**
Interact with the chatbot and click the feedback buttons!

**Step 4: Run Sayali's dashboard**
```bash
python -m streamlit run data-analyst-sayali/dashboard.py
```

**Step 5: Run Priya's dashboard**
```bash
python -m streamlit run data-analyst-priya/evaluation_dashboard.py
```

> **Important**: If dashboards show no data, run the chatbot first to generate logs!

## Data Location
All modules use a centralized database:
`shared-data/chat_logs_raw.csv`

## Demo Video
*(Add Loom link here)*

## Expected Outcome
You should see:
* Chatbot responding
* Feedback being logged
* Dashboard updating
* Evaluation metrics changing

## Notes
This is a simplified prototype using rule-based logic and manual evaluation to demonstrate product thinking and data flow.
