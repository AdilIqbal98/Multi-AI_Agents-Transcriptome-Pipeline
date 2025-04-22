# advanced_chatbot.py

import openai
import os

# Load your API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create a client for OpenAI SDK v1
client = openai.OpenAI()

# Initialize conversation history
conversation = [
    {"role": "system", "content": "You are a thoughtful medical assistant who provides accurate, helpful responses."}
]

print("Welcome to your medical assistant chatbot! Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Exiting. Stay healthy! 👋")
        break

    # Add user message to the conversation
    conversation.append({"role": "user", "content": user_input})

    # Get a response from the assistant
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=conversation,
            temperature=0.6
        )
        reply = response.choices[0].message.content.strip()
        print("Assistant:", reply)

        # Add assistant response to history
        conversation.append({"role": "assistant", "content": reply})

    except Exception as e:
        print("Error communicating with OpenAI:", e)
