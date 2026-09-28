import ollama

def ask_fin_gpt(prompt):
    response = ollama.chat(
        model="gemma2:2b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]
