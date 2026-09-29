from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="local",
)

messages = []

while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ("exit", "quit"):
        break
    messages.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
    model="qwen",
    messages=messages,
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    print("Agent: ", reply)