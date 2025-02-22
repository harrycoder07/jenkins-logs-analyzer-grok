import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# Simulated Grok summarization
def generate_summary_grok(log_text):
    """
    Placeholder for Grok's response. Manually query Grok with log_text for a real summary.
    Example: "Summarize this Jenkins log failure: <log_text>"
    """
    if "ERROR" in log_text:
        return f"Grok Summary: The build failed due to an error: {log_text.split('ERROR')[1].strip()[:50]}..."
    return "Grok Summary: No significant failure detected."

# Analyze logs and detect anomalies
def analyze_logs(log_file, output_summary_file):
    with open(log_file, 'r', encoding='utf-8') as f:
        logs = f.readlines()
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(logs).toarray()
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(X)
    predictions = model.predict(X)  # -1 = anomaly, 1 = normal
    anomalies = [log.strip() for log, pred in zip(logs, predictions) if pred == -1]
    if anomalies:
        summary = generate_summary_grok(" ".join(anomalies))
    else:
        summary = "Grok Summary: No anomalies detected in the logs."
    with open(output_summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    return anomalies, summary

if __name__ == "__main__":
    log_file = "logs/build_log.txt"
    summary_file = "summaries/failure_summary.txt"
    if os.path.exists(log_file):
        anomalies, summary = analyze_logs(log_file, summary_file)
        print("Anomalies:", anomalies)
        print("Summary:", summary)
        print("For a real Grok summary, query: 'Summarize this Jenkins log failure: " + " ".join(anomalies) + "'")
    else:
        print("Log file not found. Create logs/build_log.txt to test.")