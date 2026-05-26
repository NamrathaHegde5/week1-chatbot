from anthropic import Anthropic
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()

# Create Anthropic client
client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)
print("AI Chatbot Started")
print("Type 'exit' to quit\n")

while True:
    question = input("You: ")

    # Exit condition
    if question.lower() == "exit":
        print("Chat ended.")
        break

    # Send question to Claude
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )
    # Print AI response
    print("\nAI:", response.content[0].text)
    print()

    