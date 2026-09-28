from google import genai
import os

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

messages = []

while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ("exit", "quit"):
        break
    messages.append({"role": "user", "content": user_input})
    
    response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Explain what an AI agent is in one sentence.",
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    print("Agent: ", reply)