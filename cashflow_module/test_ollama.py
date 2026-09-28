from ollama import chat

response = chat(
    model="gemma2:2b",
    messages=[
        {
            "role": "user",
            "content": "Say hello in one line"
        }
    ]
)

print(response["message"]["content"])