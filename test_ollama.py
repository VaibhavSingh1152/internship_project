import ollama

try:
    response = ollama.chat(
        model="gemma2:2b",
        messages=[
            {
                "role": "user",
                "content": "Say hello in one sentence."
            }
        ]
    )

    print("SUCCESS")
    print(response["message"]["content"])

except Exception as e:
    print("ERROR")
    print(e)