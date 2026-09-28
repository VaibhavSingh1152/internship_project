import ollama

def explain_prediction(fund, prediction, trend="neutral"):
    prompt = f"""
    You are a finance assistant.

    Fund: {fund}
    Predicted NAV: {prediction}
    Trend: {trend}

    Explain this prediction in simple terms and give a short insight.
    Do NOT give financial advice.
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]