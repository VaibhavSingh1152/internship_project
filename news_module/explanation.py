import ollama


def generate_explanation(
        fund_name,
        prediction,
        signal,
        confidence,
        news_headlines,
        sentiment_score):

    prompt = f"""
You are a financial analysis assistant.

Fund Name:
{fund_name}

Predicted NAV:
{prediction:.2f}

Signal:
{signal}

Confidence:
{confidence:.2f}%

News Sentiment Score:
{sentiment_score}%

Recent News:
"""

    for headline in news_headlines:
        prompt += f"\n- {headline}"

    prompt += """

Explain:
1. Why the model may be bullish or bearish.
2. How the news sentiment relates to the prediction.
3. Mention possible risks.
4. Keep explanation under 150 words.
5. Do not give investment advice.
"""

    try:

        response = ollama.chat(
            model="gemma2:2b",   # change if your model name differs
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:

        return f"AI explanation error: {e}"